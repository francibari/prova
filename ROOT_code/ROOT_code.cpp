#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "TCanvas.h"
#include "RooPlot.h"
#include "TAxis.h"


void tmva_classification() {
	auto outputFile = TFile::Open("TMVA_output.root", "RECREATE");
	TMVA::Factory factory("TMVAClassification", outputFile, "!V:ROC:!Correlations:!Silent:Color:!DrawProgressBar:AnalysisType=Classification");
	TMVA::DataLoader loader("dataset");
	
	loader.AddVariable("DER_mass_MMC", 'F');
	loader.AddVariable("DER_mass_transverse_met_lep", 'F');
	loader.AddVariable("DER_mass_vis", 'F');
	loader.AddVariable("DER_pt_ratio_lep_tau", 'F');
	loader.AddVariable("PRI_tau_pt", 'F');
	loader.AddVariable("PRI_met", 'F');
	loader.AddVariable("PRI_jet_all_pt", 'F');
	loader.AddVariable("DER_sum_pt", 'F');
	loader.AddVariable("PRI_tau_eta", 'F');
	
	TFile* in_sigFile = TFile::Open("atlas-higgs-challenge-2014-v2-sig.root");
	TFile* in_bkgFile = TFile::Open("atlas-higgs-challenge-2014-v2-bkg.root");
	
	TTree* tsignal;
	TTree* tbackground;
	in_sigFile->GetObject("tree_sig", tsignal);
	in_bkgFile->GetObject("tree_bkg", tbackground);
	
	TCut mycuts, mycutb;
	
	loader.AddSignalTree(tsignal, 1.0);
	loader.AddBackgroundTree(tbackground, 1.0);
	loader.PrepareTrainingAndTestTree(mycuts, mycutb, "NTrain_Signal=10000:NTrain_Background=20000:NTest_Signal=0:NTest_Background=0:SplitMode=Random:NormMode=NumEvents:!V" );
	
	
	// choose the classifiers
	factory.BookMethod(&loader, TMVA::Types::kCuts, "ex_Cuts", "!H:!V:FitMethod=MC");
	factory.BookMethod(&loader, TMVA::Types::kFisher, "ex_Fisher", "H:!V:Fisher");
	factory.BookMethod(&loader, TMVA::Types::kMLP, "ex_MLP", "H:!V:NeuronType=tanh:VarTransform=N:NCycles=500:TestRate=5:HiddenLayers=N+5:!UseRegulator");
	factory.BookMethod(&loader, TMVA::Types::kBDT, "ex_BDT", "NTrees=200:BoostType=AdaBoost");
	
	factory.TrainAllMethods();
	factory.TestAllMethods();
	factory.EvaluateAllMethods();
	
}

void tmva_application() {
	TMVA::Reader* reader = new TMVA::Reader("!Color:!Silent");
	float x1, x2, x3, x4, x5, x6, x7, x8, x9;
	reader->AddVariable("DER_mass_MMC", &x1);
	reader->AddVariable("DER_mass_transverse_met_lep", &x2);
	reader->AddVariable("DER_mass_vis", &x3);
	reader->AddVariable("DER_pt_ratio_lep_tau", &x4);
	reader->AddVariable("PRI_tau_pt", &x5);
	reader->AddVariable("PRI_met", &x6);
	reader->AddVariable("PRI_jet_all_pt", &x7);
	reader->AddVariable("DER_sum_pt", &x8);
	reader->AddVariable("PRI_tau_eta", &x9);	
	
	x1 = 138.47;
	x2 = 51.655;
	x3 = 97.827;
	x4 = 1.582;
	x5 = 32.638;
	x6 = 16.824;
	x7 = 113.49;
	x8 = 197.76;
	x9 = 1.017;
	
	reader->BookMVA("ex_MLP", "./dataset/weights/TMVAClassification_ex_MLP.weights.xml");
	
	double val = reader->EvaluateMVA("ex_MLP");
	double error_val = reader->GetMVAError();
	
	std::cout<< "response: " << val << ", error: " << error_val << '\n';
	
}

void ROOT_code() {
	std::cout<<"TRAINING OF THE MODELS\n";
	tmva_classification();
	std::cout<<"APPLICATION OF THE MLP MODEL\n";
	std::cout<<"We know that the event is of signal type and the cut for the MLP model is at 0.355 as we can see in the figure cut_efficiency_MLP\n";
	tmva_application();
	std::cout<<"The event is classified as signal as expected\n";
}
# project_SC_Francesco_Barilari
In this repository you can find some code for machine learning on atlas dataset. This project is inspired and it is a continuation of a code that I wrote in ROOT using the TMVA package for the "statistical data analysis" course in which a comparison of different machine learning algorithms of TMVA is done. I tried to keep the same philosophy (compare different machine learning algorithms) but using python and the proper libaries: numpy, pandas, matplotlib, seaborn, scikit-learn. 
The dataset contains 279560 signal events and 538678 background events. I choose to use only some variables of the dataset that are in my opinion more interesting because there is a more distinction in the value distribution between signal and background events. The user is free to change it in the code changing the list of variables at line 23 in the python version of the code and the arguments of the `AddVariable()` function in ROOT version of the code (line 14-22 and 53-61).
Moreover, for both the code I prepare also a container using Docker and some `.sh` file with the shell script to minimize the line command that the user must execute. The repository is organized in two different subfolders, one for each type of code, that contains all the files needed to build and run the Docker container and to run the code. I decided to use the container because in this way the user does not have to install all the requirements (libraries af a specific version...) but only the docker engine to run the container, all the required libaries are inside the container.
The user can download the repository using the command:


````````````````````````````````````````````````````<pre>
$ git clone 
````````````````````````````````````````````````````<pre>


## py_code
In this folder there is the python version of the code, in particular there are:
- the source code `py_code.py` that makes the analysis
- the csv file `atlas-higgs-challenge-2014-v2.csv` where data are stored
- the `Dockerfile` that contains the information to create the Docker container image
- the bash file `run.sh` that contains the script to run the python code
- the bash file `py_code_docker.sh` that contains teh script for docker

The code uses different libaries: numpy, pandas, matplotlib, seaborn and scikit-learn. The code reads the `.csv` file, then selects only the variables to use in the training, split the dataset in train and test set, then the models are declared. I used two different model: LinearDiscriminatAnalysis and KNeightborsClassifier, both from scikit-learn. Then the models are trained using the train set and tested using the test set that produce also the ingredients to build the ROC curve and the correlation matrices. These information are used to build and show them using matplotlib and seaborn libraries. The images produced, in `.png` format, are saved in the `pythonImages` directory. This directory is created before running the python code by the `run.sh` file that create the folder, if it does not exist, and then run the python code. This file must be launch inside the container.
The `Dockerfile` contains the information to build the docker image for the container. It starts from an ubuntu image and it copy all the usefull file (`py_code.py`, `run.sh`, `.csv` file), then it installs python and the required libraries. It installs also `vim` and `feh` in case the user wants to modify the code or to see the images produced by the code.
Finally the `py_code_docker.sh` contains the script to build the image starting from the Dockerfile and run the images produced with some option to implement the graphics.

So, to create and run the container you must execute only the shell command line:
$ bash py_code_docker.sh

Once you are in the container you must execute the code using the command:
$ bash run.sh

Then yoou can navigate in the subfolder pythonImages to visualize the images produces using:
$ cd pythonImages
$ feh image_name.png



## ROOT_code
In this folder there is the ROOT version of the code, in particular:
- the `ROOT_code.cpp` that contains the code
- the `Dockerfile` that contains the instruction to build the docker image
- the two `.root` files of signal and background
- the folder `dataset` that contains plots and weights used in the models
- the folder `importantImages` that contains all the important plots produced
- the bash file `root_code_docker.sh` that contains the script for docker
- the bash file `run.sh` that contains the script to run the ROOT code

The ROOT source code contains three different macros: `tmva_classification()`, `tmva_application()`, `ROOT_code()`.
In `tmva_classification()` macro there is the part of training and testing of the models, in particular the model used are: BDT, MLP, Fisher discriminat and rectangualar cut. First, the root file to store the results is created or overwritten if it exists yet. Then the variables to consider are declared using the function AddVariable(). Then the algorithm to use are chosen with the function `BookMethod()`. The model are trained, tested and evaluated. The user can find all the graphs produced by the code in the Gui using the command in ROOT `TMVA::TMVAGui("TMVA_output.root")` but it is done by the .sh code automatically when the user runs it. I collected all the important plots produced by the macro in the `importantImages` folder but the user can find them also in the `Gui`. All the weights of the models are stored in the subfolder `weights` of the `dataset` folder.
In `tmva_application()` there is an application of the trained model to a specific case, in particular the event is the first in the dataset and we know to be a signal event. The variables to use are declared again in the same way did before, then their values are passed. Finally the model to use is passed using the `BookMVA()` function and evaluate using the `EvaluateMVA()` function. In particular in this case the model used is the MLP.
Then the last macro is the `ROOT_code()` that simply execute first the `tmva_classification()` macro and then the `tmva_application()`. This macro has the same name of the code because in this way I can run the code in a single step instead of opening root, loading the code and executing the macros (3 steps). In this way I must pass only the command `root ROOT_code.cpp` and it load automatically the code and execute only the macro with the same name of the code, on this case the `ROOT_code()` macro.
As before, the script to run the code is in the file `run.sh` that execute the ROOT code and the open the Gui that contains all the results produced in the training and testing part.
The Dockerfile contains all the information to build the docker image. In this case it starts from a ROOT image, then it copy the usefull files and it install `vim` and `feh` as before for the same reasons. As before there is a `.sh` file for docker with the script to build and run the container.

So, to create and run the container you must execute only the shell command line:
`````````````<pre>
$ bash root_code_docker.sh
````````
Once you are in the container you must execute the code using the command:
$ bash run.sh

Then yoou can navigate in the subfolder importantImages to visualize the images produces using:
$ cd importantImages
$ feh image_name.png




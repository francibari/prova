FROM rootproject/root:latest

WORKDIR /root_code

COPY atlas-higgs-challenge-2014-v2-bkg.root atlas-higgs-challenge-2014-v2-bkg.root 
COPY atlas-higgs-challenge-2014-v2-sig.root atlas-higgs-challenge-2014-v2-sig.root
COPY ROOT_code.cpp ROOT_code.cpp
COPY dataset dataset
COPY important_images important_images
COPY run.sh run.sh

RUN apt-get install -y vim
RUN apt-get install -y feh

CMD ["bash"]
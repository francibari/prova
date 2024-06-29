FROM ubuntu:22.04

WORKDIR /py_code

SHELL ["/bin/bash", "-c"]

COPY py_code.py py_code.py
COPY atlas-higgs-challenge-2014-v2.csv atlas-higgs-challenge-2014-v2.csv
COPY run.sh run.sh

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y vim
RUN apt-get install -y feh
RUN apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install numpy pandas matplotlib seaborn
RUN pip3 install scikit-learn

CMD [ "bash" ]

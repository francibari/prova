#!/bin/bash

root -l -q ROOT_code.cpp

root -l -e 'TMVA::TMVAGui("TMVA_output.root")'
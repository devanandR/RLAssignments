#!/bin/bash

PWD=`pwd`
cp $1 InputTraject.txt
python EstimateDev.py 
#cat OutputPi.txt

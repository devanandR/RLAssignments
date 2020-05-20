#!/bin/bash

PWD=`pwd`
cp $1 InputMdp.txt
python MdpDev.py 
cat OutputPi.txt

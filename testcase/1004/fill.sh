#! /bin/bash

cd `cat ../path`
./qlinkage -c 'что'
./qlinkage -c 'чем'
./qconcept -c 1 'быть'
./qconcept -c 2 'процедура'
./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c  "#$CONCEPT1 ?что быть ?чем процедура"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
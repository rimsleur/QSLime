#! /bin/bash

cd `cat ../path`
./qlinkage -c 'кто'
./qlinkage -c 'что'
./qlinkage -c 'чем'
./qlinkage -c 'какое'
./qconcept -c 1 'выполнять'
./qconcept -c 1 'иметь'
./qconcept -c 1 'быть'
./qconcept -c 2 'ты'
./qconcept -c 2 'процедура'
./qconcept -c 2 'имя'
./qconcept -c 2 'TestProcedure1'
./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какое TestProcedure1"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'ты ?кто выполнять ?что (=процедура ?что иметь ?что имя ?какое TestProcedure1).'
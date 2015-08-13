#! /bin/bash

cd `cat ../path`
./qlinkage -c 'кто'
./qlinkage -c 'что'
./qlinkage -c 'чем'
./qlinkage -c 'какой'
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
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TestProcedure1"
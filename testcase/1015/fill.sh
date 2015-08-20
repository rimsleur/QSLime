#! /bin/bash

cd `cat ../path`
./qlinkage -c 'кто'
./qlinkage -c 'что'
./qlinkage -c 'какой'
./qlinkage -c 'чем'
./qconcept -c 1 'выполнять'
./qconcept -c 1 'иметь'
./qconcept -c 1 'быть'
./qconcept -c 1 'печатать'
./qconcept -c 2 'ты'
./qconcept -c 2 'значение'
./qconcept -c 2 'процедура'
./qconcept -c 2 'имя'
./qconcept -c 2 'TestProcedure1'
./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TestProcedure1"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'печатать ?что значение ?какой "INIT[5:5]\n".'
./qconcept -a $CONCEPT2 1 'печатать ?что значение ?какой "REFR[]\n".'
./qconcept -a $CONCEPT2 2 'печатать ?что значение ?какой "SET[A1]\n".'
./qconcept -a $CONCEPT2 3 'печатать ?что значение ?какой "REFR[]\n".'
./qconcept -a $CONCEPT2 4 'печатать ?что значение ?какой "SET[B2]\n".'
./qconcept -a $CONCEPT2 5 'печатать ?что значение ?какой "REFR[]\n".'
./qconcept -a $CONCEPT2 6 'печатать ?что значение ?какой "SET[C3]\n".'
./qconcept -a $CONCEPT2 7 'печатать ?что значение ?какой "REFR[]\n".'
./qconcept -a $CONCEPT2 8 'печатать ?что значение ?какой "SET[D4]\n".'
./qconcept -a $CONCEPT2 9 'печатать ?что значение ?какой "REFR[]\n".'
./qconcept -a $CONCEPT2 10 'печатать ?что значение ?какой "SET[E5]\n".'
./qconcept -a $CONCEPT2 11 'печатать ?что значение ?какой "REFR[]\n".'
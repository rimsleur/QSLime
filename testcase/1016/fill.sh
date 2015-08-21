#! /bin/bash

cd `cat ../path`
./qlinkage -c 'кто'
./qlinkage -c 'что'
./qlinkage -c 'какой'
./qlinkage -c 'чем'
./qlinkage -c 'чего'
./qlinkage -c 'для-чего'
./qlinkage -c 'на-что'
./qlinkage -c 'как-что'
./qconcept -c 1 'выполнять'
./qconcept -c 1 'иметь'
./qconcept -c 1 'быть'
./qconcept -c 1 'создавать'
./qconcept -c 1 'использовать'
./qconcept -c 1 'устанавливать'
./qconcept -c 1 'добавлять'
./qconcept -c 1 'печатать'
./qconcept -c 2 'ты'
./qconcept -c 2 'значение'
./qconcept -c 2 'процедура'
./qconcept -c 2 'имя'
./qconcept -c 2 'список'
./qconcept -c 2 'элемент'
./qconcept -c 2 'ссылка'
./qconcept -c 2 'TestProcedure1'
./qconcept -c 2 'L1'
./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TestProcedure1"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'создавать ?что (=список ?что иметь ?что имя ?какой L1).'
./qconcept -a $CONCEPT2 1 'добавлять ?что элемент ?чего список.'
./qconcept -a $CONCEPT2 2 'создавать ?что список.'
./qconcept -a $CONCEPT2 3 'добавлять ?что элемент ?чего список.'
./qconcept -a $CONCEPT2 4 'устанавливать ?что значение (?чего элемент, ?какой 101).'
./qconcept -a $CONCEPT2 5 'добавлять ?что элемент ?чего список.'
./qconcept -a $CONCEPT2 6 'устанавливать ?что значение (?чего элемент, ?какой 102).'
./qconcept -a $CONCEPT2 7 'печатать ?что значение ?чего элемент.'
./qconcept -a $CONCEPT2 8 'печатать ?что значение ?какой "\n"'
./qconcept -a $CONCEPT2 9 'создавать ?что ссылка (?для-чего элемент (?чего (=список ?что иметь ?что имя ?какой L1), ?какой 1), ?на-что список).'
./qconcept -a $CONCEPT2 10 'создавать ?что список.'
./qconcept -a $CONCEPT2 11 'добавлять ?что элемент ?чего список.'
./qconcept -a $CONCEPT2 12 'устанавливать ?что значение (?чего элемент, ?какой 103).'
./qconcept -a $CONCEPT2 13 'печатать ?что значение ?чего элемент.'
./qconcept -a $CONCEPT2 14 'печатать ?что значение ?какой "\n"'
./qconcept -a $CONCEPT2 15 'использовать (?что элемент (?чего (=список ?что иметь ?что имя ?какой L1), ?какой 1), ?как-что список).'
./qconcept -a $CONCEPT2 16 'печатать ?что значение ?чего элемент (?чего список, ?какой 1).'
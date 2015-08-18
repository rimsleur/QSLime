#! /bin/bash

cd `cat ../path`
./qlinkage -c 'кто'
./qlinkage -c 'что'
./qlinkage -c 'какой'
./qlinkage -c 'чего'
./qlinkage -c 'чем'
./qlinkage -c 'на-сколько'
./qlinkage -c 'на-что'
./qlinkage -c 'для-чего'
./qlinkage -c 'к-чему'
./qconcept -c 1 'выполнять'
./qconcept -c 1 'иметь'
./qconcept -c 1 'быть'
./qconcept -c 1 'создавать'
./qconcept -c 1 'устанавливать'
./qconcept -c 1 'регистрировать'
./qconcept -c 1 'присоединять'
./qconcept -c 1 'печатать'
./qconcept -c 2 'ты'
./qconcept -c 2 'поле'
./qconcept -c 2 'значение'
./qconcept -c 2 'процедура'
./qconcept -c 2 'имя'
./qconcept -c 2 'событие'
./qconcept -c 2 'обработчик'
./qconcept -c 2 'условие'
./qconcept -c 2 'A1'
./qconcept -c 2 'B1'
./qconcept -c 2 'TestProcedure1'
./qconcept -c 2 'TestProcedure2'
./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TestProcedure1"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'создавать ?что условие.'
./qconcept -a $CONCEPT2 1 'создавать ?что (=поле ?что иметь ?что имя ?какой A1).'
./qconcept -a $CONCEPT2 2 'регистрировать ?что событие (?на-что значение ?какой 2, ?для-чего поле).'
./qconcept -a $CONCEPT2 3 'присоединять (?что событие, ?к-чему условие).'
./qconcept -a $CONCEPT2 4 'создавать ?что (=поле ?что иметь ?что имя ?какой B1).'
./qconcept -a $CONCEPT2 5 'регистрировать ?что событие (?на-что значение ?какой 5, ?для-чего поле).'
./qconcept -a $CONCEPT2 6 'присоединять (?что событие, ?к-чему условие).'
./qconcept -a $CONCEPT2 7 'устанавливать ?что обработчик (?чего условие, ?какой \"печатать ?что значение ?какой \\"2 + 5 = 7\\".\").'
./qconcept -a $CONCEPT2 8 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой A1), ?какой 2).'
./qconcept -a $CONCEPT2 9 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой A1), ?какой 3).'
./qconcept -a $CONCEPT2 10 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой B1), ?какой 5).'
./qconcept -a $CONCEPT2 11 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой A1), ?какой 2).'
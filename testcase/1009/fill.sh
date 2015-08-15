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
./qconcept -c 1 'выполнять'
./qconcept -c 1 'иметь'
./qconcept -c 1 'быть'
./qconcept -c 1 'создавать'
./qconcept -c 1 'устанавливать'
./qconcept -c 1 'регистрировать'
./qconcept -c 1 'печатать'
./qconcept -c 2 'ты'
./qconcept -c 2 'поле'
./qconcept -c 2 'значение'
./qconcept -c 2 'процедура'
./qconcept -c 2 'имя'
./qconcept -c 2 'событие'
./qconcept -c 2 'обработчик'
./qconcept -c 2 'изменение'
./qconcept -c 2 'TestField1'
./qconcept -c 2 'TestProcedure1'
./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TestProcedure1"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'создавать ?что (=поле ?что иметь ?что имя ?какой TestField1).'
./qconcept -a $CONCEPT2 1 'регистрировать ?что событие (?на-что изменение, ?для-чего поле).'
./qconcept -a $CONCEPT2 2 'устанавливать ?что обработчик (?чего событие, ?какой \"печатать ?что значение ?чего поле.\").'
./qconcept -a $CONCEPT2 3 'устанавливать ?что значение (?чего поле, ?какой 1).'
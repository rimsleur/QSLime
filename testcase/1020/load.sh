#! /bin/bash

EXEC_PWD=$PWD
cd ../../database
./clear_user_space.sh
cd $EXEC_PWD
cd `cat ../path`

./qconcept -c 2 'TestProcedure1'
./qconcept -c 2 'X=1'
./qconcept -c 2 'X=2'
./qconcept -c 2 'X=3'
./qconcept -c 2 'XL'
./qconcept -c 2 'X'
./qconcept -c 2 'Y'
./qconcept -c 2 'Y=3'
./qconcept -c 2 'Print'
./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TestProcedure1"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'создавать ?что (=поле ?что иметь ?что имя ?какой XL).'
./qconcept -a $CONCEPT2 1 'создавать ?что (=поле ?что иметь ?что имя ?какой X).'
./qconcept -a $CONCEPT2 2 'регистрировать ?что событие (?на-что значение ?какой 1, ?для-чего поле).'
./qconcept -a $CONCEPT2 3 'устанавливать ?что обработчик (?чего событие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой X=1).\").'
./qconcept -a $CONCEPT2 4 'регистрировать ?что событие (?на-что значение ?какой 2, ?для-чего поле).'
./qconcept -a $CONCEPT2 5 'устанавливать ?что обработчик (?чего событие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой X=2).\").'
./qconcept -a $CONCEPT2 6 'регистрировать ?что событие (?на-что значение ?какой 3, ?для-чего поле).'
./qconcept -a $CONCEPT2 7 'устанавливать ?что обработчик (?чего событие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой X=3).\").'
./qconcept -a $CONCEPT2 8 'создавать ?что (=поле ?что иметь ?что имя ?какой Y).'
./qconcept -a $CONCEPT2 9 'регистрировать ?что событие (?на-что значение ?какой 3, ?для-чего поле).'
./qconcept -a $CONCEPT2 10 'устанавливать ?что обработчик (?чего событие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой Y=3).\").'
./qconcept -a $CONCEPT2 11 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой X), ?какой 1).'
./qconcept -a $CONCEPT2 12 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой Y), ?какой 1).'
./qconcept -a $CONCEPT2 13 'печатать ?что значение ?какой "INIT[3:3]\n".'
./qconcept -a $CONCEPT2 14 'печатать ?что значение ?какой "REFR[]\n".'

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой X=1"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой XL), ?какой "A").'
./qconcept -a $CONCEPT2 16 'выполнять ?что (=процедура ?что иметь ?что имя ?какой Print).'
./qconcept -a $CONCEPT2 17 'увеличивать (?что значение ?чего (=поле ?что иметь ?что имя ?какой X), ?на-сколько 1).'

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой X=2"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой XL), ?какой "B").'
./qconcept -a $CONCEPT2 19 'выполнять ?что (=процедура ?что иметь ?что имя ?какой Print).'
./qconcept -a $CONCEPT2 20 'увеличивать (?что значение ?чего (=поле ?что иметь ?что имя ?какой X), ?на-сколько 1).'

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой X=3"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой XL), ?какой "C").'
./qconcept -a $CONCEPT2 22 'выполнять ?что (=процедура ?что иметь ?что имя ?какой Print).'
./qconcept -a $CONCEPT2 23 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой X), ?какой 1).'
./qconcept -a $CONCEPT2 24 'увеличивать (?что значение ?чего (=поле ?что иметь ?что имя ?какой Y), ?на-сколько 1).'

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой Y=3"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'удалять ?что событие (?на-что значение ?какой 1, ?для-чего (=поле ?что иметь ?что имя ?какой X)).'

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой Print"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'печатать ?что значение ?какой "SET[".'
./qconcept -a $CONCEPT2 27 'печатать ?что значение ?чего (=поле ?что иметь ?что имя ?какой XL).'
./qconcept -a $CONCEPT2 28 'печатать ?что значение ?чего (=поле ?что иметь ?что имя ?какой Y).'
./qconcept -a $CONCEPT2 29 'печатать ?что значение ?какой "]\n".'
./qconcept -a $CONCEPT2 30 'печатать ?что значение ?какой "REFR[]\n".'
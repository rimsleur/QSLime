#! /bin/bash

EXEC_PWD=$PWD
cd ../../database
./clear_user_space.sh
cd $EXEC_PWD
cd `cat ../path`

./qconcept -c 2 'TestProcedure1'
./qconcept -c 2 'A'
./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TestProcedure1"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'создавать ?что (=поле ?что иметь ?что имя ?какой A).'
./qconcept -a $CONCEPT2 1 'регистрировать ?что событие (?на-что изменение, ?для-чего поле).'
./qconcept -a $CONCEPT2 2 'устанавливать ?что обработчик (?чего событие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой A).\").'
./qconcept -a $CONCEPT2 3 'устанавливать ?что значение (?чего поле, ?какой "привет мир!").'
./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой A"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'печатать ?что значение ?чего (=поле ?что иметь ?что имя ?какой A).'
./qconcept -a $CONCEPT2 5 'удалять ?что событие (?на-что изменение, ?для-чего (=поле ?что иметь ?что имя ?какой A)).'
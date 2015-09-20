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
./qconcept -a $CONCEPT2 0 'создавать ?что (=поле ?что иметь ?что имя ?какой XL).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=поле ?что иметь ?что имя ?какой X).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 1, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего триггер, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой X=1).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 2, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего триггер, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой X=2).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 3, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего триггер, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой X=3).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=поле ?что иметь ?что имя ?какой Y).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 3, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего триггер, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой Y=3).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой X), ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой Y), ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "INIT[3:3]\n".'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "REFR[]\n".'

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой X=1"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой XL), ?какой "A").'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'выполнять ?что (=процедура ?что иметь ?что имя ?какой Print).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'увеличивать (?что значение ?чего (=поле ?что иметь ?что имя ?какой X), ?на-сколько 1).'

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой X=2"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой XL), ?какой "B").'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'выполнять ?что (=процедура ?что иметь ?что имя ?какой Print).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'увеличивать (?что значение ?чего (=поле ?что иметь ?что имя ?какой X), ?на-сколько 1).'

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой X=3"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой XL), ?какой "C").'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'выполнять ?что (=процедура ?что иметь ?что имя ?какой Print).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего (=поле ?что иметь ?что имя ?какой X), ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'увеличивать (?что значение ?чего (=поле ?что иметь ?что имя ?какой Y), ?на-сколько 1).'

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой Y=3"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'удалять ?что триггер (?какой "==", ?на-что значение ?какой 1, ?для-чего (=поле ?что иметь ?что имя ?какой X)).'

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой Print"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'печатать ?что значение ?какой "SET[".'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего (=поле ?что иметь ?что имя ?какой XL).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего (=поле ?что иметь ?что имя ?какой Y).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "]\n".'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "REFR[]\n".'
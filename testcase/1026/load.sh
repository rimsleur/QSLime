#! /bin/bash

EXEC_PWD=$PWD
cd ../../database
./clear_user_space.sh
cd $EXEC_PWD
cd `cat ../path`

./qconcept -c 2 'TestProcedure1'
./qconcept -c 2 'TP001'
./qconcept -c 2 'TP002'
./qconcept -c 2 'Поле1'
./qconcept -c 2 'Поле2'
./qconcept -c 2 'Поле3'
./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TestProcedure1"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'создавать ?что (=поле ?что иметь ?что имя ?какой Поле1).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего Поле1, ?какой 2).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=поле ?что иметь ?что имя ?какой Поле2).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 1, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего триггер, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой TP001).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего Поле2, ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=поле ?что иметь ?что имя ?какой Поле3).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 1, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего триггер, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой TP002).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего Поле3, ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TP001"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Триггер Поле2==1
./qconcept -a $CONCEPT2 0 'увеличивать (?что значение ?чего Поле2, ?на-сколько Поле1).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего Поле2.'; PREVLINE=`echo "$PREVLINE + 1" | bc`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TP002"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Триггер Поле3==1
./qconcept -a $CONCEPT2 0 'увеличивать (?что значение ?чего Поле3, ?на-сколько Поле2).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего Поле3.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
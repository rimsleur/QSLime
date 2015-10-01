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
./qconcept -c 2 'Список1'
./qconcept -c 2 'Список2'
./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TestProcedure1"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'создавать ?что (=поле ?что иметь ?что имя ?какой Поле1).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=список ?что иметь ?что имя ?какой Список1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'добавлять ?что элемент ?чего Список1.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 1, ?для-чего элемент (?чего Список1, ?какой 1)).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего триггер, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой TP001).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=список ?что иметь ?что имя ?какой Список2).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'добавлять ?что элемент ?чего Список2.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 2, ?для-чего элемент (?чего Список2, ?какой 1)).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего триггер, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой TP002).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего Поле1, ?какой 2).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего элемент (?чего Список1, ?какой 1), ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего элемент (?чего Список2, ?какой 1), ?какой 2).'; PREVLINE=`echo "$PREVLINE + 1" | bc`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TP001"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Триггер Список1[1]==1
./qconcept -a $CONCEPT2 0 'увеличивать (?что значение ?чего элемент (?чего Список1, ?какой 1), ?на-сколько Поле1).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего элемент (?чего Список1, ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TP002"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Триггер Список2[1]==2
./qconcept -a $CONCEPT2 0 'увеличивать (?что значение ?чего элемент (?чего Список2, ?какой 1), ?на-сколько элемент (?чего Список1, ?какой 1)).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего элемент (?чего Список2, ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
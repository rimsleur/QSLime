#! /bin/bash

EXEC_PWD=$PWD
cd ../../database
./clear_user_space.sh
cd $EXEC_PWD
cd `cat ../path`

./qconcept -c 2 'TestProcedure1'
./qconcept -c 2 'TP001'
./qconcept -c 2 'TP002'
./qconcept -c 2 'СP001'
./qconcept -c 2 'СP002'
./qconcept -c 2 'СP003'
./qconcept -c 2 'СP004'
./qconcept -c 2 'СP005'
./qconcept -c 2 'СP006'
./qconcept -c 2 'СP007'
./qconcept -c 2 'СP008'
./qconcept -c 2 'СP009'
./qconcept -c 2 'C1'
./qconcept -c 2 'C2'
./qconcept -c 2 'C3'
./qconcept -c 2 'C4'
./qconcept -c 2 'C5'
./qconcept -c 2 'C6'
./qconcept -c 2 'C7'
./qconcept -c 2 'C8'
./qconcept -c 2 'C9'
./qconcept -c 2 'SnakeLength'
./qconcept -c 2 'XList'
./qconcept -c 2 'YList'
./qconcept -c 2 'ListIterator'
./qconcept -c 2 'Direction'
./qconcept -c 2 'Temp'
./qconcept -c 2 'Print'
./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TestProcedure1"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
./qconcept -a $CONCEPT2 0 'создавать ?что (=список ?что иметь ?что имя ?какой XList).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'добавлять ?что элемент ?чего список.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего элемент, ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'добавлять ?что элемент ?чего список.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего элемент, ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'добавлять ?что элемент ?чего список.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего элемент, ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=список ?что иметь ?что имя ?какой YList).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'добавлять ?что элемент ?чего список.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего элемент, ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'добавлять ?что элемент ?чего список.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего элемент, ?какой 2).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'добавлять ?что элемент ?чего список.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего элемент, ?какой 3).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=поле ?что иметь ?что имя ?какой SnakeLength).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего поле, ?какой 3).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=поле ?что иметь ?что имя ?какой Temp).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=поле ?что иметь ?что имя ?какой ListIterator).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=условие ?что иметь ?что имя ?какой C1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего условие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой СP001).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что приоритет (?чего условие, ?какой 3).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=условие ?что иметь ?что имя ?какой C2).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего условие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой СP002).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что приоритет (?чего условие, ?какой 2).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=условие ?что иметь ?что имя ?какой C3).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего условие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой СP003).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что приоритет (?чего условие, ?какой 2).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=условие ?что иметь ?что имя ?какой C4).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего условие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой СP004).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что приоритет (?чего условие, ?какой 2).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=условие ?что иметь ?что имя ?какой C5).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего условие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой СP005).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что приоритет (?чего условие, ?какой 2).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=условие ?что иметь ?что имя ?какой C6).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего условие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой СP006).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=условие ?что иметь ?что имя ?какой C7).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего условие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой СP007).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=условие ?что иметь ?что имя ?какой C8).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего условие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой СP008).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=условие ?что иметь ?что имя ?какой C9).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего условие, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой СP009).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?на-что изменение, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "!=", ?на-что значение ?какой 3, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 1, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего триггер, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой TP001).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что приоритет (?чего триггер, ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 3, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что обработчик (?чего триггер, ?какой \"выполнять ?что (=процедура ?что иметь ?что имя ?какой TP002).\").'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что приоритет (?чего триггер, ?какой 3).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C2).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C3).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C4).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C5).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C6).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C7).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C8).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C9).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'создавать ?что (=поле ?что иметь ?что имя ?какой Direction).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 1, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C2).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C6).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 2, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C3).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C8).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 3, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C4).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C9).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 4, ?для-чего поле).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C5).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C7).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 1, ?для-чего элемент (?чего YList, ?какой 3)).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C8).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 10, ?для-чего элемент (?чего YList, ?какой 3)).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C6).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 1, ?для-чего элемент (?чего XList, ?какой 3)).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C9).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'регистрировать ?что триггер (?какой "==", ?на-что значение ?какой 10, ?для-чего элемент (?чего XList, ?какой 3)).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'присоединять (?что триггер, ?к-чему C7).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего ListIterator, ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего Direction, ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "INIT[10:10]\n".'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "SET[A1]\n".'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "SET[A2]\n".'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "SET[A3]\n".'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "REFR[]\n".'; PREVLINE=`echo "$PREVLINE + 1" | bc`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TP001"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Триггер ListIterator==1
./qconcept -a $CONCEPT2 0 'печатать ?что значение ?какой "CLR[".'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'использовать ?что элемент (?чего XList, ?какой 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'преобразовывать (?что элемент ?как-что число, ?во-что Temp ?как-что буква).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего Temp.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'использовать ?что элемент (?чего YList, ?какой ListIterator).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего элемент.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "]\n"'; PREVLINE=`echo "$PREVLINE + 1" | bc`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой TP002"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Триггер ListIterator==3
./qconcept -a $CONCEPT2 0 'устанавливать ?что значение (?чего ListIterator, ?какой 1).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "REFR[]\n"'; PREVLINE=`echo "$PREVLINE + 1" | bc`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой СP001"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Условие (ListIterator, ListIterator!=3)
./qconcept -a $CONCEPT2 0 'устанавливать ?что значение (?чего Temp, ?какой ListIterator).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'увеличивать (?что значение ?чего Temp, ?на-сколько 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'использовать ?что элемент (?чего XList, ?какой Temp).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего элемент (?чего XList, ?какой ListIterator), ?какой элемент).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'использовать ?что элемент (?чего YList, ?какой Temp).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'устанавливать ?что значение (?чего элемент (?чего YList, ?какой ListIterator), ?какой элемент).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'увеличивать (?что значение ?чего ListIterator, ?на-сколько 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой СP002"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Условие (ListIterator==3, Direction==1)
./qconcept -a $CONCEPT2 0 'использовать ?что элемент (?чего XList, ?какой ListIterator).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'преобразовывать (?что элемент ?как-что число, ?во-что Temp ?как-что буква).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'увеличивать (?что значение ?чего элемент (?чего YList, ?какой ListIterator), ?на-сколько 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "SET[".'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего Temp.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего элемент (?чего YList, ?какой ListIterator).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "]\n".'; PREVLINE=`echo "$PREVLINE + 1" | bc`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой СP003"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Условие (ListIterator==3, Direction==1)
./qconcept -a $CONCEPT2 0 'использовать ?что элемент (?чего XList, ?какой ListIterator).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'преобразовывать (?что элемент ?как-что число, ?во-что Temp ?как-что буква).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'уменьшать (?что значение ?чего элемент (?чего YList, ?какой ListIterator), ?на-сколько 1).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "SET[".'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего Temp.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего элемент (?чего YList, ?какой ListIterator).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "]\n".'; PREVLINE=`echo "$PREVLINE + 1" | bc`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой СP004"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Условие (ListIterator==3, Direction==4)
./qconcept -a $CONCEPT2 0 'уменьшать (?что значение ?чего элемент (?чего XList, ?какой ListIterator), ?на-сколько 1).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'использовать ?что элемент (?чего XList, ?какой ListIterator).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'преобразовывать (?что элемент ?как-что число, ?во-что Temp ?как-что буква).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "SET[".'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего Temp.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего элемент (?чего YList, ?какой ListIterator).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "]\n".'; PREVLINE=`echo "$PREVLINE + 1" | bc`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой СP005"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Условие (ListIterator==3, Direction==4)
./qconcept -a $CONCEPT2 0 'увеличивать (?что значение ?чего элемент (?чего XList, ?какой ListIterator), ?на-сколько 1).'; PREVLINE=`./qconcept -g`
./qconcept -a $CONCEPT2 $PREVLINE 'использовать ?что элемент (?чего XList, ?какой ListIterator).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'преобразовывать (?что элемент ?как-что число, ?во-что Temp ?как-что буква).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "SET[".'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего Temp.'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?чего элемент (?чего YList, ?какой ListIterator).'; PREVLINE=`echo "$PREVLINE + 1" | bc`
./qconcept -a $CONCEPT2 $PREVLINE 'печатать ?что значение ?какой "]\n".'; PREVLINE=`echo "$PREVLINE + 1" | bc`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой СP006"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Условие (ListIterator==3, Direction==1, Y[3]==10)
./qconcept -a $CONCEPT2 0 'устанавливать ?что значение (?чего Direction, ?какой 4).'; PREVLINE=`./qconcept -g`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой СP007"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Условие (ListIterator==3, Direction==4, X[3]==10)
./qconcept -a $CONCEPT2 0 'устанавливать ?что значение (?чего Direction, ?какой 2).'; PREVLINE=`./qconcept -g`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой СP008"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Условие (ListIterator==3, Direction==2, Y[3]==1)
./qconcept -a $CONCEPT2 0 'устанавливать ?что значение (?чего Direction, ?какой 3).'; PREVLINE=`./qconcept -g`

./qconcept -c 5
CONCEPT1=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"
./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой СP009"
./qconcept -c 7
CONCEPT2=`./qconcept -m`
./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"
# Условие (ListIterator==3, Direction==3, X[3]==1)
./qconcept -a $CONCEPT2 0 'устанавливать ?что значение (?чего Direction, ?какой 1).'; PREVLINE=`./qconcept -g`
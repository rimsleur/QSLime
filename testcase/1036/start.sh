#! /bin/bash

./../../bin/qslime-create-pipes

gnome-terminal --window --working-directory="/home/amarch/DATA/Projects/quadoadviser/git/QSLime/bin" -e "./qslime-trm" &

./../../interpreter/main.py -s "ты ?кто загружать ?что (=модуль ?что иметь ?что имя ?какой Snake)."
#! /bin/bash

cd `cat ../path`
./qlinkage -c 'что'
./qlinkage -c 'чему'
./qlinkage -c "от"
./qlinkage -c "до"
./qconcept -c 2 'число'
./qconcept -c 1 'принадлежать'
./qconcept -c 2 'диапазон'
./qconcept -c 3 '1'
./qconcept -c 3 '10'
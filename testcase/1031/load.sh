#! /bin/bash
SOURCE='Snake.qsl'

EXEC_PWD=$PWD
cd ../../database
./clear_user_space.sh
cd $EXEC_PWD
cd `cat ../path`

./qconcept -c 2 'C1'
./qconcept -c 2 'C2'
./qconcept -c 2 'C3'
./qconcept -c 2 'C4'
./qconcept -c 2 'C5'
./qconcept -c 2 'C6'
./qconcept -c 2 'C7'
./qconcept -c 2 'C8'
./qconcept -c 2 'C9'
./qconcept -c 2 'XList'
./qconcept -c 2 'YList'

cd $EXEC_PWD
SCRIPT=$SOURCE.'sh'
touch $SCRIPT
chmod +x $SCRIPT

cd ../../tools
./qlploadmodule.sh $EXEC_PWD/$SOURCE $EXEC_PWD/$SCRIPT

cd $EXEC_PWD
./$SCRIPT
rm $SCRIPT
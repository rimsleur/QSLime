#! /bin/bash
SOURCE='Snake.qsl'

EXEC_PWD=$PWD
cd ../../database
./clear_user_space.sh
cd $EXEC_PWD
cd `cat ../path`

cd $EXEC_PWD
SCRIPT=$SOURCE.'sh'
touch $SCRIPT
chmod +x $SCRIPT

cd ../../tools
./qlploadmodule.sh $EXEC_PWD/$SOURCE $EXEC_PWD/$SCRIPT

cd $EXEC_PWD
./$SCRIPT
rm $SCRIPT
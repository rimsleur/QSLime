#! /bin/bash

DIR="/tmp"

if [ ! -e $DIR/qlp-std-in ];
then mkfifo $DIR/qlp-std-in;
fi

if [ ! -e $DIR/qlp-std-out ];
then mkfifo $DIR/qlp-std-out;
fi

if [ ! -e $DIR/qlp-ctl-in ];
then mkfifo $DIR/qlp-ctl-in;
fi

if [ ! -e $DIR/qlp-ctl-out ];
then mkfifo $DIR/qlp-ctl-out;
fi

if [ ! -e $DIR/qlp-dbg-in ];
then mkfifo $DIR/qlp-dbg-in;
fi

if [ ! -e $DIR/qlp-dbg-out ];
then mkfifo $DIR/qlp-dbg-out;
fi

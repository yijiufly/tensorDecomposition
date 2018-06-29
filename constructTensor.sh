#!/bin/sh
APK_DIR="$PWD/apps/2"
DEX2JAR_DIR="$PWD/dex2jar-2.0"
DEX2JAR="$DEX2JAR_DIR/dex2jar.sh"
PARSE_DIR="$PWD/dexparser"
OUTPUT_DIR="$PWD/output"
DEX_TO_JAR_EXT="-dex2jar.jar"
HOME=$PWD

cd $APK_DIR
declare -a array=(`ls`)
cd $HOME
max=$[${#array[@]}-1]
echo $max
for k in $(seq 0 $max)
do
    apkfile=${array[$k]}
    echo analysing $apkfile ...
    cd $APK_DIR
    unzip $apkfile -d $HOME/unzip
	cd $HOME
	python $PARSE_DIR/parse.py $HOME/unzip/classes.dex >> $OUTPUT_DIR/$k
	rm -r unzip/*
done

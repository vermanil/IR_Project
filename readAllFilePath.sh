#!/bin/bash
# parentdir = ../en.docs.2011/
cd ..
cd en.docs.2011/
# pwd
flag=0
fl=0
i=0
export foo="hi"
path=()
for d in `ls`;
do 
	#var s = "../en.docs.2011/" + "$d"
	# echo $d
	if [ $flag -eq 1 ]; 
		then
		if [ $fl -eq 1 ];
		then
			cd ..
			fl=2
		fi
		cd ..
	# pwd
	fi
	flag=1
	cd $d
	for subdir in `ls`;
	do 
		# echo $subdir
		if [ $fl -eq 1 ]; 
		then
			cd ..
		fi
		fl=1
		cd $subdir
		s=`pwd`
		#echo $s
		path[$i]=$s
		# echo $s
		i=$((i+1))
	done
# echo "${path[@]}"
done	
# declare -a joined;
# joined=( $(./english_Index.py "${path[@]}" ) );
cd ..
cd ..
cd ..
cd FinalIR
python3 english_Index.py "${path[@]}"
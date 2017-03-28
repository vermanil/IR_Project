#!/bin/bash
# parentdir = ../en.docs.2011/
cd ..
cd en.docs.2011/
# pwd
flag=0
fl=0
i=0
loop=-1
export foo="hi"
path=()
for d in `ls`;
do 
	#var s = "../en.docs.2011/" + "$d"
	# echo $d
	loop=$((loop+1))
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
		if [ $fl -eq 1 ]; 
		then
			cd ..
		fi
		# echo $subdir
		# if [ -d "$subdir" ]; then
  		# Control will enter here if $DIRECTORY exists.
		fl=1
		# echo $subdir
		if [ $tele -eq 1 ]; then 
			cd ..
		fi
		tele=0
		cd $subdir
		if [ $loop -eq 1 ]; then
			for a in `ls`;
			do
				if [[ "$a" == *utf8 ]]; then
    				# echo "yes"
    				cd $a
    				for q in `ls`; 
    				do
    					cd $q
    					s=`pwd`
						path[$i]=$s
						i=$((i+1))
						cd ..
    				done
					cd ..
				else
					pwd
					# echo $a
					if [ $tele -eq 1 ]; then 
						cd ..
					fi
					tele=1
					cd $a
					s=`pwd`
					path[$i]=$s
					i=$((i+1))
				fi
			done
		else
			s=`pwd`
			path[$i]=$s
			# echo $s
			i=$((i+1))
		fi
	done
# echo "${path[@]}"
done
# echo "${path[@]}"	
# declare -a joined;
# joined=( $(./english_Index.py "${path[@]}" ) );
cd ..
cd ..
cd ..
if [ $tele -eq 1 ]; then 
	cd ..
fi
cd FinalIR
python3 english_Index.py "${path[@]}"
#!/bin/bash
if [ $# -ne 2 ]
then
	echo "usage:$0 train_data output"
	exit 1;
fi;

train_data=$1;
awk '{
	if($1!=last && last!=""){
		content=last;
		for(i in score){
			content=content"\t"i":"score[i];
		}
		print content;
		delete score;
	}
	last=$1;
	if($3==1){
		score[$2]++;
	}
}' $train_data > $2


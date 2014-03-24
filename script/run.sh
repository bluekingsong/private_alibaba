#!/bin/bash
if [ $# -ne 2 ]
then
	echo "usage:$0 train_data predict_threshold"
	exit 1;
fi;

train_data=$1;

#./train.sh $train_data $u_eps $u_buy_eps $b_eps $b_buy_eps;
#./predict.py temp/score 8.txt $6
#./recall_history.sh $train_data temp/score
./make_matrix.sh $train_data mat
awk '{
	if(ARGV[1]==FILENAME){
		content=content==""?$1" 1" : content"\t"$1" 1";
	}else{
		print $1"\t"content;
	}
}' mat.brand mat.user > temp/score

./predict.py temp/score 8.txt 0


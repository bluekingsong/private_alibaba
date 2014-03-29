#!/bin/bash
if [ $# -ne 1 ]
then
	echo "usage:$0 train_data"
	exit 1;
fi;
userfile="data/all.user";
itemfile="data/all.brand";
if [ ! -f $userfile ] || [ ! -f $itemfile ]
then
	echo $userfile" or "$itemfile" don't exist.";
	exit 1;
fi;
train_data=$1;
awk -v recordCnt="$records" '{
	if(FILENAME==ARGV[1]){
		users[$1];
	}else if(FILENAME==ARGV[2]){
		items[$1];
	}else{
		if($1!=last && last!=""){
			content=last;
			recalls=0;
			for(i in score){
				recalls++;
				content=content"\t"i":"score[i];
			}
			if(recalls>0)
				print content > "/tmp/score_history";
			delete score;
			#delete month;
			#delete last_month;
		}
		last=$1;
		if($3>=1){
			score[$2]++;
#			if(last_month[$3]!=$4){
#				month[$2]++;
#				last_month[$2]=$4;
#			}
		}
	}
}END{
	#print "maxium buy brands:"maxBuy;
}' $userfile $itemfile $train_data  #> "/tmp/score_history";
echo "score file is /tmp/score_history";
head /tmp/score_history


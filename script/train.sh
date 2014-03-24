#!/bin/bash
if [ $# -ne 5 ]
then
	echo "usage:$0 train_data user_eps user_buy_eps brand_eps brand_buy_eps"
	exit 1;
fi;

train_data=$1;
u_eps=$2;
u_buy_eps=$3;
b_eps=$4;
b_buy_eps=$5;

awk '{ user[$1]; cnt[$1" "$3]++;}END{ for(u in user)print u"\t"cnt[u" "0]+0"\t"cnt[u" "1]+0"\t"cnt[u" "2]+0"\t"cnt[u" "3]+0"\t"0+cnt[u" "0]+cnt[u" "1]+cnt[u" "2]+cnt[u" "3] }' $train_data > "temp/user.cnt";
awk '{ user[$2]; cnt[$2" "$3]++;}END{ for(u in user)print u"\t"cnt[u" "0]+0"\t"cnt[u" "1]+0"\t"cnt[u" "2]+0"\t"cnt[u" "3]+0"\t"0+cnt[u" "0]+cnt[u" "1]+cnt[u" "2]+cnt[u" "3] }' $train_data > "temp/brand.cnt";

awk -v b_eps="$b_eps" -v b_buy_eps="$b_buy_eps" -v u_eps="$u_eps" -v u_buy_eps="$u_buy_eps"  '{
	if(FILENAME==ARGV[1]){
		if($6<b_eps || $3<b_buy_eps) next;
		brand[$1" "0]=($3+1)/($2+1);
		brand[$1" "2]=($3+1)/($4+1);
		brand[$1" "3]=($3+1)/($5+1);
		brand_dict[$1];
	}else if(FILENAME==ARGV[2]){
		if($6<u_eps || $3<u_buy_eps) next;
		users[$1];
	}else if(FILENAME==ARGV[3]){
		if(!($1 in users) || !($2 in brand_dict)) next;
		if($1!=last && last!=""){
			content=last;
			for(i in score){
				content=content"\t"i":"score[i];
			}
			print content;
			delete score;
		}
		last=$1;
		score[$2]+=brand[$2" "$3];
	}
}' "temp/brand.cnt" "temp/user.cnt" $train_data > "temp/score";



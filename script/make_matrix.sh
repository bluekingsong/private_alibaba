#!/bin/bash
if [ $# -ne 5 ]
then
	echo "usage:$0 train_data output [user_buy_eps brand_eps brand_buy_eps]"
	if [ $# -eq 2 ]
	then
		u_buy_eps=1;
		b_eps=4;
		b_buy_eps=1;
	else
		exit 1;
	fi;
fi;
train_data=$1;
output=$2;
if [ $# -eq 5 ]
then
	u_buy_eps=$3;
	b_eps=$4;  ## click eps
	b_buy_eps=$5;
fi;
awk '{ user[$1]; cnt[$1" "$3]++;}END{ for(u in user)print u"\t"cnt[u" "0]+0"\t"cnt[u" "1]+0"\t"cnt[u" "2]+0"\t"cnt[u" "3]+0"\t"0+cnt[u" "0]+cnt[u" "1]+cnt[u" "2]+cnt[u" "3] }' $train_data > "temp/user.cnt";
awk '{ user[$2]; cnt[$2" "$3]++;}END{ for(u in user)print u"\t"cnt[u" "0]+0"\t"cnt[u" "1]+0"\t"cnt[u" "2]+0"\t"cnt[u" "3]+0"\t"0+cnt[u" "0]+cnt[u" "1]+cnt[u" "2]+cnt[u" "3] }' $train_data > "temp/brand.cnt";

awk -v b_eps="$b_eps" -v b_buy_eps="$b_buy_eps" -v u_buy_eps="$u_buy_eps" '{
	if(FILENAME==ARGV[1]){
		if($2<b_eps || $3<b_buy_eps) next;
		brands[$1]=$3/$2;      ### buy-num/click-num
	}else if(FILENAME==ARGV[2]){
		if($3<u_buy_eps) next;
		users[$1];
	}else if(FILENAME==ARGV[3]){
		if(!($1 in users) || !($2 in brands)) next;
		if($1!=last && last!=""){
			content=last;
			for(i in score){
				content=content"\t"i" "score[i];
			}
			print content;
			delete score;
		}
		last=$1;
		if($3==0)	score[$2]+=brands[$2];
		else if($3==1)	score[$2]++;
	}
}' "temp/brand.cnt" "temp/user.cnt" $train_data > $output;
cut -f1 ${output} > ${output}.user;
awk '{ for(i=2;i<=NF;i+=2) print $i }' ${output} | sort -nu > ${output}.brand
wc -l ${output}* temp/*.cnt

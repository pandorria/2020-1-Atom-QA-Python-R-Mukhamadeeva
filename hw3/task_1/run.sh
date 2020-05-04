#!/bin/bash

get_total_requests(){
	echo "" >> $RESULT
	echo "Total Requests:" >> $RESULT
	wc -l $LOGFILE | awk '{ print $1 }' >> $RESULT
	echo "" >> $RESULT
}

get_request_methods(){
	echo "Total Request Methods:" >> $RESULT
	cat $LOGFILE \
	| awk '{gsub ("\"", ""); print $6}' \
	| sort \
	| uniq -c \
	| awk '{print $1, $2}' >> $RESULT
	echo "" >> $RESULT
}

get_top_lagre_request(){
	echo "" >> $RESULT
	echo "Top 10 Lagest Requests:" >> $RESULT
	cat $LOGFILE \
	| awk '{print $10, $7, $9}' \
	| sort -k1 -rn \
	| head >> $RESULT
	echo "" >> $RESULT
}


get_client_error(){
	echo "" >> $RESULT
	echo "Top 10 Client Error:" >> $RESULT
	cat $LOGFILE \
	| awk '{print $10, $7, $9}' \
	| sort -k1 -rn \
	| head >> $RESULT
	echo "" >> $RESULT
}

get_top_client_error(){
	echo "" >> $RESULT
	echo "Top 10 Client Errors:" >> $RESULT
	cat $LOGFILE \
	| awk '{print $1, $7, $9}'\
	| awk '{if ($3 ~ /4[0-9][0-9]/) print}'\
	| head >> $RESULT
	echo "" >> $RESULT
}

get_top_redirect_request(){
	echo "" >> $RESULT
	echo "Top 10 Redirect Requests:" >> $RESULT
	cat $LOGFILE \
	| awk '{print $1, $7, $9}'\
	| awk '{if ($3 ~ /3[0-9][0-9]/) print}'\
	| head >> $RESULT
	echo "" >> $RESULT
}

if test "$#" -eq 2; then
	args=("$@")
	LOGFILE=${args[0]} 
	RESULT=${args[1]} 
	get_total_requests
	get_request_methods
	get_top_lagre_request
	get_top_client_error
	get_top_redirect_request
fi
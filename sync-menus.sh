#!/bin/bash
for i in {0..13}
do
	curl --location --request POST 'ec2-44-213-37-146.compute-1.amazonaws.com:8000/fetch_menus/'$(date +%Y/%m/%d --date='today + '$i' day')/ --header 'Authorization: Token d93a56351342bbae35dfa3e2e443bcc61debdd8e'
done

#!/bin/bash
for i in {0..13}
do
	curl --location --request POST 'ec2-44-213-37-146.compute-1.amazonaws.com:8000/fetch_menus/'$(date +%Y/%m/%d --date='today + '$i' day')/ --header 'API-AUTH bf58eb3654743918c78f2e83af33a643e45e2fdf'
done

#!/usr/bin/env bash

folder=$(echo $0 | cut -c-31)

cd $folder
python web_scrape.py $1
python tweet.py $1

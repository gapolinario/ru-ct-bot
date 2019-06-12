#!/usr/bin/env bash

folder=$(less .folder)

cd $folder
python web_scrape.py $1

# add command for tweet

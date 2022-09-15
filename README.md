# vt_crawler
###
Simple crawling app in Python

## How does it work?
It is a simple web crawler so it goes through to any webpage you input and then goes to any other link it will find there.
It has built-in timeout a pages limit so it won’t run forever or overwhelm the server. 

## How can I run it
This app uses (almost) native Python, so you need to have it installed. Then it needs a few simple libraries (time, sys, requests)
Then you can just run it like python vt_crawler and you will find out everything else you need :)

## Limitation and Ideas
One of the big limitations is if there are any links outside the anchor HTML tag, Crawler won’t recognize it. 
Also if the Links is not a proper URL, Crawler won’t crawl it, but the list of the pages are already recognized 
so the first improvement I would do is use this link and connect them with the current crawled page like “/next” will do “mypage.com/next”. 

Another thing I would do is save the result to some txt file or even better to a database.
Another improvement is a kind of async timeout, so there will be a timeout for each server and not a general one. 
In that case if the crawler hits a timeout on one server it crawls another and the other one left for later.


# Multi-threaded Web Scraping Indeed.com for Most-Wanted Data Science Skills
## Introduction
This is a multi-threaded web scraper of Indeed.com that scrapes data science job Ads for user pre-defined location (for example, Pittsburgh, PA).
And it finally provides a bar chart of most-wanted data science skills in job market in that location.
* The program is written in Python 3.
* Single-threaded scraping program, which is my first version of this scraper, is also provided.
* Multi-threaded scraper is faster in speed than single-threaded scraper by 862.79% for the following Pittsburgh case.

## Visualization and Results
![pittsburgh_081316](https://cloud.githubusercontent.com/assets/19921232/17683707/4b2973f4-630a-11e6-95c4-d3284e251dd4.png)

* These results were run on August 12, 2016.

## Installation and Usages
Here is an example to run the application against Seattle WA

`python3 run_scraper.py --city Seattle --state WA`



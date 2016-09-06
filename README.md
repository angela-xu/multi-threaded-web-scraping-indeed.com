# Multi-threaded Web Scraping indeed.com for Most-Wanted Data Science Skills
## Introduction
This is a multi-threaded web scraper to scrape data science job Ads for user pre-defined location (e.g. Seattle, WA) on indeed.com to gain insights of the most-wanted data science skills in the job market. At the end of scraping, it will provide the user with the total number of job Ads scraped, a sorted list of most-wanted data science skills (each with its number and percentage of apearing in job Ads), and a bar chart for visualization.
* This application is written in Python 3.
* For Pittsburgh case (100+ jobs), this multi-threaded scraper is 862.79% faster than a single-threaded one. 
* For Seattle case (1100+ jobs), this multi-threaded version has reduced the running time from a 12 hours to 20 minutes.

## Visualization and Results
### Seattle
![seattle_09_05_2016](https://cloud.githubusercontent.com/assets/19921232/18264212/d724addc-73c3-11e6-8d2e-fcd7178309a8.png)
* Date: 09-05-2016
* City: Seattle, WA
* Number of Jobs Scraped: 1181
* Run Time: 1176.9583258628845 seconds

### San Francisco
![san francisco_09_05_2016](https://cloud.githubusercontent.com/assets/19921232/18263977/45c1fb02-73c2-11e6-9357-2ae77748b8fc.png) 
* Date: 09-05-2016    
* City: San Francisco, CA
* Number of Jobs Scraped: 1878
* Run Time: 2133.5088317394257 seconds

### San Jose
![san jose_09_05_2016](https://cloud.githubusercontent.com/assets/19921232/18263203/040e7afa-73bd-11e6-84c6-d78aff00adda.png)
* Date: 09-05-2016
* City: San Jose, CA
* Number of Jobs Scraped: 1567
* Run Time: 1054.757504940033 seconds

### Los Angeles
![los angeles_09_05_2016](https://cloud.githubusercontent.com/assets/19921232/18263198/f44d1a4a-73bc-11e6-87d1-133c43a0c6aa.png)
* Date: 09-05-2016
* City: Los Angeles, CA
* Number of Jobs Scraped: 524
* Run Time: 265.3683178424835 seconds

### San Diego
![san diego_09_05_2016](https://cloud.githubusercontent.com/assets/19921232/18263200/fd22329a-73bc-11e6-8e4d-c4241523d8f1.png)
* Date: 09-05-2016
* City: San Diego, CA
* Number of Jobs Scraped: 476
* Run Time: 319.94061756134033 seconds

### New York City
![new york_09_06_2016](https://cloud.githubusercontent.com/assets/19921232/18264990/3c5f3984-73c8-11e6-80f5-9be0ac2501b7.png)
* Date: 09-06-2016
* City: New York, NY
* Number of Jobs Scraped: 2338
* Run Time: 1950.0931429862976 seconds

### Washington, D.C.
![washington_dc_09_05_2016](https://cloud.githubusercontent.com/assets/19921232/18263205/094a2d84-73bd-11e6-903f-255c03dbb9ee.png)
* Date: 09-05-2016
* City: Washington, DC
* Number of Jobs Scraped: 1753
* Run Time: 986.4153757095337 seconds

### Boston
![boston_09_06_2016](https://cloud.githubusercontent.com/assets/19921232/18287970/3e987308-742e-11e6-8023-25f792e2513d.png)
Date: 09-06-2016
City: Boston, MA
Number of Jobs Scraped: 1678
Run Time: 1501.2796454429626 seconds

### Chicago
![chicago_09_05_2016](https://cloud.githubusercontent.com/assets/19921232/18263183/dac6bf68-73bc-11e6-9756-5dbfc1cdf47b.png)
* Date: 09-05-2016
* City: Chicago, IL
* Number of Jobs Scraped: 466
* Run Time: 320.2699830532074 seconds

### Charlotte
![charlotte_09_05_2016](https://cloud.githubusercontent.com/assets/19921232/18263178/d3d6b596-73bc-11e6-8ed4-06ef7f6d882c.png)
* Date: 09-05-2016
* City: Charlotte, NC
* Number of Jobs Scraped: 117
* Run Time: 119.16461515426636 seconds

### Houston
![houston_09_05_2016](https://cloud.githubusercontent.com/assets/19921232/18263185/e231f33a-73bc-11e6-8b8e-b2d08582f420.png)
* Date: 09-05-2016
* City: Houston, TX
* Number of Jobs Scraped: 174
* Run Time: 196.04837822914124 seconds

## Installation and Usages
* Download all files and folder in this repository and save them in the same folder.
* Run run_scraper.py in Python3 with a city/state name.
* An example to run the application against Seattle WA: `python3 run_scraper.py --city Seattle --state WA`

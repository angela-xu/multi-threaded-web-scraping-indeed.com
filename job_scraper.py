###############################################################################################
#  
# Job Ads Scraper - Multi-threaded Scraping
#
# Author: Huanzhu Xu
###############################################################################################


import requests
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from collections import Counter
from threading import Thread
import queue
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import sys

# Total size of job ad web pages in bytes
total_size = 0

def make_soup(html):
    '''
    This function takes an HTML object as argument,
    and returns a Beautiful Soup object.

    html: HTML object
    return: Beautiful Soup object
    '''
    soup = BeautifulSoup(html, 'lxml')
    # In case lxml does not work
    if len(soup) == 0:
        soup = BeautifulSoup(html, 'html5lib')
    return soup


def get_job_info(url):
    '''
    This function takes a URL of one job ad as argument,
    cleans up the raw HTMl and returns a one-dimensional list
    that contains a set of words appearing in this job ad.
    e.g. url = 'https://us-amazon.icims.com/jobs/423819'

    url: string, a URL
    return: list, a one-dimensional list that contains a set of words
    '''
    try:
        html = requests.get(url).text
        global total_size
        total_size += sys.getsizeof(html)
        #print('Scraping ' + url + ' Size ' + str(sys.getsizeof(html)))
    except Exception as e:
        # In case of connection problems 
        print(str(e))
        return    

    soup = make_soup(html)

    for script in soup(['script', 'style']):
        # Remove these two elements from soup
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split(' '))

    # Fix spacing issue
    def chunk_space(chunk):
        chunk = chunk + ' '
        return chunk

    # Get rid of all blank lines and ends of line
    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8')    

    try:
        text = text.decode('unicode_escape').encode('ascii', 'ignore')
    except:
        # As some websites are not formatted in a way that this works
        return

    text = re.sub('[^a-zA-Z.+3]', ' ', str(text))    # Get rid of any skils that are not words
    text = text.lower().split()    # Convert to lower case and split them apart
    stop_words = set(stopwords.words('english'))    # Filter out any stop words
    text = [w for w in text if not w in stop_words]
    text = list(set(text))    # Get the set of words

    return text    # One-dimensional list


def get_indeed_page_info(url, page_num):
    '''
    This function takes a URL and a page number as arguments,
    combines them into a new URL for search, and returns a two-dimensional list,
    where each value of the list is a one-dimensional list that contains a set of words 
    appearing in one job ad of this page.

    url: string, a base indeed.com URL before the page number, e.g. 'http://www.indeed.com/jobs?q=data+scientist&l=Seattle%2C+WA'
    page_num: int, a page number
    return: list, a two-dimensional list where each value of the list is a one-dimensional list
    '''
    base_url = 'http://www.indeed.com'
    page_job_descriptions = []

    start_num = str(page_num * 10)
    page_url = ''.join([url, '&start=', start_num])

    print('Getting page: ' + page_url)
    html_page = requests.get(page_url).text
    page_soup = make_soup(html_page)

    # The center column on the page where job ads exist
    results_column = page_soup.find(id = 'resultsCol')    

    if results_column == None:
        print('Cannot find "resultsCol" for: ' + page_url)
        with open('output/failed_to_parse_page.txt', 'a') as text_file:
            text_file.write('\n')
            text_file.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
            text_file.write(page_url + '\n')
            text_file.write(html_page + '\n')
        return page_job_descriptions

    # Get the URLs for the jobs
    job_urls = [base_url + link.get('href') for link in results_column.find_all('a', href=True)]   
    # Only get the job related URLs
    job_urls = [x for x in job_urls if 'clk' in x] 
    #for x in job_urls: 
    #    print(x)

    for i in range(len(job_urls)):
        description = get_job_info(job_urls[i])
        if description:    # Only append when the website was accessed correctly
            page_job_descriptions.append(description)

    print('Page ' + str(page_num) + ' done with collecting job descriptions' )

    return page_job_descriptions    # Two-dimensional list


def get_indeed_page_info_by_range(url, page_range):
    '''
    This function takes a URL and a range of page numbers as arguments,
    and returns a three-dimensional list where each value of the list is 
    a two-dimensional list that contains the job descriptions of one page.

    url: string, a URL
    page_range: list, a list of a range of numbers
    return: list, a three-dimensional list
    '''
    results = []
    for i in page_range:
        results.append(get_indeed_page_info(url, i)) 
    return results    # Three-dimensional list


def work(url, page_range, queue):
    '''
    This function is executed by worker thread in multi-threading mode.
    It takes a URL, a list of a range of page numbers, and a queue as arguments,
    and puts its results into the queue.

    url: string, a URL
    page_range: list, a list of a range of numbers
    queue: queue, a thread-safe queue
    '''
    result = get_indeed_page_info_by_range(url, page_range)
    queue.put(result)


def process_url(num_pages, url):
    '''
    This function is the main thread in multi-threading mode.
    It takes the the number of total pages of job ads and a URL as arguments,
    combines the results of worker threads and returns a four-dimensional list
    that contains the results.

    num_pages: int, number of total pages of job ads
    url: string, a URL
    return: list, a four-dimensioanl list that contains the results of worker threads
    '''
    # Set the maximum number of threads to be 20
    if num_pages < 20:
        num_threads = num_pages
    else:
        num_threads = 20 
    print('Using {} worker threads'.format(num_threads))

    page_group = int(num_pages / num_threads)
    q = queue.Queue()
    threads = [None] * num_threads

    for i in range(0, num_threads):
        page_range = range(page_group * i, page_group * (i + 1))
        t = Thread(target=work, args=(url, page_range, q))
        t.start()
        threads[i] = t
        time.sleep(1)    # Sleep between worker threads

    for i in range(0, num_threads):
        threads[i].join()
        print('Thread {} joined'.format(i))
    print("All threads finished")

    return [q.get() for _ in range(num_threads)]   # Four-dimensional list


def run_scraper(city=None, state=None, job='data+scientist'):
    '''
    This function takes a city/state and a job title as arguments 
    and looks for all job ads on Indeed.com with specified city/state and job title. 
    It crawls all of the job ads and keeps track of how many use a preset list of skills. 

    It returns the number of total job ads successfullt scraped, a dataframe
    that contains information about each skill with its number and percentage
    of appearing in job ads, and a bar chart displaying the percentage for each skill.

    city/state: string, city/state of interest, for example, run_scraper('Seattle', 'WA').
                Use a two letter abbreviation for the state.
                City and state must be specified together, or be omitted together.
                If city and state are omitted, the function will assume a national search.

    return: 1) the number of total job ads successfully scraped
            2) a Pandas dataframe that contains information about each preset skill 
               with its number and percentage of appearing in job ads
            3) a bar chart for visualization
    '''
    city_copy = city[:]

    if city is not None:
        # For city name like 'San Francisco', we want to convert it into 'San+Francisco'
        city_list = city.split()  
        city = '+'.join(city_list)
        url_list = ['http://www.indeed.com/jobs?q=', job, '&l=', city, '%2C+', state]
    else:
        url_list = ['http://www.indeed.com/jobs?q=', job]

    url = ''.join(url_list)    # URL for job search
    print("Using URL " + url)

    try:
        html = requests.get(url).text
    except:
        print('The location ' + city_copy + ', ' + state + ' could not be found.')
        return

    soup = make_soup(html)

    num = soup.find(id = 'searchCount')
    if num == None:
        num = soup.find(id = 'searchCount') 
    num_jobs = num.string.encode('utf-8')

    # Total number of jobs found
    job_numbers = re.findall('\d+', str(num_jobs))  

    # Process commas in large number representations
    if len(job_numbers) > 3:
        total_num_jobs = (int(job_numbers[2]) * 1000) + int(job_numbers[3])
    else:
        total_num_jobs = int(job_numbers[2])

    if city is None:
        print(str(total_num_jobs) + ' jobs found nationwide')
    print(str(total_num_jobs) + ' jobs found in ' + city_copy + ', ' + state)

    num_pages = int(total_num_jobs / 10)

    #
    ### Multi-threading
    #

    total_job_descriptions = process_url(num_pages, url)    # Four-dimensional list
    # Convert four-dimensional list into two-dimensional list
    total_job_descriptions = sum(sum(total_job_descriptions, []), []) 
    total_jobs_found = len(total_job_descriptions)

    print('Done with collecting the job ads!')
    print('There were ' + str(total_jobs_found) + ' jobs successfully found.')

    #
    ### Calculating the number and percentage of job ads having a certain skill
    #

    doc_frequency = Counter()
    [doc_frequency.update(item) for item in total_job_descriptions]

    language_dict = Counter({'Python': doc_frequency['python'], 'R': doc_frequency['r'],
                             'Java': doc_frequency['java'], 'C++': doc_frequency['c++'],
                             'Ruby': doc_frequency['ruby'], 'Perl': doc_frequency['perl'],
                             'MATLAB': doc_frequency['matlab'],'JavaScript': doc_frequency['javascript'],
                             'Scala': doc_frequency['scala'], 'C#': doc_frequency['c#'],
                             'PHP': doc_frequency['php'], 'HTML': doc_frequency['html'],
                             'SAS': doc_frequency['sas'], 'Julia': doc_frequency['julia']})

    tool_dict = Counter({'Excel': doc_frequency['excel'], 'Tableau': doc_frequency['tableau'],
                         'D3.js': doc_frequency['d3.js'], 'LaTex': doc_frequency['latex'],
                         'SPSS': doc_frequency['spss'], 'D3': doc_frequency['d3'],
                         'STATA': doc_frequency['stata']})

    big_data_dict = Counter({'Hadoop': doc_frequency['hadoop'], 'MapReduce': doc_frequency['mapreduce'],
                             'Spark': doc_frequency['spark'], 'Pig': doc_frequency['pig'],
                             'Hive': doc_frequency['hive'], 'Shark': doc_frequency['shark'],
                             'Oozie': doc_frequency['oozie'], 'ZooKeeper': doc_frequency['zookeeper'],
                             'Flume': doc_frequency['flume'], 'Mahout': doc_frequency['mahout']})

    database_dict = Counter({'SQL': doc_frequency['sql'], 'NoSQL': doc_frequency['nosql'],
                             'HBase': doc_frequency['hbase'], 'Cassandra': doc_frequency['cassandra'],
                             'MongoDB': doc_frequency['mongodb']})

    total_skills = language_dict + tool_dict + big_data_dict + database_dict

    # Convert results into a dataframe
    df = pd.DataFrame(list(total_skills.items()), columns = ['Skill', 'NumAds'])
    # Percentage of job ads having a certain skill
    df['Percentage'] = df.NumAds / total_jobs_found * 100.0 
    # Sort data for plotting
    df.sort_values(by='Percentage', ascending=True, inplace=True)
    pd.set_option('display.width', 1000)
    #
    ### Visualization
    #

    plot = df.plot(x='Skill', y='Percentage', kind='barh', legend=False, color='skyblue', 
                   title='Percentage of Data Scientist Job Ads with a Key Skill, ' + city_copy)
    plot.set_xlabel('Percentage Appearing in Job Ads')
    # Convert the pandas plot object to a matplotlib object
    fig = plot.get_figure()
    plt.tight_layout()

    return (total_jobs_found, total_size, df, fig)



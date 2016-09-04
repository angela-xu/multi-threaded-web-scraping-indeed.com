import requests
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from collections import Counter
from threading import Thread
import queue
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors


def make_soup(html):
    '''
    This function takes an HTML object as argument, 
    and returns a Beautiful Soup object.

    html: HTML object
    return: soup object 
    '''
    soup = BeautifulSoup(html, 'lxml')
    if len(soup) == 0:
        soup = BeautifulSoup(html, 'html5lib')    # In case lxml does not work
    return soup


def get_job_info(url):
    '''
    This function takes an URL of one single job Ad as argument,
    cleans up the raw HTMl and returns a set of words of the job Ad.

    url: string, an URL
    return: list, a set of words
    '''
    try:
        html = requests.get(url).text
    except:
        return    # In case of connection problems
   
    soup = make_soup(html)

    for script in soup(['script', 'style']):
        script.extract()    # Remove these two elements from soup

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split(' '))    # Break multi-headlines into a line each

    def chunk_space(chunk):
        chunk_out = chunk + ' '    # Fix spacing issue
        return chunk_out

    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8')    # Get rid of all blank lines and ends of line
    
    try:
        text = text.decode('unicode_escape').encode('ascii', 'ignore')
    except:
        return    # As some websites are not formatted in a way that this works
    
    text = re.sub('[^a-zA-Z.+3]', ' ', str(text))    # Get rid of any skils that are not words
    text = text.lower().split()    # Convert to lower case and split them apart
    stop_words = set(stopwords.words('english'))    # Filter out any stop words
    text = [w for w in text if not w in stop_words] 
    text = list(set(text))    # Get the set of words

    return text


def get_page_info(url, page_num):
    '''
    This function takes a URL and a page number as arguments,
    combines them into a new URL for search, and returns a list of lists
    where each list element contains a set of words of one job Ad on that page. 

    url: string, the base URL before the page number
    page_num: int, a page number
    return: list, a list of lists, each list element contains a set of words 
    '''
    print('Getting page ' + str(page_num))
    start_num = str(page_num * 10) 
    current_page = ''.join([url, '&start=', start_num])  

    html_page = requests.get(current_page).text 
    page_soup = make_soup(html_page)

    base_url = 'http://www.indeed.com'
    job_link_area = page_soup.find(id = 'resultsCol')    # The center column on the page where job Ads exist
    job_urls = [base_url + link.get('href') for link in job_link_area.find_all('a', href=True)]    # Get the URLs for the jobs
    job_urls = [x for x in job_urls if 'clk' in x]    # Get only the job related URLs

    page_job_descriptions = []

    for i in range(len(job_urls)):
        description = get_job_info(job_urls[i])
        if description:    # Only append when the website was accessed correctly
            page_job_descriptions.append(description)
        time.sleep(1)    # Sleep between connection requests

    return page_job_descriptions


def get_skill_info(city=None, state=None):
    '''
    This function takes a desired city/state as argument and looks for all new job Ads 
    on Indeed.com with specified city/state. It crawls all of the job Ads and keeps track of 
    how many use a preset list of typical data science skills. It finally returns a bar chart 
    displaying the percentage for each skill at the end of collation.

    city/state: string, city/state of interest, for example, get_skill_info('Seattle', 'WA').
                Use a two letter abbreviation for the state. 
                City and state must be specified together, or be omitted together. 
                If city and state are omitted, the function will assume a national search.

    return: a bar chart showing the most commonly desired skills in the job market for a data scientist
    '''
    job = 'data+scientist'
    city_copy = city[:]

    if city is not None:
        city = city.split()
        city = '+'.join(word for word in city)
        url_list = ['http://www.indeed.com/jobs?q=', job, '&l=', city, '%2C+', state]
    else:
        url_list = ['http://www.indeed.com/jobs?q=', job]

    url = ''.join(url_list)    # URL for job search

    try:
        html = requests.get(url).text
    except:
        'The location ' + city_copy + ', ' + state + ' could not be found.'
        return

    soup = make_soup(html)
    
    num_jobs_area = soup.find(id = 'searchCount').string.encode('utf-8')
    job_numbers = re.findall('\d+', str(num_jobs_area))    # Total number of jobs found

    if len(job_numbers) > 3:
        total_num_jobs = (int(job_numbers[2]) * 1000) + int(job_numbers[3])
    else:
        total_num_jobs = int(job_numbers[2])

    if city is None:
        print(str(total_num_jobs) + ' jobs found nationwide')
    print(str(total_num_jobs) + ' jobs found in ' + city_copy + ', ' + state) 

    num_pages = total_num_jobs / 10 

    def work(url, page_num, queue):
        result = get_page_info(url, page_num)
        queue.put(result)

    def combine_results(num_pages, url):
        arguments = range(1, int(num_pages+1))
        q = queue.Queue()
        threads = []
    
        for argument in arguments:
            t = Thread(target=work, args=(url, argument, q)) 
            t.start()
            threads.append(t)
            time.sleep(1)

        for t in threads:
            t.join()
    
        return [q.get() for _ in range(len(arguments))]

    total_job_descriptions = combine_results(num_pages, url)
    total_job_descriptions = sum(total_job_descriptions, [])

    print('Done with collecting the job Ads!')
    print('There were ' + str(len(total_job_descriptions)) + ' jobs successfully found.')

    doc_frequency = Counter()    # Create a full counter of skills
    [doc_frequency.update(item) for item in total_job_descriptions]

    language_dict = Counter({'Python': doc_frequency['python'], 'R': doc_frequency['r'],
                             'Java': doc_frequency['java'], 'C++': doc_frequency['c++'],
                             'Ruby': doc_frequency['ruby'], 'Perl': doc_frequency['perl'],
                             'MATLAB': doc_frequency['matlab'],'JavaScript': doc_frequency['javascript'],
                             'Scala': doc_frequency['scala'], 'C': doc_frequency['c'],
                             'C#': doc_frequency['c#'], 'PHP': doc_frequency['php'],
                             'HTML': doc_frequency['html'], 'SAS': doc_frequency['sas'],
                             'Julia': doc_frequency['julia']})

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

    df = pd.DataFrame(list(total_skills.items()), columns = ['Skill', 'NumAds'])    # Convert skils into a dataframe
    df.NumAds = (df.NumAds) * 100 / len(total_job_descriptions)    # Percentage of job Ads having that skill
    df.sort_values(by='NumAds', ascending=True, inplace=True)    # Sort data for plottiing

    plot = df.plot(x='Skill', kind='barh', legend=False, color='skyblue', title='Percentage of Data Scientist Job Ads with a Key Skill, ' + city_copy)
    plot.set_xlabel('Percentage Appearing in Job Ads')
    fig = plot.get_figure()    # Convert the pandas plot object to a matplotlib object
    plt.tight_layout()

    return fig, df



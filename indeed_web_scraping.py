import requests # Website connections
from bs4 import BeautifulSoup # HTML parsing
import re # Regular experssions
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter # Keep track of our skil counts
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
import pandas as pd # For converting results to a dataframe and bar chart plots
import matplotlib.pyplot as plt # For visualizations of results
import matplotlib.colors as colors # For visualizations of results



def make_soup(html):
    soup = BeautifulSoup(html, 'lxml') # Make soup object
    if len(soup) == 0: # If the default parser lxml does not work, try another one
        soup = BeautifulSoup(html, 'html5lib')
    return soup


def get_job_info(url):
    '''
    This function takes an URL of job posting as argument,
    cleans up the raw HTMl and returns a set of words of the job posting.

    url: string, an URL

    return: list, a set of words
    '''
    try:
        html = requests.get(url).text # Connect to the job posting
    except:
        return # In case the website is no longer there or some other weird connection problem
   
    soup = make_soup(html)

    for script in soup(['script', 'style']):
        script.extract() # Remove these two elements from BS4 object

    text = soup.get_text() # Get the text from soup object
    lines = (line.strip() for line in text.splitlines()) # Break into lines
    chunks = (phrase.strip() for line in lines for phrase in line.split(' ')) # Break multi-headlines into a line each

    def chunk_space(chunk):
        chunk_out = chunk + ' ' # To fix spacing issue
        return chunk_out

    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8') # Get rid of all blank lines and ends of line
    
    try:
        text = text.decode('unicode_escape').encode('ascii', 'ignore')
    except:
        return # As some websites are not formatted in a way that this works

    
    text = re.sub('[^a-zA-Z.+3]', ' ', str(text)) # Get rid of any skils that are not words
    text = text.lower().split() # Convert to lower case and split them apart
    stop_words = set(stopwords.words('english')) # Filter out any stop words
    text = [w for w in text if not w in stop_words] 
    text = list(set(text)) # Get the set of words

    return text


# test case
# url = 'https://www.dice.com/jobs/detail/10200946b/652232?&rx_medium=cpc&CMPID=AG_IN_PD_JS_AV_OG_RC_&utm_campaign=Advocacy_Ongoing&utm_medium=Aggregator&utm_source=Indeed&rx_campaign=indeed21&rx_group=100952&rx_job=10200946b%2F652232&rx_source=Indeed'
# test = get_job_info(url)
# print(test)


def get_skill_info(city=None, state=None):
    '''
    This function takes a desired city/state as argument and looks for all new job postings 
    on Indeed.com with specified city/state. It crawls all of the job positngs and keeps track of 
    how many use a preset list of typical data science skills. It finally returns a bar chart 
    displaying the percentage for each skill at the end of collation.

    city/state: string, city/state of interest, for example, get_skill_info('Seattle', 'WA').
                Use a two letter abbreviation for the state. 
                City and state must be specified together, or be omitted together. 
                If city and state are omitted, the function will assume a national search.

    return: a bar chart showing the most commonly desired skills in the job market for a data scientist
    '''
    job = 'data+scientist' # Searching for data scientist exact fit ('data scientist' on Indeed search)
    base_url = 'http://www.indeed.com'
    city_copy = city[:]

    # Make sure the city specified works properly if it has more than one word (for example: San Francisco)
    if city is not None:
        city = city.split()
        city = '+'.join(word for word in city)
        url_list = ['http://www.indeed.com/jobs?q=', job, '&l=', city, '%2C+', state]
    else:
        url_list = ['http://www.indeed.com/jobs?q=', job]

    url = ''.join(url_list) # URL for job search

    try:
        html = requests.get(url).text
    except:
        'The location ' + city_copy + ', ' + state + ' could not be found.'
        return

    soup = make_soup(html)
    
    num_jobs_area = soup.find(id = 'searchCount').string.encode('utf-8')
    job_numbers = re.findall('\d+', str(num_jobs_area)) # Total number of jobs found

    if len(job_numbers) > 3:
        total_num_jobs = (int(job_numbers[2]) * 1000) + int(job_numbers[3])
    else:
        total_num_jobs = int(job_numbers[2])

    if city is None:
        print(str(total_num_jobs) + ' jobs found nationwide')

    print(str(total_num_jobs) + ' jobs found in ' + city_copy + ', ' + state) 

    num_pages = total_num_jobs / 10 

    job_descriptions = [] # Store all job descriptions 

    for i in range(1, int(num_pages+1)):
        print('Getting page ' + str(i))
        start_num = str(i*10)
        current_page = ''.join([url, '&start=', start_num])
    
        html_page = requests.get(current_page).text
        page_soup = make_soup(html_page)

        job_link_area = page_soup.find(id = 'resultsCol') # The center column on the page where job postings exist
        job_urls = [base_url + link.get('href') for link in job_link_area.find_all('a', href=True)] # Get the URLs for the jobs
        job_urls = [x for x in job_urls if 'clk' in x] # Get just the job related URLs
     
        for j in range(0, len(job_urls)):
            description = get_job_info(job_urls[j])
            if description: # Only append when the website was accessed correctly
                job_descriptions.append(description)
            sleep(1) # Not to hit the server a lot

    print('Done with collecting the job postings!')
    print('There were ' + str(len(job_descriptions)) + ' jobs successfully found.')

    doc_frequency = Counter() # Create a full counter of skills
    [doc_frequency.update(item) for item in job_descriptions] # List comp

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

    total_skills = language_dict + tool_dict + big_data_dict + database_dict # Preset dictionary of total skills

    df = pd.DataFrame(list(total_skills.items()), columns = ['Skill', 'NumPostings']) # Convert skils into a dataframe
    df.NumPostings = (df.NumPostings) * 100 / len(job_descriptions) # Percentage of job postings having that skil
    df.sort_values(by='NumPostings', ascending=True, inplace=True) # Sort data for plottiing


    plot = df.plot(x='Skill', kind='barh', legend=False, color='skyblue', title='Percentage of Data Scientist Job Ads with a Key Skill, ' + city_copy)
    plot.set_xlabel('Percentage Appearing in Job Ads')
    
    fig = plot.get_figure() # Convert the pandas plot object to a matplotlib object
    plt.tight_layout()

    return fig, df



city = 'Syracuse'
state = 'NY'
info = get_skill_info(city=city, state=state)
print(info[1])
print(type(info[1]))
print(type(info[0]))
info[0].savefig('/home/angelaxu/Xcode/projects/Indeed_Web_Scraping/fig5.png')



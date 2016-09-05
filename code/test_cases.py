from scraper1_singlethreading import get_job_info
from scraper2_multithreading import get_page_info

# test case of get_job_info()
url = 'http://www.indeed.com/viewjob?jk=ad7a03682c45df5e&q=data+scientist&l=Seattle%2C+WA&tk=1aq1lqih6bukkcbp&from=web'
print('')
print('------ Test of get_job_info() ------')
test = get_job_info(url)
print('')
print(test)
print('')
print('------ get_job_info() - test pass ------')

# test case of get_page_info()
url = 'http://www.indeed.com/jobs?q=data+scientist&l=Seattle%2C+WA'
page_num = 2
print('')
print('------ Test of get_page_info() ------')
test = get_page_info(url, page_num)
print('')
print(test)
print('')
print('------ get_page_info() - test pass ------')


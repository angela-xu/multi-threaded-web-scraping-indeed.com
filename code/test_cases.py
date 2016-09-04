# test case of get_job_info()
url1 = 'http://www.indeed.com/viewjob?jk=ad7a03682c45df5e&q=data+scientist&l=Seattle%2C+WA&tk=1aq1lqih6bukkcbp&from=web'
test1 = get_job_info(url)
print('Test of get_job_info():')
print('')
print(test1)



# test case of get_page_info()
url2 = 'http://www.indeed.com/jobs?q=data+scientist&l=Seattle%2C+WA'
page_num = 2
test2 = get_page_info(url, page_num)
print('Test of get_page_info():')
print('')
print(test2)


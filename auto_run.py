import job_scraper
import csv

city_state_list = []

with open('cities.csv', newline='') as csvfile:
    city_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in city_reader:
        try:
            city_state_list.append((row[0], row[1]))
        except:
            pass

today = job_scraper.datetime.date.today()
today_1 = today.strftime('%m-%d-%Y')
today_2 = today.strftime('%m_%d_%Y')

# Total number of cities
num_of_cities = len(city_state_list)
# Total number of job ads scraped
auto_run_total_jobs = 0
# Total size of job ad web pages in bytes  
auto_run_total_size = 0

auto_run_start_time = job_scraper.time.time()

for (city, state) in city_state_list:
    print('------ Scraping Job Ads in ' + city + ', ' + state + ' ------')
    start_time = job_scraper.time.time()
    (total_jobs_found, total_size, dataframe, figure) = job_scraper.run_scraper(city=city, state=state)
    run_time = job_scraper.time.time() - start_time

    auto_run_total_jobs += total_jobs_found
    auto_run_total_size += total_size

    print('')
    print('Date: ' + today_1)
    print('City: ' + city + ', ' + state)
    print('Number of Jobs: ' + str(total_jobs_found))
    print('Bytes processed: ' + str(total_size))
    print('Run Time: %s seconds' % (run_time))
    print('')
    print(dataframe)
    print('')

    with open('output/%s_%s.txt' % (city, today_2), 'a') as log:
        log.write('Date: ' + today_1 + '\n')
        log.write('City: ' + city + ', ' + state + '\n')
        log.write('Number of Jobs: ' + str(total_jobs_found) + '\n')
        log.write('Bytes processed: ' + str(total_size) + '\n')
        log.write('Run Time: %s seconds' % (run_time) + '\n\n')

    dataframe.to_csv('output/%s_%s.csv' % (city, today_2), sep='\t', index=False)
    figure.savefig('output/%s_%s.png' % (city, today_2))

with open('output/auto_run_%s.txt' % (today_2), 'a') as auto_log:
    auto_log.write('Date: ' + today_1 + '\n')
    auto_log.write('Number of Cities: ' + str(num_of_cities) + '\n')
    auto_log.write('Number of Jobs: ' + str(auto_run_total_jobs) + '\n')
    auto_log.write('Bytes processed: ' + str(auto_run_total_size) + '\n')
    auto_log.write('Run Time: %s' % (job_scraper.time.time() - auto_run_start_time) + '\n\n')

import job_scraper
import csv

city_state_list = []

line_num = 0

with open('Top1000Population.csv', newline='') as csvfile:
    city_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in city_reader:
        line_num += 1
        try:
            print(line_num)
            print(row)
            city_state_list.append((row[0], row[1]))
        except:
            pass

print(city_state_list)

for (city, state) in city_state_list:
    print("Scraping" + city + ", " + state)
    start_time = job_scraper.time.time()
    (total_jobs_found, total_size, dataframe, figure) = job_scraper.run_scraper(city=city, state=state)
    run_time = job_scraper.time.time() - start_time
    
    today = job_scraper.datetime.date.today()
    today_1 = today.strftime('%m-%d-%Y')
    today_2 = today.strftime('%m_%d_%Y')
    
    print('')
    print('Date: ' + today_1)
    print('City: ' + city + ', ' + state)
    print('Number of Jobs Scraped: ' + str(total_jobs_found))
    print('Bytes processed: ' + str(total_size))
    print('Run Time: %s seconds' % (run_time))
    print('')
    print(dataframe)
    dataframe.to_csv('output/%s_%s.txt' % (city, today_2), sep='\t', index=False)
    figure.savefig('output/%s_%s.png' % (city, today_2))


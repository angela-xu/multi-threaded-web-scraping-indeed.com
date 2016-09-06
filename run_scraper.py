import job_scraper
import argparse

parser = argparse.ArgumentParser(description='Find Most-Wanted Skills for Different Jobs on indeed.com')
parser.add_argument('--city', nargs = 1, help='target city')
parser.add_argument('--state', nargs = 1, help='target state in abbreviation like "WA", "CA", or "NY"')
args = parser.parse_args()

city = args.city[0]
state = args.state[0]

start_time = job_scraper.time.time()
info = job_scraper.run_scraper(city=city, state=state)
run_time = job_scraper.time.time() - start_time

today = job_scraper.datetime.date.today()
today_1 = today.strftime('%m-%d-%Y')
today_2 = today.strftime('%m_%d_%Y')

start_time = jobscraper.time.time()
(total_jobs_found, dataframe, figure) = jobscraper.run_scraper(city=city, state=state)
run_time = jobscraper.time.time() - start_time

print('')
print('Date: ' + today)
print('City: ' + city + ', ' + state)
print('Number of Jobs Scraped: ' + str(total_jobs_found))
print('Run Time: %s seconds' % (run_time))
print('')
print(info[df])
dataframe.to_csv('output/%s_%s.txt' % (city, today), sep='\t')
figure.savefig('output/%s_%s.png' % (city, today))

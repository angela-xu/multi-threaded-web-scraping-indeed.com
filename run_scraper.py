import jobscraper
import argparse

parser = argparse.ArgumentParser(description='Find hot skills for different career positions on indeed.com')
parser.add_argument('--city', nargs = 1, help='target city')
parser.add_argument('--state', nargs = 1, help='target state in abbreviation like "WA" or "NY"')
parser.add_argument('--numThreads', nargs = 1, type=int, default=20,  help='number of threads that will be spawned by the application')
args = parser.parse_args()

city = args.city[0]
state = args.state[0]
numThreads = args.numThreads

start_time = jobscraper.time.time()
info = jobscraper.run_scraper(city=city, state=state)
run_time = jobscraper.time.time() - start_time

today = jobscraper.datetime.date.today().strftime('%m_%d_%Y')

print('')
print('Date: ' + today)
print('City: ' + city + ', ' + state)
print('Number of Jobs Scraped: ' + str(info[0]))
print('Run Time: %s seconds' % (run_time))
print('')
print(info[1])
info[1].to_csv('output/%s_%s.txt' % (city, today), sep='\t')
info[2].savefig('output/%s_%s.png' % (city, today))

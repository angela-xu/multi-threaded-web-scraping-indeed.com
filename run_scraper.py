import scraper3_multithreading as sp

start_time = sp.time.time()
info = sp.get_skill_info(city=city, state=state)
end_time = sp.time.time()
run_time = end_time - start_time

today = sp.datetime.date.today()
today_1 = today.strftime('%m-%d-%Y')
today_2 = today.strftime('%m_%d_%Y')

print('')
print('Date: ' + today_1)
print('City: ' + city + ', ' + state)
print('Number of Jobs Scraped: ' + str(info[0]))
print('Run Time: %s seconds' % (run_time))
print('')
print(info[1])
info[1].to_csv('output/%s_%s.txt' % (city, today_2), sep='\t')
info[2].savefig('output/%s_%s.png' % (city, today_2))

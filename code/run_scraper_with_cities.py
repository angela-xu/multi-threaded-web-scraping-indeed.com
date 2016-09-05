import scraper3_multithreading as sp

# state = 'WA'
# city = 'Seattle'
# city = 'Spokane'
# city = 'Tacoma'
# city = 'Bellevue'
# city = 'Everett'
# city = 'Renton'
# city = 'Yakima'
# city = 'Kirkland'
# city = 'Redmond'

# state = 'CA'
# city = 'Los Angeles'
# city = 'San Diego'
# city = 'San Jose'
# city = 'San Francisco'
# city = 'Fresno'
# city = 'Sacramento'
# city = 'Long Beach'
# city = 'Oakland'
# city = 'Riverside'
# city = 'Irvine'

# state = 'TX'
# city = 'Houston'
# city = 'San Antonio'
# city = 'Dallas'
# city = 'Austin'
# city = 'Fort Worth'

# state = 'NJ'
# city = 'Newark'
# city = 'Jersey City'

# state = 'FL'
# city = 'Jacksonville'
# city = 'Miami'

# city = 'New York'
# state = 'NY'

# city = 'Chicago'
# state = 'IL'

# city = 'Washington'
# state = 'DC'

# city = 'Boston'
# state = 'MA'

# city = 'Houston'
# state = 'TX'

# city = 'Philadelphia'
# state = 'PA'

# city = 'Phoenix'
# state = 'AZ'

# city = 'Minneapolis'
# state = 'MN'

# city = 'Pittsburgh'
# state = 'PA'

# city = 'Syracuse'
# state = 'NY'

# city = 'Columbus'
# state = 'OH'

# city = 'Charlotte'
# state = 'North Carolina'

# city = 'Las Vegas'
# state = 'Nevada'

# city = 'Atlanda'
# state = 'GA'

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

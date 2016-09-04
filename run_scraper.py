from better_scraper_n import *
import datetime

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

# city = 'San Antonio'
# state = 'TX'

# city = 'Dallas'
# state = 'TX'

# city = 'Austin'
# state = 'TX'

# city = 'Minneapolis'
# state = 'MN'

# city = 'Pittsburgh'
# state = 'PA'

# city = 'Newark'
# state = 'NJ'

# city = 'Jersey City'
# state = 'NJ'

city = 'Syracuse'
state = 'NY'


# state = 'FL'
# city = 'Jacksonville'
# city = 'Miami'

# city = 'Columbus'
# state = 'OH'

# city = 'Charlotte'
# state = 'North Carolina'

# city = 'Las Vegas'
# state = 'Nevada'

# city = 'Atlanda'
# state = 'GA'


start_time = time.time()
info = get_skill_info(city=city, state=state)
end_time = time.time()
run_time = end_time - start_time
print('run time --- %s seconds ---' % (run_time))
print('')
print(info[0])

with open('./output/%s.txt' % (city), 'w') as text_file:
    text_file.write(info[0])
# info[0].savefig('./output/%s/%s_%s.png' % (city, city, datetime.date().today()))
# info[1].to_csv('./output/%s/%s.csv' % (city, city), sep='\t')

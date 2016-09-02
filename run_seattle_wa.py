from better_scraper_n import *

# city = 'Seattle'
# state = 'WA'
city = 'Pittsburgh'
state = 'PA'

start_time = time.time()
info = get_skill_info(city=city, state=state)
print('--- %s seconds ---' % (time.time() - start_time))
print('')

print(info[1])
info[0].savefig('/home/angelaxu/Xcode/projects/Seattle_090116.png')


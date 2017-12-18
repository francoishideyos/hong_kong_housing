import requests, math, time,pandas as pd
from bs4 import BeautifulSoup

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

link          = []
date_of_visit = []

r = requests.get('https://www.28hse.com/en/buy/house-type-g1',headers=headers)

soup = BeautifulSoup(r.text,"lxml")

# Get the number of results
result = soup.find('div', class_='search_total_result')

num_result = float(result.find('em').string)

# Number of pages
pages = math.ceil(num_result/15)
# print('There are {} pages'.format(pages))

# find class="agentad_a clearfix "
listings = soup.findAll('div',class_='agentad_a clearfix ')
for item in listings:
	link.append(item.p.a['href'])
    date_of_visit.append(time.strftime("%H:%M:%S"))

# from page 2 to pages
base_url = 'https://www.28hse.com/en/buy/house-type-g1/list-'

i = 2
while i < pages + 1:
	url = base_url + str(i)
	r = requests.get(url,headers=headers)
	soup = BeautifulSoup(r.text,"lxml)
	#find class="agentad_a clearfix "
	listings = soup.findAll('div',class_='agentad_a clearfix ')
	for item in listings:
		link.append(item.p.a['href'])
        date_of_visit.append(time.strftime("%H:%M:%S"))
    i += 1

data = [link,date_of_visit]
df = pd.DataFrame(data)
df = df.transpose()
cols = ['Link','Date']
df.columns = cols

import time
import requests
import sys
import re
from win10toast import ToastNotifier
from bs4 import BeautifulSoup


toaster = ToastNotifier()
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'pragma': 'no-cache',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'cache-control': 'no-cache',
        'connection': 'keep-alive',
        'host': 'termmasterschedule.drexel.edu'
        }
urls = open('links.txt').read().split('\n')
for url in range(0, len(urls)):
    if urls[url] == '':
        urls.pop(url)

while True:
	time.sleep(int(sys.argv[1]))
	for i in range(0, len(urls)):
		response = requests.get(urls[i], headers=headers)
		if (response.status_code != 200):
			print("Unable to get data from URL #" + str(i))
		soup = BeautifulSoup(response.text, features="html.parser")
		elements = soup.find_all("td", class_="tableHeader".split())
		enroll = None
		for element in elements:
			if element.get_text() == 'Enroll':
				enroll = element.findNext('td').get_text()
				break
		if enroll == None:
			print("Unable to parse data from URL #" + str(i))
		if enroll == 'CLOSED':
			continue
		else:
			toaster.show_toast("Your class has opened up for the URL #" + str(i + 1))
			sys.stdout.write("Your class has opened up for the url " + str(urls[i]) + "\n")
			sys.stdout.flush()
			urls.pop(i)
			

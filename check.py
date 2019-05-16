import time
import requests
import sys
import re
from win10toast import ToastNotifier
from bs4 import BeautifulSoup

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'pragma': 'no-cache',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'cache-control': 'no-cache',
        'connection': 'keep-alive',
        'host': 'termmasterschedule.drexel.edu'
        }

def getURL(class_url):
	response = requests.get(class_url, headers=headers)
	if (response.status_code != 200):
		printToStdOut("Unable to get data from URL #" + str(i))
	return response

class Notification():
	toaster = ToastNotifier()
	message = None
	def __init__(self, message):
		self.message = message

	def displayNotification(self):
		self.toaster.show_toast("Enrollment Checker", self.message, duration=10, threaded=True)

def printToStdOut(message):
	sys.stdout.write(message)
	sys.stdout.flush()

def checkClasses(classes, delay):
	#Base case, all classes have been checked
	if len(classes) == 0:
		return
	time.sleep(delay)
	for i in range(0, len(classes)):
		response = getURL(classes[i])
		soup = BeautifulSoup(response.text, features="html.parser")
		elements = soup.find_all("td", class_="tableHeader".split())
		enroll = None
		#If we find an element that contains 'Enroll', the next td contains enrollment number
		for element in elements:
			if element.get_text() == 'Enroll':
				enroll = element.findNext('td').get_text()
				break
		if enroll == None:
			print("Unable to parse data from URL #" + str(i))
		#If the enrollment is closed (maybe do something?)
		elif enroll == 'CLOSED':
			continue
		#Display notification, print message, remove from array, call function with rest of array
		else:
			notification = Notification("Your class has opened up for the URL #" + str(i + 1))
			notification.displayNotification()
			printToStdOut("Your class has opened up for the url " + str(classes[i]) + "\n")
			classes.pop(i)
			checkClasses(classes, delay)
			return
	checkClasses(classes, delay)

if __name__ == "__main__":
	urls = open('links.txt').read().split('\n')
	sleep_time = 15
	if len(sys.argv) == 2:
		sleep_time = int(sys.argv[1])
	for url in range(0, len(urls)):
		if urls[url] == '':
			urls.pop(url)
	checkClasses(urls, sleep_time)
	printToStdOut("Your classes have all opened up!")

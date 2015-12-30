# Written by Robert Bradshaw (Georgia Tech)
# v1.0.0
# Apparently, the majority of pages on Wikipedia will eventually link to the Philosophy page if you keep following the first non-italicized link on each page.
# TODO: Implement adjency list and Dijkstra's shortest path algorithm to find the shortest path to the Philosophy page.

import random, argparse, os, time, urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import *

def ViewBot(browser):
	visitedPages = {}
	record = []
	count = 0

	while (True):
		current = BeautifulSoup(browser.page_source, "lxml")

		title = str(current.find("title"))
		if (title in visitedPages):
			print ("Circular reference detected. I gotta end it here.")
			return record
		elif (title not in visitedPages):
			visitedPages[title] = 1
		else:
			return None

		if ("Philosophy" in title):
			print ("it took " + str(count) + " links to get there, but we made it. Here's the sequence you went in: \n")
			print (record)
			return (record)

		interval = random.triangular(.5, 6, 1)
		time.sleep(interval)

		nextLink = getNextLink(current)
		if (not nextLink):
			print ("Couldn't find another link to follow.")
			return None
		nextLink = "https://en.wikipedia.org" + nextLink

		record.append(nextLink)
		browser.get(nextLink)

		print (count)
		count = count + 1


def getNextLink(page):
	par = page.find("p")
	for link in par.find_all('a'):
		currentURL = link.get('href')
		if (currentURL):
			if (isValid(currentURL)):
				return currentURL
	return None

def isValid(url):
	blacklist = ["#cite_note", "Help:"]
	for element in blacklist:
		if (element in url):
			return False
	return True

def Main():
	parser = argparse.ArgumentParser()
	parser.add_argument("pageName", help = "page you're searching for")
	args = parser.parse_args()

	browser = webdriver.Firefox()
	browser.get("https://wikipedia.org")

	searchBox = browser.find_element_by_id("searchInput")
	searchBox.send_keys(args.pageName)
	searchBox.submit()

	os.system("clear")

	print ("Bot initialized.")
	ViewBot(browser)
	browser.close()

if (__name__ == "__main__"):
	Main()

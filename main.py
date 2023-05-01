from datagather import simulate
from util import post_event
import datetime


def main():
	url = "http://localhost:8020/elevator-request"

	#Simulate one week of collecting elevator data
	sim = simulate(datetime.datetime(2023, 4, 1, 6, 0, 0), datetime.datetime(2023, 4, 8, 6, 0, 0), 10)

	#Post each event on the database for future data science stuff
	for s in sim:
		post_event(url, s)


main()
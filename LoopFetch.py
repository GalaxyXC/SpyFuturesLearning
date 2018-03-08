# Code written by Liansai Dong
# Last Edit: 2018-03-08
# CPython version: 3.4.4

# Environment installed with Bloomberg Python API 3.9.0, available at
# https://www.bloomberg.com/professional/support/api-library/
import re
import time

import FetchHistory

memberFile = "SPX_member.prn"

with open(memberFile, "r") as f:
	text = f.read()
	Ticker = re.findall("[\w ]+Equity", text)
	count = 0
	for tck in Ticker:
		count += 1
		if count > 506:
			break

		print(tck)

		try:
			time.sleep(1.7)
			FetchHistory.FetchHistoryData(tck, "19860101", "20171231")
			print(tck, " successfully fetched")
		except:
			print(tck, " failed to fetch")

	print(str(len(Ticker)) + " ticker(s) parsed.")

FetchHistory.FetchHistoryData("SPY US Equity", "19860101", "20171231")
print("SPY US Equity fetched.")
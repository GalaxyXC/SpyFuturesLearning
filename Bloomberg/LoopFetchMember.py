# Code written by Liansai Dong
# Last Edit: 2018-03-26
# CPython version: 3.4.4

# Environment installed with Bloomberg Python API 3.9.0, available at
# https://www.bloomberg.com/professional/support/api-library/

import datetime as dt
import time

import FetchHistoricalMember


if __name__ == "__main__":
    # Initialization
    startDay = dt.date(2013,1,1)
    thisDay = startDay
    # endDay = dt.date(1996,2,1)
    endDay = dt.date(2017,12,31)

    # a Set to store all Ticker ID
    tckList = set([])

    start_time = time.time()
    
    step = 0
    while (thisDay - endDay) <= dt.timedelta(days = 0):
        step += 1
        if step % 30 == 0:
            print("crawling member list for: " + thisDay.strftime("%Y%m%d"))

        try:
            time.sleep(0.3)
            FetchHistoricalMember.getMemberAtDate(tckList, thisDay.strftime("%Y%m%d"))
        except:
            print("crawling member list failed for:" + str(thisDay))

        thisDay = thisDay + dt.timedelta(days = 1)

    print("Crawling from: " + str(startDay) + " to: " + str(endDay) + " ... ")
    print(str(len(tckList)) + " tickers collected.")
    print("Real Exec. time: %s seconds ---" % round((time.time() - start_time), 2))

    with open("UniqueTickerList.txt", "w") as f:
        f.write("\n".join(tckList))

import re

f0 = "SPX_member.prn"
f1 = "UniqueTickerList_1990_1991.txt"
f1_b = "UniqueTickerList_1990_1991_b.txt"
f2 = "UniqueTickerList_1992_2012.txt"
f3 = "UniqueTickerList_2013_2017.txt"

additionalCrawlList = set([])
with open(f0, "r") as ref:
    allTicker = ref.read()
    with open(f1, "r") as f:
        for line in f:
            fullTicker = line.strip() + " Equity"
            if bool(re.search(fullTicker, allTicker)): # found in ref
                continue
            else:
                additionalCrawlList.add(fullTicker)

    with open(f2, "r") as f:
        for line in f:
            fullTicker = line.strip() + " Equity"
            if bool(re.search(fullTicker, allTicker)): # found in ref
                continue
            else:
                additionalCrawlList.add(fullTicker)

    with open(f3, "r") as f:
        for line in f:
            fullTicker = line.strip() + " Equity"
            if bool(re.search(fullTicker, allTicker)): # found in ref
                continue
            else:
                additionalCrawlList.add(fullTicker)

outStr = str('\n'.join(additionalCrawlList))

print("=== Additional: ===")
print(outStr)

with open("additionalTicker.txt", "w") as fw:
    fw.write(outStr)
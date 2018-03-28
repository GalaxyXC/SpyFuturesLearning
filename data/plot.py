import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot

# values
inputDirectory = "FieldData/"
outputDirectory = "plot/"
if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

filename = 'SPY US EquityFieldData.csv'

# table 1

for filename in os.listdir(inputDirectory):
    if filename.endswith("FieldData.csv"):
        print("\n PARSING: " + os.path.join(inputDirectory, filename))

        N = 0
        Nfield = 0
        meanOpen = 0
        meanClose = 0
        meanHigh = 0
        meanLow = 0
        meanVolumn = 0

        security = pd.read_csv((inputDirectory + filename), index_col=0, header=None).T
        security['date'] = pd.to_datetime(security['date'], format='%Y-%m-%d', errors='ignore')
        security = security.set_index('date')

        N = security.shape[0]
        Nfield = security.shape[1]
        try:
            meanOpen = pd.to_numeric(security['OPEN']).mean()
        except:
            meanOpen = -99

        try:
            meanClose = pd.to_numeric(security['PX_LAST']).mean()
        except:
            meanClose = -99

        try:
            meanHigh = pd.to_numeric(security['HIGH']).mean()
        except:
            meanHigh = -99

        try:
            meanLow = pd.to_numeric(security['LOW']).mean()
        except:
            meanLow = -99

        try:
            meanVolumn = pd.to_numeric(security['VOLUME']).mean()
        except:
            meanVolumn = -99

        header = ['name', 'N', 'Nfields', 'MeanOpen', 'MeanClose', 'MeanHigh', 'MeanLow', 'MeanVolume']
        # Nobs, Nfields = security.shape
        # MeanOpen, MeanClose, MeanHigh, MeanLow, MeanVol = security.mean()
        out = []
        out.append(filename)
        out.append(N)
        out.append(Nfield)
        out.append(meanOpen)
        out.append(meanClose)
        out.append(meanHigh)
        out.append(meanLow)
        out.append(meanVolumn)

        try:
            with open(outputDirectory+"Table1_Summaries.csv", "a", newline="") as f:
                csvWriter = csv.writer(f)
                csvWriter.writerow(out)
        except:
            with open(outputDirectory+"Table1_Summaries.csv", "w", newline="") as f:
                csvWriter = csv.writer(f)
                csvWriter.writerow()
                csvWriter.writerow(out)




# Fig 1 Tiem Series
spy = pd.read_csv((inputDirectory + filename), index_col=0, header=None).T
spy['date'] = pd.to_datetime(spy['date'], format='%Y-%m-%d', errors='ignore')
spy['OPEN'] = pd.to_numeric(spy['OPEN'])
spy['HIGH'] = pd.to_numeric(spy['HIGH'])
spy['LOW'] = pd.to_numeric(spy['LOW'])
spy['PX_LAST'] = pd.to_numeric(spy['PX_LAST'])
spy['VOLUME'] = pd.to_numeric(spy['VOLUME'])
spy = spy.set_index('date')

'''
fig, ax = plt.subplots()
ax3 = ax.twinx()
rspine = ax3.spines['right']
rspine.set_position(('axes', 1.15))
ax3.set_frame_on(True)
ax3.patch.set_visible(False)
fig.subplots_adjust(right=0.7)

pd.to_numeric(spy['OPEN']).plot()
pd.to_numeric(spy['HIGH']).plot()
pd.to_numeric(spy['LOW']).plot()
pd.to_numeric(spy['PX_LAST']).plot()
pd.to_numeric(spy['VOLUME']).plot(secondary_y=True)
'''

spy.plot(subplots=True, figsize=(12, 8), title='SPY US Equity');

# Fig 2 Lag plot
# Using the spy data frame from above

# plotting
fig = plt.figure()
ax = fig.add_subplot(111)

# draw lag_plot iteratively through: OPEN; PX_LAST; HIGH; LOW; VOLUME
# (remember to change output file name)
lag_plot(spy['LOW'])

ax.yaxis.set_ticks_position('none')
ax.xaxis.set_ticks_position('none')

a = 0.7
# ticks = [1000,2000,3000,4000,5000]
# ticks = [20,40,60,80,100]
ticks = [50,100,150,200,250]
ax.xaxis.set_ticks(ticks)
ax.set_xticklabels(ticks, fontsize=10, alpha=a)
ax.yaxis.set_ticks(ticks)
ax.set_yticklabels(ticks, fontsize=10, alpha=a)

ax.set_xlabel('SPY Open Price (t)', fontsize=10, alpha=a, ha='left')
ax.set_ylabel('SPY Open Price (t+1)', fontsize=10, alpha=a)

plt.savefig(outputDirectory + 'Fig2_LagPlot.png', bbox_inches='tight', dpi=300)
# plt.show(block=True)


# Fig 3 histogram
spy.hist(alpha=0.5, figsize=(16, 8))

# Fig 4 boxplot
# merge dataset first
import os
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

# Process Demand Data
count = 0
for file in os.listdir('datasets/Demand'):
  if count == 0:
    if file.startswith('PUBLIC_HISTDEMAND'):
      dfDem = pd.read_csv('datasets/Demand/' + file, skiprows=1, usecols=[4, 5, 6, 7], skipfooter=1, engine='python')
      count += 1
  else:
    if file.startswith('PUBLIC_HISTDEMAND'):
      dfDem2 = pd.read_csv('datasets/Demand/' + file, skiprows=1, usecols=[4, 5, 6, 7], skipfooter=1, engine='python')
      dfDem = dfDem.append(dfDem2, ignore_index=True)

# Process Solar Data
countSol = 0
for file in os.listdir('datasets/Solar'):
  if countSol == 0:
    if file.startswith('PUBLIC_ROOFTOP'):
      dfSol = pd.read_csv('datasets/Solar/' + file, skiprows=1, usecols=[4, 5, 6], skipfooter=1, engine='python')
      countSol += 1
  else:
    if file.startswith('PUBLIC_ROOFTOP'):
      dfSol2 = pd.read_csv('datasets/Solar/' + file, skiprows=1, usecols=[4, 5, 6], skipfooter=1, engine='python')
      dfSol = dfSol.append(dfSol2, ignore_index=True)

# Get data starting Oct-2019 to Sep-2020 only
dfDem = dfDem[dfDem['SETTLEMENTDATE'] >= '2019/10/01 00:00:00'].reset_index()
dfSol = dfSol[dfSol['INTERVAL_DATETIME'] >= '2019/10/01 00:00:00']
dfSol = dfSol[dfSol['INTERVAL_DATETIME'] < '2020/10/01 00:00:00'].reset_index()

# Pivot Dataframes
dfPivotDem = dfDem.pivot_table('DEMAND.1', ['SETTLEMENTDATE', 'PERIODID'], 'REGIONID').reset_index()
dfPivotSol = dfSol.pivot_table('POWER', ['INTERVAL_DATETIME'], 'REGIONID').reset_index()

# Add Quarter of Year Column
dfPivotDem['quarter'] = pd.PeriodIndex(dfPivotDem.SETTLEMENTDATE, freq='Q')
dfPivotSol['quarter'] = pd.PeriodIndex(dfPivotSol.INTERVAL_DATETIME, freq='Q')

# Insert TimePeriods on Solar Dataframe
dfPivotSol['PERIOD'] = pd.to_datetime(dfPivotSol['INTERVAL_DATETIME']).dt.strftime('%H:%M')

# Do Averageifs on dataframes
dfAggDem = dfPivotDem.groupby(['quarter','PERIODID']).mean().round(2)
dfAggSol = dfPivotSol.groupby(['quarter', 'PERIOD']).mean().round(2)

# Set x values for scatter plot
x = np.arange(0, 48, 1, dtype='int')

# Extract data to be plotted and save to a list
# Q4 2019 DATA
NSWDemQ4 = list(dfAggDem['NSW1'][dfAggDem['quarter'] == '2019Q4'])
NSWSolQ4 = list(dfAggSol['NSW1'][dfAggSol['quarter'] == '2019Q4'])
VICDemQ4 = list(dfAggDem['VIC1'][dfAggDem['quarter'] == '2019Q4'])
VICSolQ4 = list(dfAggSol['VIC1'][dfAggSol['quarter'] == '2019Q4'])

NSWDemQ4Max = []
NSWDemQ4Min = []
for i in range(len(NSWDemQ4)):
  if NSWDemQ4[i] != max(NSWDemQ4):
    NSWDemQ4Max.append(None)
  else:
    NSWDemQ4Max.append(int(NSWDemQ4[i]))
  if NSWDemQ4[i] != min(NSWDemQ4):
    NSWDemQ4Min.append(None)
  else:
    NSWDemQ4Min.append(int(NSWDemQ4[i]))

NSWSolQ4Max = []
NSWSolQ4Min = []
for i in range(len(NSWSolQ4)):
  if NSWSolQ4[i] != max(NSWSolQ4):
    NSWSolQ4Max.append(None)
  else:
    NSWSolQ4Max.append(int(NSWSolQ4[i]))

VICDemQ4Max = []
VICDemQ4Min = []
for i in range(len(VICDemQ4)):
  if VICDemQ4[i] != max(VICDemQ4):
    VICDemQ4Max.append(None)
  else:
    VICDemQ4Max.append(int(VICDemQ4[i]))
  if NSWDemQ4[i] != min(NSWDemQ4):
    VICDemQ4Min.append(None)
  else:
    VICDemQ4Min.append(int(VICDemQ4[i]))

VICSolQ4Max = []
for i in range(len(VICSolQ4)):
  if VICSolQ4[i] != max(VICSolQ4):
    VICSolQ4Max.append(None)
  else:
    VICSolQ4Max.append(int(VICSolQ4[i]))

# Q1 2020 DATA
NSWDemQ1 = list(dfAggDem['NSW1'][dfAggDem['quarter'] == '2020Q1'])
NSWSolQ1 = list(dfAggSol['NSW1'][dfAggSol['quarter'] == '2020Q1'])
VICDemQ1 = list(dfAggDem['VIC1'][dfAggDem['quarter'] == '2020Q1'])
VICSolQ1 = list(dfAggSol['VIC1'][dfAggSol['quarter'] == '2020Q1'])

NSWDemQ1Max = []
NSWDemQ1Min = []
for i in range(len(NSWDemQ1)):
  if NSWDemQ1[i] != max(NSWDemQ1):
    NSWDemQ1Max.append(None)
  else:
    NSWDemQ1Max.append(int(NSWDemQ1[i]))
  if NSWDemQ1[i] != min(NSWDemQ1):
    NSWDemQ1Min.append(None)
  else:
    NSWDemQ1Min.append(int(NSWDemQ1[i]))

NSWSolQ1Max = []
for i in range(len(NSWSolQ1)):
  if NSWSolQ1[i] != max(NSWSolQ1):
    NSWSolQ1Max.append(None)
  else:
    NSWSolQ1Max.append(int(NSWSolQ1[i]))

VICDemQ1Max = []
VICDemQ1Min = []
for i in range(len(VICDemQ1)):
  if VICDemQ1[i] != max(VICDemQ1):
    VICDemQ1Max.append(None)
  else:
    VICDemQ1Max.append(int(VICDemQ1[i]))
  if NSWDemQ1[i] != min(NSWDemQ1):
    VICDemQ1Min.append(None)
  else:
    VICDemQ1Min.append(int(VICDemQ1[i]))

VICSolQ1Max = []
for i in range(len(VICSolQ1)):
  if VICSolQ1[i] != max(VICSolQ1):
    VICSolQ1Max.append(None)
  else:
    VICSolQ1Max.append(int(VICSolQ1[i]))

# Q2 2020 DATA
NSWDemQ2 = list(dfAggDem['NSW1'][dfAggDem['quarter'] == '2020Q2'])
NSWSolQ2 = list(dfAggSol['NSW1'][dfAggSol['quarter'] == '2020Q2'])
VICDemQ2 = list(dfAggDem['VIC1'][dfAggDem['quarter'] == '2020Q2'])
VICSolQ2 = list(dfAggSol['VIC1'][dfAggSol['quarter'] == '2020Q2'])

NSWDemQ2Max = []
NSWDemQ2Min = []
for i in range(len(NSWDemQ2)):
  if NSWDemQ2[i] != max(NSWDemQ2):
    NSWDemQ2Max.append(None)
  else:
    NSWDemQ2Max.append(int(NSWDemQ2[i]))
  if NSWDemQ2[i] != min(NSWDemQ2):
    NSWDemQ2Min.append(None)
  else:
    NSWDemQ2Min.append(int(NSWDemQ2[i]))

NSWSolQ2Max = []
for i in range(len(NSWSolQ2)):
  if NSWSolQ2[i] != max(NSWSolQ2):
    NSWSolQ2Max.append(None)
  else:
    NSWSolQ2Max.append(int(NSWSolQ2[i]))

VICDemQ2Max = []
VICDemQ2Min = []
for i in range(len(VICDemQ2)):
  if VICDemQ2[i] != max(VICDemQ2):
    VICDemQ2Max.append(None)
  else:
    VICDemQ2Max.append(int(VICDemQ2[i]))
  if VICDemQ2[i] != min(VICDemQ2):
    VICDemQ2Min.append(None)
  else:
    VICDemQ2Min.append(int(VICDemQ2[i]))

VICSolQ2Max = []
for i in range(len(VICSolQ2)):
  if VICSolQ2[i] != max(VICSolQ2):
    VICSolQ2Max.append(None)
  else:
    VICSolQ2Max.append(int(VICSolQ2[i]))

# Q3 2020 DATA
NSWDemQ3 = list(dfAggDem['NSW1'][dfAggDem['quarter'] == '2020Q3'])
NSWSolQ3 = list(dfAggSol['NSW1'][dfAggSol['quarter'] == '2020Q3'])
VICDemQ3 = list(dfAggDem['VIC1'][dfAggDem['quarter'] == '2020Q3'])
VICSolQ3 = list(dfAggSol['VIC1'][dfAggSol['quarter'] == '2020Q3'])

NSWDemQ3Max = []
NSWDemQ3Min = []
for i in range(len(NSWDemQ3)):
  if NSWDemQ3[i] != max(NSWDemQ3):
    NSWDemQ3Max.append(None)
  else:
    NSWDemQ3Max.append(int(NSWDemQ3[i]))
  if NSWDemQ3[i] != min(NSWDemQ3):
    NSWDemQ3Min.append(None)
  else:
    NSWDemQ3Min.append(int(NSWDemQ3[i]))

NSWSolQ3Max = []
for i in range(len(NSWSolQ3)):
  if NSWSolQ3[i] != max(NSWSolQ3):
    NSWSolQ3Max.append(None)
  else:
    NSWSolQ3Max.append(int(NSWSolQ3[i]))

VICDemQ3Max = []
VICDemQ3Min = []
for i in range(len(VICDemQ3)):
  if VICDemQ3[i] != max(VICDemQ3):
    VICDemQ3Max.append(None)
  else:
    VICDemQ3Max.append(int(VICDemQ3[i]))
  if NSWDemQ3[i] != min(NSWDemQ3):
    VICDemQ3Min.append(None)
  else:
    VICDemQ3Min.append(int(VICDemQ3[i]))

VICSolQ3Max = []
for i in range(len(VICSolQ3)):
  if VICSolQ3[i] != max(VICSolQ3):
    VICSolQ3Max.append(None)
  else:
    VICSolQ3Max.append(int(VICSolQ3[i]))

# Plot Line Graph
fig, ax = plt.subplots(2, 4)
fig.suptitle('Daily Average Demand Comparison and Solar PV Measurement Generation' + '\n' + ' between NSW and VIC for the Last 4 Quarters', fontsize=14)

# Q4 DEMAND 2019 SUBPLOT
ax1 = plt.subplot(2, 4, 1)
plt.plot(NSWDemQ4, '', VICDemQ4, '')
plt.xlabel('Q4 - 2019')
plt.ylabel('Load Demand, MW')
plt.legend(['NSW Demand', 'VIC Demand'], loc=8)
plt.scatter(x, NSWDemQ4Max, c='red')
plt.scatter(x, NSWDemQ4Min, c='green')
plt.scatter(x, VICDemQ4Max, c='red')
plt.scatter(x, VICDemQ4Min, c='green')
for i, txt in enumerate(NSWDemQ4Max):
    ax1.annotate(txt, (x[i], NSWDemQ4[i]), ha='center')
for i, txt in enumerate(NSWDemQ4Min):
    ax1.annotate(txt, (x[i], NSWDemQ4[i]))
for i, txt in enumerate(VICDemQ4Max):
    ax1.annotate(txt, (x[i], VICDemQ4[i]), ha='center')
for i, txt in enumerate(VICDemQ4Min):
    ax1.annotate(txt, (x[i], VICDemQ4[i]))
ax1.set_ylim([0, 11000])
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.set_xticks([])

# Q1 DEMAND 2020 SUBPLOT
ax2 = plt.subplot(2, 4, 2)
plt.plot(NSWDemQ1, '', VICDemQ1, '')
plt.xlabel('Q1 - 2020')
plt.title('                       Average Daily Demand over 48 30-minute Intervals', loc='left')
plt.scatter(x, NSWDemQ1Max, c='red')
plt.scatter(x, NSWDemQ1Min, c='green')
plt.scatter(x, VICDemQ1Max, c='red')
plt.scatter(x, VICDemQ1Min, c='green')
for i, txt in enumerate(NSWDemQ1Max):
    ax2.annotate(txt, (x[i], NSWDemQ1[i]), ha='center')
for i, txt in enumerate(NSWDemQ1Min):
    ax2.annotate(txt, (x[i], NSWDemQ1[i]))
for i, txt in enumerate(VICDemQ1Max):
    ax2.annotate(txt, (x[i], VICDemQ1[i]), ha='center')
for i, txt in enumerate(VICDemQ1Min):
    ax2.annotate(txt, (x[i], VICDemQ1[i]))
ax2.set_ylim([0, 11000])
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.set_xticks([])

# Q2 DEMAND 2020 SUBPLOT
ax3 = plt.subplot(2, 4, 3)
plt.plot(NSWDemQ2, '', VICDemQ2, '')
plt.xlabel('Q2 - 2020')
plt.scatter(x, NSWDemQ2Max, c='red')
plt.scatter(x, NSWDemQ2Min, c='green')
plt.scatter(x, VICDemQ2Max, c='red')
plt.scatter(x, VICDemQ2Min, c='green')
for i, txt in enumerate(NSWDemQ2Max):
    ax3.annotate(txt, (x[i], NSWDemQ2[i]), ha='center')
for i, txt in enumerate(NSWDemQ2Min):
    ax3.annotate(txt, (x[i], NSWDemQ2[i]))
for i, txt in enumerate(VICDemQ2Max):
    ax3.annotate(txt, (x[i], VICDemQ2[i]), ha='center')
for i, txt in enumerate(VICDemQ2Min):
    ax3.annotate(txt, (x[i], VICDemQ2[i]))
ax3.set_ylim([0, 11000])
ax3.spines['right'].set_visible(False)
ax3.spines['top'].set_visible(False)
ax3.set_xticks([])

# Q3 DEMAND 2020 SUBPLOT
ax4 = plt.subplot(2, 4, 4)
plt.plot(NSWDemQ3, '', VICDemQ3, '')
plt.xlabel('Q3 - 2020')
plt.scatter(x, NSWDemQ3Max, c='red')
plt.scatter(x, NSWDemQ3Min, c='green')
plt.scatter(x, VICDemQ3Max, c='red')
plt.scatter(x, VICDemQ3Min, c='green')
for i, txt in enumerate(NSWDemQ3Max):
    ax4.annotate(txt, (x[i], NSWDemQ3[i]), ha='center')
for i, txt in enumerate(NSWDemQ3Min):
    ax4.annotate(txt, (x[i], NSWDemQ3[i]))
for i, txt in enumerate(VICDemQ3Max):
    ax4.annotate(txt, (x[i], VICDemQ3[i]), ha='center')
for i, txt in enumerate(VICDemQ3Min):
    ax4.annotate(txt, (x[i], VICDemQ3[i]))
ax4.set_ylim([0, 11000])
ax4.spines['right'].set_visible(False)
ax4.spines['top'].set_visible(False)
ax4.set_xticks([])

# Q4 SOLAR 2019 SUBPLOT
ax5 = plt.subplot(2, 4, 5)
plt.plot(NSWSolQ4, '', VICSolQ4)
plt.xlabel('Q4 - 2019')
plt.ylabel('Actual Solar PV Measurement' + '\n' +'Generation, MW')
plt.legend(['NSW Solar PV Measurement Gen', 'VIC Solar PV Measurement Gen'], loc=10)
plt.scatter(x, NSWSolQ4Max, c='red')
plt.scatter(x, VICSolQ4Max, c='red')
for i, txt in enumerate(NSWSolQ4Max):
    ax5.annotate(txt, (x[i], NSWSolQ4[i]), ha='center')
for i, txt in enumerate(VICSolQ4Max):
    ax5.annotate(txt, (x[i], VICSolQ4[i]), ha='center')
ax5.set_ylim([0, 1550])
ax5.spines['right'].set_visible(False)
ax5.spines['top'].set_visible(False)
ax5.set_xticks([])

# Q1 SOLAR 2020 SUBPLOT
ax6 = plt.subplot(2, 4, 6)
plt.plot(NSWSolQ1, '', VICSolQ1)
plt.xlabel('Q1 - 2020')
plt.title('                Average Daily Solar PV Generation over 48 30-minute Intervals', loc='left')
ax6.set_ylim([0, 1550])
plt.scatter(x, NSWSolQ1Max, c='red')
plt.scatter(x, VICSolQ1Max, c='red')
for i, txt in enumerate(NSWSolQ1Max):
    ax6.annotate(txt, (x[i], NSWSolQ1[i]), ha='center')
for i, txt in enumerate(VICSolQ1Max):
    ax6.annotate(txt, (x[i], VICSolQ1[i]), ha='center')
ax6.set_ylim([0, 1550])
ax6.spines['right'].set_visible(False)
ax6.spines['top'].set_visible(False)
ax6.set_xticks([])

# Q2 SOLAR 2020 SUBPLOT
ax7 = plt.subplot(2, 4, 7)
plt.plot(NSWSolQ2, '', VICSolQ2)
plt.xlabel('Q2 - 2020')
ax7.set_ylim([0, 1550])
plt.scatter(x, NSWSolQ2Max, c='red')
plt.scatter(x, VICSolQ2Max, c='red')
for i, txt in enumerate(NSWSolQ2Max):
    ax7.annotate(txt, (x[i], NSWSolQ2[i]), ha='center')
for i, txt in enumerate(VICSolQ2Max):
    ax7.annotate(txt, (x[i], VICSolQ2[i]), ha='center')
ax7.set_ylim([0, 1550])
ax7.spines['right'].set_visible(False)
ax7.spines['top'].set_visible(False)
ax7.set_xticks([])

# Q3 SOLAR 2020 SUBPLOT
ax8 = plt.subplot(2, 4, 8)
plt.plot(NSWSolQ3, '', VICSolQ3)
plt.xlabel('Q3 - 2020')
ax8.set_ylim([0, 1550])
plt.scatter(x, NSWSolQ3Max, c='red')
plt.scatter(x, VICSolQ3Max, c='red')
for i, txt in enumerate(NSWSolQ3Max):
    ax8.annotate(txt, (x[i], NSWSolQ3[i]), ha='center')
for i, txt in enumerate(VICSolQ3Max):
    ax8.annotate(txt, (x[i], VICSolQ3[i]), ha='center')
ax8.set_ylim([0, 1550])
ax8.spines['right'].set_visible(False)
ax8.spines['top'].set_visible(False)
ax8.set_xticks([])

plt.show()


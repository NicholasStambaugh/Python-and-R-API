import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import time
import seaborn as sns



#style of graphs
plt.style.use('fivethirtyeight')
pd.set_option('max_columns', 500)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]

from fredapi import Fred

#API key
fred_key = 'enter your key'

#establish key
fred = Fred(api_key=fred_key)

#searching for economic data
sp_search = fred.search('S&P', order_by='popularity')

#view columns
sp_search.head()

#plotting SP500 from 2013
sp500 = fred.get_series(series_id='SP500')
sp500.plot(figsize=(10, 5), title='S&P 500', lw=2)
plt.show()

#plotting GDP
gdp = fred.get_series(series_id='GDP')
gdp.plot(figsize=(10, 5), title='GDP', lw=2)
plt.show()

#plotting world currency
cur = fred.get_series(series_id='WCURCIR')
cur.plot(figsize=(10, 5), title='World Currency', lw=2)
plt.show()

#merging datasets
gdp.name = "gdp"
cur.name = "cur"
df1 = pd.merge(gdp, cur, left_index=True, right_index=True)
df1

#plotting currency against gdp using seaborn
sns.set_theme()
sns.lmplot(data=df1, x="gdp", y="cur")
plt.show()

#pull unemployment rate
unemp_df = fred.search('unemployment rate state', filter=('frequency','Monthly'))
unemp_df = unemp_df.query('seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"')
unemp_df = unemp_df.loc[unemp_df['title'].str.contains('Unemployment Rate')]



#unemployed by state
ax = uemp_states.loc[uemp_states.index == '2022-08-01'].T \
    .sort_values('2022-08-01') \
    .plot(kind='barh', figsize=(8, 12), width=0.7, edgecolor='black',
          title='Unemployment Rate by State, August 2022')
ax.legend().remove()
ax.set_xlabel('% Unemployed')
plt.show()

#pull participation rate
part_df = fred.search('participation rate state', filter=('frequency','Monthly'))
part_df = part_df.query('seasonal_adjustment == "Seasonally Adjusted" and units == "Percent"')

part_id_to_state = part_df['title'].str.replace('Labor Force Participation Rate for ','').to_dict()

all_results = []

for myid in part_df.index:
    results = fred.get_series(myid)
    results = results.to_frame(name=myid)
    all_results.append(results)
    time.sleep(0.1) # Don't request to fast and get blocked
part_states = pd.concat(all_results, axis=1)
part_states.columns = [part_id_to_state[c] for c in part_states.columns]


#unemployment against participation rate
state = 'Michigan'
fig, ax = plt.subplots(figsize=(10, 5), sharex=True)
ax2 = ax.twinx()
uemp_states2 = uemp_states.asfreq('MS')
l1 = uemp_states2.query('index >= 2021 and index < 2022')[state] \
    .plot(ax=ax, label='Unemployment')
l2 = part_states.dropna().query('index >= 2021 and index < 2022')[state] \
    .plot(ax=ax2, label='Participation', color=color_pal[3])
ax2.grid(False)
ax.set_title(state)
fig.legend(labels=['Unemployment','Participation'])
plt.show()

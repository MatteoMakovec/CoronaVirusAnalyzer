import pandas as pd
import matplotlib.pyplot as plt



url = "https://data.humdata.org/dataset/novel-coronavirus-2019-ncov-cases"
confirmed = pd.read_csv('externalSources/covid19_confirmed.csv')
deaths = pd.read_csv('externalSources/covid19_deaths.csv')
recovered = pd.read_csv('externalSources/covid19_recovered.csv')

confirmed = confirmed.drop(['Province/State', 'Lat', 'Long'], axis=1)
deaths = deaths.drop(['Province/State', 'Lat', 'Long'], axis=1)
recovered = recovered.drop(['Province/State', 'Lat', 'Long'], axis=1)

confirmed = confirmed.groupby(confirmed['Country/Region']).aggregate('sum')
deaths = deaths.groupby(deaths['Country/Region']).aggregate('sum')
recovered = recovered.groupby(recovered['Country/Region']).aggregate('sum')

confirmed = confirmed.T
deaths = deaths.T
recovered = recovered.T

#Compute new cases
new_cases = confirmed.copy()
for day in range (1, len(confirmed)):
    new_cases.iloc[day] = confirmed.iloc[day] - confirmed.iloc[day-1]

#Compute growth rate
growth_rate = confirmed.copy()
for day in range (1, len(confirmed)):
    growth_rate.iloc[day] = (new_cases.iloc[day] - confirmed.iloc[day-1])*100

#Compute active cases
active_cases = confirmed.copy()
for day in range (0, len(confirmed)):
    active_cases.iloc[day] = confirmed.iloc[day] - deaths.iloc[day] - recovered.iloc[day]

#Compute overall growth rate
overall_growth_rate = confirmed.copy()
for day in range (1, len(confirmed)):
    overall_growth_rate.iloc[day] = ((active_cases.iloc[day] - active_cases.iloc[day-1]) / active_cases.iloc[day-1])*100

#Compute death rate
death_rate = confirmed.copy()
for day in range (1, len(confirmed)):
    death_rate.iloc[day] = (death_rate.iloc[day] - confirmed.iloc[day])*100


####        VISUALIZATION        ###
countries = ['Italy', 'France', 'United Kingdom', 'US', 'China', 'Germany']

ax = plt.subplot()
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.set_title('Covid-19 - Total Cases Growth Rate', color='white')

for country in countries:
    overall_growth_rate[country].plot(label=country)

plt.legend(loc='upper left')
plt.show()
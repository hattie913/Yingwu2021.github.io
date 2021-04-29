# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 17:02:26 2021

@author: hatti
"""

import pandas as pd
from sodapy import Socrata


tokenID = 'JcQWnC7xw1VPRl8Z87EDxhYd6'
username = "wu_ying@bentley.edu"
password = 'Wu913520'

# get statewise covid19 cases from CDC.gov
client = Socrata('data.cdc.gov',tokenID, username,password)

url = 'https://data.cdc.gov/resource/9mfq-cb36.json'
covid = client.get_all('9mfq-cb36',select = 'submission_date,state,tot_cases,new_case,conf_cases,new_death,conf_death')

              
covidCases_df= pd.DataFrame.from_records(covid)


covidCases_df = covidCases_df[covidCases_df.submission_date>'2020-12-01']  # submission_date is str....?
covidCases_df =covidCases_df.set_index(covidCases_df.submission_date).drop(columns= 'submission_date')
# check if there are missing values in new_case:
newCase_nan = covidCases_df.new_case.isna().any()  # False!


covidCases_df = covidCases_df.fillna(value = 0)
# add info of 'NYC' to 'NY'
covidCases_df[['new_case', 'tot_cases','new_death','conf_death','conf_cases']]=covidCases_df[['new_case', 'tot_cases','new_death','conf_death','conf_cases']].apply(pd.to_numeric)
allNY = covidCases_df[covidCases_df.state.isin(['NY','NYC'])]
# sum all ny and nyc values group by the same date to get the entire NY state number
nyCases= allNY.groupby(allNY.index).sum()
nyCases['state'] = 'NY'

#delete data with ny and nyc first:
notNY =covidCases_df[~covidCases_df.state.isin(['NY','NYC'])]
# add the modified data of NY to the orginal dataframe:
stateCases_df =notNY.append(nyCases)


# get vaccine dataset:
vaccine_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv'
vaccine =pd.read_csv(vaccine_url,error_bad_lines=False)  # start from 2020-12-20
vaccine= vaccine[['date','location','total_vaccinations','daily_vaccinations','daily_vaccinations_per_million',
                   'people_fully_vaccinated','people_fully_vaccinated_per_hundred']]

#vaccine.loc[:,'date']= pd.to_datetime(vaccine.date,format = '%Y-%m-%d')
vaccine_df = vaccine.set_index(vaccine.date).drop(columns = 'date')

# only include location of the states names 
usVaccine = vaccine[~vaccine.location.isin(['Bureau of Prisons','Dept of Defense','Indian Health Svc', 'Long Term Care', 
                                           'Veterans Health','United States'])]



us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Federated States of Micronesia': 'FSM',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Martial Islands': 'RMI',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York State': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Republic of Palau':'PW',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'}

state_abbv = pd.DataFrame(list(us_state_abbrev.items()))
state_abbv.rename(columns = {0:'location',1:'state'},inplace = True)
#merge with state_abbv
stateVaccine = pd.merge(usVaccine,state_abbv)
stateCases_df2 = stateCases_df.reset_index()
stateCases_df2 = stateCases_df2.rename(columns = {'submission_date':'date'})
# format the date to be the same format as usVaccine.date (delete: 'T00:00:00:00.000')
stateCases_df2.date = stateCases_df2.date.str[0:-13]



vaccine_cases = pd.merge(stateCases_df2,stateVaccine,on = ['state','date'])

stateList = ['CA','TX','FL','NY','PA','IL','OH','GA','NC','MI','MA']
statesCovid = vaccine_cases[vaccine_cases.state.isin(stateList)]

statesCovid =statesCovid.drop(columns = ['total_vaccinations','conf_death','conf_cases','people_fully_vaccinated',
                                         'people_fully_vaccinated_per_hundred'])
statesCovid = statesCovid.sort_index()
statesCovid = statesCovid.fillna(0)
statesCovid.rename(columns = {'date':'Date','state':'State Abbv','new_case':'New Case','new_death':'New Death',
                              'daily_vaccinations':'Daily Vaccinations','daily_vaccinations_per_million':'Daily Vaccinations/million',
                              'location':'State','tot_cases':'Total Cases'},inplace = True)

#statesCovid['Date'] = pd.to_datetime(statesCovid['Date'],format = '%Y-%m-%d')
statesCovid = statesCovid[['Date','State','Total Cases','New Case','New Death', 
       'Daily Vaccinations', 'Daily Vaccinations/million']]


statesCovid.to_pickle('covidproject.pkl')



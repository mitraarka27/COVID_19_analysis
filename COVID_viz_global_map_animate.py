# -*- coding: utf-8 -*-
"""
Author: Arka Mitra
13th March 2020, 8:00pm, 
Champaign, Illinois, USA

Data is sourced from:  
Center for Systems Science and Engineering (JHU CSSE).
Johns Hopkins University, freely availbale on GitHub.
https://github.com/CSSEGISandData/COVID-19
"""

import io
import csv
import glob
import datetime
import plotly
import pandas as pd
import numpy as np
import urllib.request
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.offline import plot
from datetime import date, timedelta
import plotly.graph_objects as go
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML


def get_data_from_CSSE_Github():
    covid19_con_url = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
    covid19_x_url = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
    covid19_rec_url = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
    covid_con_data = pd.read_csv(covid19_con_url, header=0, keep_default_na=False, na_values={"Province/State" : "foo"})
    covid_x_data = pd.read_csv(covid19_x_url, header=0, keep_default_na=False, na_values={"Province/State" : "foo"})
    covid_rec_data = pd.read_csv(covid19_rec_url, header=0, keep_default_na=False, na_values={"Province/State" : "foo"})
#    without_provinces = covid_data[covid_data['Province/State'] == '']
#    with_provinces = covid_data[covid_data['Province/State'] != '']
#    country_with_provinces = np.unique(with_provinces['Country/Region'])
#    country_without_provinces = np.unique(without_provinces['Country/Region'])
    return covid_con_data, covid_x_data, covid_rec_data

covid_con_data, covid_x_data, covid_rec_data = get_data_from_CSSE_Github()
covid_confirmed = covid_con_data.melt(id_vars=covid_con_data.columns[:4],
                                 var_name="Date", value_name="Cases")
covid_deaths = covid_x_data.melt(id_vars=covid_x_data.columns[:4],
                                 var_name="Date", value_name="Cases")
covid_recovered = covid_rec_data.melt(id_vars=covid_rec_data.columns[:4],
                                 var_name="Date", value_name="Cases")


indexes = np.unique(covid_confirmed['Date'], return_index=True)[1]
dates = [covid_confirmed['Date'][index] for index in sorted(indexes)]
#last_date = covid_confirmed['Date'][len(covid_confirmed)-1]
#dff = covid_confirmed[covid_confirmed['Date'].eq(last_date)].\
#        sort_values(by='Cases', ascending=False).head(10)
##dff['alert'] = [i for i in range(0,len(dff))]
#dff = dff.rename(columns={'Cases':'Confirmed'})
#top_countries = dff['Country/Region']
#dff1 = covid_recovered[covid_recovered['Date'].eq(last_date)]
#dff1 = dff1[dff1['Country/Region'].eq(top_countries)]
#dff1 = dff1.rename(columns={'Cases':'Recovered'})
#dff2 = covid_deaths[covid_deaths['Date'].eq(last_date)]
#dff2 = dff2[dff2['Country/Region'].eq(top_countries)]
#dff2 = dff2.rename(columns={'Cases':'Deaths'})
#dff = pd.merge(dff, dff1, how='left', on=['Province/State', 'Country/Region',
#                                             'Lat', 'Long', 'Date'])
#dff = pd.merge(dff, dff2, how='left', on=['Province/State', 'Country/Region',
#                                             'Lat', 'Long', 'Date'])
    
_X = np.arange(10)
fig, ax = plt.subplots(figsize=(15, 8))
#ax.barh(_X-0.2, dff['Confirmed'],height=0.2,color='yellow',label='Confirmed')
#ax.barh(_X, dff['Recovered'],height=0.2,color='green',label='Recovered')
#ax.barh(_X+0.2, dff['Deaths'],height=0.2,color='red',label='Deaths')
#
#ax.set(yticks=_X, yticklabels=dff['Country/Region'], ylim=[2*0.2 - 1, len(dff)])
#ax.legend(fontsize=13)

def draw_barchart(date_n):
    last_date = dates[date_n]
    print(last_date)
    dff = covid_confirmed[covid_confirmed['Date'].eq(last_date)].\
            sort_values(by='Cases', ascending=False).head(10)
    #dff['alert'] = [i for i in range(0,len(dff))]
    dff = dff.rename(columns={'Cases':'Confirmed'})
    top_countries = dff['Country/Region']
    dff1 = covid_recovered[covid_recovered['Date'].eq(last_date)]
    dff1 = dff1[dff1['Country/Region'].eq(top_countries)]
    dff1 = dff1.rename(columns={'Cases':'Recovered'})
    dff2 = covid_deaths[covid_deaths['Date'].eq(last_date)]
    dff2 = dff2[dff2['Country/Region'].eq(top_countries)]
    dff2 = dff2.rename(columns={'Cases':'Deaths'})
    dff = pd.merge(dff, dff1, how='left', on=['Province/State', 'Country/Region',
                                                 'Lat', 'Long', 'Date'])
    dff = pd.merge(dff, dff2, how='left', on=['Province/State', 'Country/Region',
                                                 'Lat', 'Long', 'Date'])
    ax.clear()
    ax.barh(_X-0.2, dff['Confirmed'],height=0.2,color='yellow',label='Confirmed')
    ax.barh(_X, dff['Recovered'],height=0.2,color='green',label='Recovered')
    ax.barh(_X+0.2, dff['Deaths'],height=0.2,color='red',label='Deaths')
    dx = dff['Confirmed'].max() / 20
    for i, (value, name) in enumerate(zip(dff['Confirmed'], dff['Country/Region'])):
#        ax.text(value+dx, i,     name,           size=12, weight=600, ha='right', va='bottom')
#        ax.text(value-dx, i-.25, group_lk[name], size=10, color='#444444', ha='right', va='baseline')
        ax.text(value+dx, i,  f'{value:,.0f}',  size=12, ha='right',  va='center')
    # ... polished styles
    ax.text(0.7, 0.6, str(datetime.datetime.strptime(dff['Date'][0], '%m/%d/%y').strftime('%B %d, %Y')),
            transform=ax.transAxes, color='#777777', size=30, ha='right', weight=600)
    ax.text(0, 1.06, 'Population', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
#    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0.1, 1.08, 'COVID-19 : Top 10 most affected places globally (by day)',
            transform=ax.transAxes, size=18, weight=500, ha='left')
    ax.text(1, 0, '', transform=ax.transAxes, ha='right',
            color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    ax.set(yticks=_X, yticklabels=dff['Country/Region']+'\n'+dff['Province/State'], ylim=[2*0.2 - 1, len(dff)])
    ax.legend(fontsize=13)
#    ax.tick_params(axis="y", labelsize=12, weight='bold')
    plt.box(False)
    
#draw_barchart(covid_confirmed['Date'][len(covid_confirmed)-1])
fig, ax = plt.subplots(figsize=(15, 8))
animator = animation.FuncAnimation(fig, draw_barchart,frames=range(len(dates)))
#HTML(animator.save('COVID19_top10_nations')) 
animator.save('COVID19_top10_nations.gif', fps=0.5)

plt.show()

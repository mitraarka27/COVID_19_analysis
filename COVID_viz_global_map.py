# -*- coding: utf-8 -*-
"""
Author: Arka Mitra
20th March 2020, 4:00pm, 
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
import imageio
import pandas as pd
import numpy as np
import urllib.request
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.offline import plot
from datetime import date, timedelta
import plotly.graph_objects as go


def get_data_from_CSSE_Github(date):
    covid19_daily_data_url = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_daily_reports/"
    url = covid19_daily_data_url+str(date)+".csv"
    covid_data = pd.read_csv(url, header=0, keep_default_na=False, na_values={"Province/State" : "foo"})
#    without_provinces = covid_data[covid_data['Province/State'] == '']
#    with_provinces = covid_data[covid_data['Province/State'] != '']
#    country_with_provinces = np.unique(with_provinces['Country/Region'])
#    country_without_provinces = np.unique(without_provinces['Country/Region'])
    return covid_data

def plot_frame_from_data(covid_data, d):
    limits = [(0,1),(1,5),(5,10),(10,50),(50,100),(100,200),(200,1000)]
    #colors = ["seagreen","yellow","orange","orangered","red","crimson","darkred"]
    colors = ["darkred","crimson","red","orangered","orange","yellow","seagreen"]
    fig = go.Figure(go.Scattergeo())
    fig.update_geos(
        visible=False, resolution=50,showland=True,
        showocean=True,bgcolor="lightgrey",
        landcolor="grey",oceancolor="lightblue",
        showcountries=True, countrycolor="black"
    )
    #fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
    for i in range(len(limits)):
        lim = limits[i]
        df_sub = covid_data[lim[0]:lim[1]]
        fig.add_trace(go.Scattergeo(
            lon = df_sub['Longitude'],
            lat = df_sub['Latitude'],
#            text = df_sub['Country/Region']+', '+df_sub['Province/State']+ 
#            '<br>Confirmed cases = '+df_sub['Confirmed'].astype(str)+
#            '<br>Fatal cases = '+df_sub['Deaths'].astype(str)+
#            '<br>Recovery cases = '+df_sub['Recovered'].astype(str),
#            text = 'by @mitraarka27 (Arka Mitra); credit: JHU CSSE GitHub',
#            textposition = 'bottom right',
            marker = dict(
                size = df_sub['Confirmed']/10,
                color = colors[i],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode = 'area'
            ),
            name = '{0} - {1}'.format(lim[0],lim[1])))
    fig.update_layout(title_text = 'Relative spread of COVID-19 Infections by Country/Region'+
                      '<br>Date : '+datetime.datetime.strptime(d,'%m-%d-%Y').strftime('%B %d, %Y'),
                      legend_title='<b> People affected </b>',
            showlegend = False,
            geo = dict(
                scope = 'world',
                landcolor = 'rgb(217, 217, 217)',
            ),
        annotations=[
            go.layout.Annotation(
                text='by @mitraarka27 (Arka Mitra); credit: JHU CSSE GitHub',
                align='left',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=1.,
                y=0.,
                bordercolor='black',
                borderwidth=1
        )]
      )      
#    plot(fig)
    fig.write_image('COVID19_'+str(d)+'.jpeg')
    
images=[]
start_date = date(2020, 3, 1)
end_date = date(2020, 3, 19)
delta = timedelta(days=1)
while start_date <= end_date:
    print (start_date.strftime("%m-%d-%Y"))
    covid_data = get_data_from_CSSE_Github(start_date.strftime("%m-%d-%Y"))
    plot_frame_from_data(covid_data, start_date.strftime("%m-%d-%Y"))
    images.append(imageio.imread('COVID19_'+str(start_date.strftime("%m-%d-%Y"))+'.jpeg'))
    start_date += delta
imageio.mimsave('COVID19_global_spread_ts.gif', images , fps=0.8)

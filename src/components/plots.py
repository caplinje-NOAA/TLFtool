# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:53:59 2023
This module handles the rendering of SSP data
@author: jim
"""

# dash imports
from dash import dcc, html

# 
import numpy as np

# plotting imports
import plotly.express as px
import plotly.graph_objects as go

from . import ids


# initial figure
linFigure = html.Div(dcc.Graph(figure=go.Figure(),id=ids.LIN_PLOT,style={ 'height': '50vh'}))

# just plot the inputs as they are entered
def plotInputs(df):
    #ridiculous range setting
    minL,maxL = np.min(df['level'].values),np.max(df['level'].values)
    offset = (maxL-minL)*0.1
    yRange = [minL-offset,maxL+offset]
    fig = go.Figure()
    fig.add_trace(go.Scatter(mode="markers", x=df["range_m"], y=df["level"] ))

    fig.update_xaxes(type="log")

    fig.update_layout(
        # title="Plot Title",
        xaxis_title='Range (m)',
        yaxis_title='Level (dB)',
        # legend_title="Legend Title",
        font=dict(
        #  family="Courier New",
        size=12,
        # color="RebeccaPurple"
        ),
        yaxis_range=yRange

      )
    
    return fig

# plot all of the fits
def plotFit(df,fits, confBands=True):
    #ridiculous range setting
    minL,maxL = np.min(fits[0].levels_fit),np.max(fits[0].levels_fit)
    offset = (maxL-minL)*0.1
    yRange = [minL-offset,maxL+offset]
    fig = go.Figure()
    
    colors = ["blue","magenta","green"]
    for i,fit in enumerate(fits):
        
        if confBands:
            fig.add_trace(go.Scatter(x=fit.ranges_fit,y=fit.conf_lower, fill=None, mode='lines',line_color=colors[i],showlegend=False))
            fig.add_trace(go.Scatter(x=fit.ranges_fit,y=fit.conf_upper, fill='tonexty', mode='lines',line_color=colors[i],name='confidence interval'))
        fig.add_trace(go.Scatter(mode="lines",x =fit.ranges_fit,y=fit.levels_fit,name=fit.label,line_color=colors[i]))
    
    fig.add_trace(go.Scatter(mode="markers", x=df["range_m"], y=df["level"],name='data',line_color='red'))
    fig.update_xaxes(type="log")

    fig.update_layout(
        # title="Plot Title",
        xaxis_title='Range (m)',
        yaxis_title='Level (dB)',
        # legend_title="Legend Title",
        font=dict(
        #  family="Courier New",
        size=12,
        # color="RebeccaPurple"
        ),
        yaxis_range=yRange

      )
    
    return fig







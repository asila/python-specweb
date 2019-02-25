# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 15:35:28 2019

@author: JWKigo
"""
import opusFC
import pandas as pd
import numpy as np

import base64
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table_experiments as dte
from dash.dependencies import Input, Output
import dash
import pandas as pd
import io
import seaborn as sns



app = dash.Dash()

app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([

    html.H1(children="Dash"),
    
   
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            html.A('upload File')
        ]),



        style={
           'width': '100px',
            'height': '40px',
            'lineHeight': '35px',
            'backgroundColor': '#287c28',
            'fontsize' : '24px',
            'textAlign': 'left',
            'margin': '1px',
            'padding':'2px',
           
            
        },

    ),
  html.Br(),
    html.H5("Dash Table"),
    html.Div(dte.DataTable(rows=[{}], id='table')),
    html.Br(),
    
  
    

    ])


# file upload function
def parse_contents(contents, filename):
    content_type, content_string = contents
    
    SNM = []
    INS = []
    DAT = []
    TIM = []
    #EXP = []
    DUR = []
    CNM = []
    RES = []
    ZFF = []
    NPT = []
    LWN = []
    LXV = []
    FXV = []
    minY = []
    maxY= []   

    
    for f in filename:
        try:
            decoded = base64.b64decode(content_string)
            blocks= opusFC.listContents(decoded)
            data= opusFC.getOpusData(decoded, blocks[0])

            SNM.append(data.parameters['SNM'])
            INS.append(data.parameters['INS'])
            DAT.append(data.parameters['DAT'])
            TIM.append(data.parameters['TIM'])
            DUR.append(data.parameters['DUR'])
            CNM.append(data.parameters['CNM'])
            RES.append(data.parameters['RES'])
            ZFF.append(data.parameters['ZFF'])
            NPT.append(data.parameters['NPT'])
            LWN.append(data.parameters['LWN'])
            FXV.append(data.parameters['FXV']) 
            LXV.append(data.parameters['LXV'])
            minY.append(data.minY)
            maxY.append(data.maxY)

            varnames = 'SNM', 'Instrument', 'Scan_date', "Time", "Duration", "Operator", "Resolution", "Zero_filling_Factor", "Number_points", "Laser_Wavenumber", "Wavenumber_one", "Wavenumber_last", "Min_absorbance", "Max_Absorbance"

            metadata1 = np.vstack((SNM, INS, DAT, TIM, DUR, CNM, RES, ZFF, NPT, LWN, FXV, LXV, minY, maxY)).T


            df = pd.DataFrame(metadata1, columns=varnames)
        except Exception as e:
            print(e)
        return None
    return df
#%%
# callback table creation
@app.callback(Output('table', 'rows'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_output(contents, filename):
    if contents is not None:
        df = parse_contents(contents, filename)
        if df is not None:
           
            return df.to_dict('records')
        else:
            return [{}]
    else:
        return [{}]
    
    app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == '__main__':
    app.run_server(debug=True,port=213)

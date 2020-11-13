# -*- coding: utf-8 -*-

import pandas as pd
import plotly.express as px
import os
import plotly

if not os.path.exists("images"):
    os.mkdir("images")

path = 'D:\WB_LOG'
output_path = 'D:\WB_LOG\LOG'
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        full_path = os.path.join(root, name)
        project_name = root.split(os.path.sep)[-2]
        panel_name = root.split(os.path.sep)[-1]
        print(project_name,panel_name)
        if not os.path.exists(output_path + project_name):
            os.mkdir(output_path + project_name)
        if not os.path.exists(output_path + project_name + '/' + panel_name):
            os.mkdir(output_path + project_name + '/' + panel_name)
            
        
        df = pd.read_csv(full_path)
        
        fig_cool = px.scatter(df, x = 'COOL-u', y = 'COOL-v', title='u-v graph for ' + name)
        fig_standard = px.scatter(df, x = 'STANDARD-u', y = 'STANDARD-v', title='u-v graph for ' + name)
        fig_warm = px.scatter(df, x = 'WARM-u', y = 'WARM-v', title='u-v graph for ' + name)
        plotly.offline.plot(fig_cool, filename = output_path + project_name + '/' + panel_name + '/' + panel_name + '_COOL.html', auto_open=False)
        plotly.offline.plot(fig_standard, filename = output_path + project_name + '/' + panel_name + '/' + panel_name + '_STANDARD.html', auto_open=False)
        plotly.offline.plot(fig_warm, filename = output_path + project_name + '/' + panel_name + '/' + panel_name + '_WARM.html', auto_open=False)

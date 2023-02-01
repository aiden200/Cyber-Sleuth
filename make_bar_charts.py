# %% 
import os
import pandas as pd
import numpy as np
import chart_studio.plotly as py
import cufflinks as cf
# import seaborn as sns # shaun: delete later because this just gives me datasets to play with
import plotly.express as px
import plotly.graph_objects as go
from glob import glob
# import csv




# %%
def add_headers_to_profiles():
    header_list = ["ip_address", "frequency_percentage"]
    ip_profiles = map(os.path.basename, glob("ip_profiles/*"))
    for profile in ip_profiles:
        df = pd.read_csv(f"ip_profiles/{profile}", header=None)
        df.rename(columns={0: 'ip_address', 1: 'frequency_percentage'}, inplace=True)
        df.to_csv(f"ip_profiles/{profile}", index=False) # save to new csv file
   

add_headers_to_profiles()

# %%
def make_charts():
    if not os.path.exists("bar_charts"):
        os.mkdir("bar_charts")
    exclusions = {"background.csv":None, "chrome.csv":None, "google.csv":None} #TODO: make it so I'm working only with final path name
    ip_profiles = map(os.path.basename, glob("ip_profiles/*"))
    cols = ["ip_address", "frequency_percentage"]
    for profile in ip_profiles:
        if profile in exclusions:
            continue
        df = pd.read_csv(f"ip_profiles/{profile}", names=cols, header=None)
        fig = px.bar(df, x="ip_address", y="frequency_percentage",
                   title="IP Address Frequency",
                   labels={
                    "ip_address" : "IP Address",
                    "frequency_percentage" : "Percentage of Times IP Address was Present in Each Trace"}
                    )
        fig.update_xaxes(categoryorder='category ascending')
        fig.show()
        fig.write_image(f"bar_charts/{profile}fig.jpeg")  
        

make_charts()


# %%
'''
 # is_header = not any(cell.isdigit() for cell in df[0])
        # print("is_header?: ", is_header)
        # if not is_header:
            # print("entered if case")

def add_headers_to_profiles():
    header_list = ["ip_address", "frequency_percentage"]
    ip_profiles = map(os.path.basename, glob("ip_profiles/*"))
    for profile in ip_profiles:
        df = pd.read_csv(f"ip_profiles/{profile}", header=None)
        df.to_csv(f"ip_profiles/{profile}" cols=header_list, index=False)
        # file.to_csv("gfg2.csv", header=headerList, index=False)

add_headers_to_profiles()

# df = pd.read_csv(f"ip_profiles/{profile}", header=None)
# df.rename(columns={0: 'ip_address', 1: 'frequency_percentage'}, inplace=True)
# df.to_csv(f"ip_profiles/{profile}", index=False) # save to new csv file
'''






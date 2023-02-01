


# %% 
import os
import pandas
import pandas as pd
import numpy as np
import chart_studio.plotly as py
import cufflinks as cf
# import seaborn as sns # shaun: delete later because this just gives me datasets to play with
import plotly.express as px
import plotly.graph_objects as go
# import kaleido
%matplotlib inline


from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline()

x = "wazzup"
"hello"


# %%
df = pd.read_csv('ip_addresses_frequency.csv')
df.head()
fig = px.histogram(df, x="ip_addresses", y="frequency",
                   title="Count of Each IP Address in Trace",
                   labels={
                    "ip_addresses" : "IP Address",
                    "frequency" : "Count"}
                    )
fig.update_layout(yaxis_title = "Count")
fig.update_xaxes(categoryorder='category ascending')
fig.show()

# %%
if not os.path.exists("images"):
    os.mkdir("images")
fig.write_image("images/fig.jpeg")


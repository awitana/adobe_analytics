#importing files Client and ReportDefinition from the adobe_analytics python library https://github.com/SaturnFromTitan/adobe_analytics
from adobe_analytics import Client, ReportDefinition

#setting client to Avi's username and secret (from Adobe Analytics User Management)
client = Client('username', 'secret')


#setting suite to global report suite rsid (report suite ID)
suites = client.suites()
suite = suites['fairfaxnz-stuffoverall-production']

#importing python libraries (already installed via UI)
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

#setting library options
#allowing pandas to display all columns of a dataframe for print()
pd.set_option('display.max_columns', None)

#can be used to generate a list of available metrics, dimensions and segments if this report needs to be updated
#print(suite.metrics())
#print(suite.dimensions())
#print(suite.segments())

#definining a function to run a report for
    #dimensions - prop2(Site Section)
    #metrics - visitors, visits, page views, event22(Article View)
    #segments - domestic traffic (country = NZ)
    #granularity = day

report_definition = ReportDefinition(
    dimensions=[
        {"id":"prop2","top":50},
    ],
    metrics=[
        "visitors",
        "visits",
        "pageviews",
        "event22",
    ],
    segments=[
        "s200000657_5a5e8295b9b6c367461ff88f",
    ],
    date_from="2018-08-01",
    date_to="2018-08-31",
    granularity = "day"
)

#saving output of report_definition function in dataframe and converting columns to numeric where applicable
df = suite.download(report_definition)
df = df.apply(pd.to_numeric, errors='ignore')

#creating subset dataframes
national_df = df[df["Site Section"] == "national"]
lifestyle_df = df[df["Site Section"] == "life-style"]
business_df = df[df["Site Section"] == "business"]
sport_df = df[df["Site Section"] == "sport"]

#plotting linegraphs
#plotting individual dataframes x = date(converted from string to datetime and date extracted) vs y = page views
plt.plot([datetime.strptime(d,"%Y-%m-%d %H:%M:%S").date() for d in national_df["Datetime"]],national_df["Page Views"])
plt.plot([datetime.strptime(d,"%Y-%m-%d %H:%M:%S").date() for d in lifestyle_df["Datetime"]],lifestyle_df["Page Views"])
plt.plot([datetime.strptime(d,"%Y-%m-%d %H:%M:%S").date() for d in business_df["Datetime"]],business_df["Page Views"])
plt.plot([datetime.strptime(d,"%Y-%m-%d %H:%M:%S").date() for d in sport_df["Datetime"]],sport_df["Page Views"])
#creating legend for graphs and location for legend
plt.legend(["national", "life-style", "business", "sport"], loc='upper left')
#formatting x axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d/%Y"))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.gcf().autofmt_xdate()
#plotting graph
plt.show()

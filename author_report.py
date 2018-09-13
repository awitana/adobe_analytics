#importing files Client and ReportDefinition from the adobe_analytics library
from adobe_analytics import Client, ReportDefinition

#importing plotting libraries
from plotly import figure_factory as ff
import plotly
import pandas as pd

client = Client('username', 'shared secret')
suites = client.suites()
suite = suites['fairfaxnz-stuffoverall-production']

#returning a list of available metrics, dimensions and segments
#print(suite.metrics())
#print(suite.dimensions())
#print(suite.segments())

#definining a function to run a report for
#dimensions - prop61(content ID+title), prop64(author)
#metrics - unique visitors, page views
#segments - domestic traffic nz, life & style site section
#pass in additional values with kwargs

report_definition = ReportDefinition(
    dimensions=[
        {"id": "prop61", "top": 10},
        {"id": "prop64", "top": 10},
    ],
    metrics=[
        "totalvisitorsdaily",
        "pageviews"
    ],
    segments=[
        "s200000657_5a5e8295b9b6c367461ff88f",
        "s200000657_5ac55314b9b6c31f7ea86815",
    ],
    date_from="2018-09-10",
    date_to="2018-09-10",
)

#saving output of report_definition function in dataframe
dataframe = suite.download(report_definition)

#sorting values by page views
dataframe = dataframe.apply(pd.to_numeric, errors='ignore')
dataframe = dataframe.sort_values(by='Page Views', ascending=False)

#creating and plotting table
table = ff.create_table(dataframe)
plotly.offline.plot(table, filename='table.html')


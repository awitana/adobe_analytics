#importing files Client and ReportDefinition from the adobe_analytics library
from adobe_analytics import Client, ReportDefinition

#enter your username and shared secret (from Adobe Analytics User Management)
client = Client('username', 'shared secret')
suites = client.suites()
#global report suite
suite = suites['fairfaxnz-stuffoverall-production']

#importing python libraries (already installed via UI)
import pandas as pd
pd.set_option('display.max_columns', None)
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import numpy as np

#returning a list of available metrics, dimensions and segments
#print(suite.metrics())
#print(suite.dimensions())
#print(suite.segments())

#definining a function to run a report for
#dimensions - prop45(Device ID), evar131(AB Testing Segment)
#metrics - visits, page views, event22(Article View)
#segments - platform = ios & android apps


report_definition = ReportDefinition(
    dimensions=[
        {"id":"prop45","top":100},
        {"id":"evar131","top":1},
    ],
    metrics=[
        "visits",
        "pageviews",
        "event22",
    ],
    segments=[
        "s200000657_5acd2e79e16ac06b09e0138b",
    ],
    date_from="2018-07-01",
    date_to="2018-07-31",
)

#saving output of report_definition function in dataframe
df = suite.download(report_definition)

#drop na and device id = 000....
df = df.apply(pd.to_numeric, errors='ignore')
df = df[df["Device ID"]!= "00000000-0000-0000-0000-000000000000"]
df = df.dropna()
print(df.head())

#subset dataframes by a/b testing segment value
segment_a_df = df[df["A/B Testing Segment"] == 'A']
segment_b_df = df[df["A/B Testing Segment"] == 'B']

#check data types
#data_types = segment_a.dtypes
#print(data_types)

print("\n")
print("Segment A Summary Stats")
print(segment_a_df.describe())
print("\n")
print("Segment B Summary Stats")
print(segment_b_df.describe())
print("\n")

#using the Mann-Whitney U test for comparing independent data samples: the nonparametric version of the Student t-test

# compare sample visits
print("For Visits")
stat, p = mannwhitneyu(segment_a_df["Visits"], segment_b_df["Visits"])
print('Statistics=%.3f, p=%.3f' % (stat, p))

# interpret
alpha = 0.05
if p > alpha:
   print('Same distribution (fail to reject H0)')
else:
   print('Different distribution (reject H0)')

print("\n")

# compare sample page views
print("For Page Views")
stat, p = mannwhitneyu(segment_a_df["Page Views"], segment_b_df["Page Views"])
print('Statistics=%.3f, p=%.3f' % (stat, p))

# interpret
alpha = 0.05
if p > alpha:
    print('Same distribution (fail to reject H0)')
else:
    print('Different distribution (reject H0)')

print("\n")

# compare sample page views
print("For Article Views")
stat, p = mannwhitneyu(segment_a_df["Article View"], segment_b_df["Article View"])
print('Statistics=%.3f, p=%.3f' % (stat, p))

# interpret
alpha = 0.05
if p > alpha:
    print('Same distribution (fail to reject H0)')
else:
    print('Different distribution (reject H0)')

#plt.hist(segment_a["Visits"]/31, bins=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
#plt.ylabel('Count')
#plt.show()

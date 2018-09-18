# purpose: check for statiscally significant differences in key KPIs (Visits, Page Views, Article Views)
# between the A and B testing segments on the iOS and Android apps

# https://machinelearningmastery.com/nonparametric-statistical-significance-tests-in-python/

# Hypothesis - Fail to reject H0: distributions are equal

# library requirements
# adobe_analytics https://github.com/SaturnFromTitan/adobe_analytics
# pandas
# datetime
# matplotlib.pyplot
# scipy.stats

# importing python libraries (already installed via UI)
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
from adobe_analytics import Client, ReportDefinition
import pandas as pd
pd.set_option("display.max_columns", None)

# setting client variable with my username and shared secret (from Adobe Analytis user management)
client = Client("awitana:Fairfax NZ", "b235d083b8484579ec71f3544d746442")

# setting suite variable with the global report suite id
suites = client.suites()
suite = suites["fairfaxnz-stuffoverall-production"]

# can be used to return a list of available metrics, dimensions and segments if the code needs to be updated
# print(suite.metrics())
# print(suite.dimensions())
# print(suite.segments())

# running report for top 400 dimensions for 2018-09-01 to 2018-09-15
# dimensions - prop45(Device ID), evar131(AB Testing Segment)
# metrics - visits, page views, event22(Article View)

report_definition = ReportDefinition(
    dimensions=[
        {"id": "prop45", "top": 400},
        {"id": "evar131", "top": 1},
    ],
    metrics=[
        "visits",
        "pageviews",
        "event22",
    ],
    date_from="2018-09-01",
    date_to="2018-09-15",
)

# saving output in a dataframe
device_df = suite.download(report_definition)

# transforming dataframe by converting strings to numeric (where applicable) and dropping na and device id = 000....
device_df = device_df.apply(pd.to_numeric, errors="ignore")
device_df = device_df[device_df["Device ID"] != "00000000-0000-0000-0000-000000000000"]
device_df = device_df.dropna()

# print dataframe head (columns are Device ID, A/B Testing Segment, Visits, Page Views, Article View)
print(device_df.head())

# subsetting device_df dataframe by A/B Testing Segment value
device_a_df = device_df[device_df["A/B Testing Segment"] == 'A']
device_b_df = device_df[device_df["A/B Testing Segment"] == 'B']

# generating summary statistics of device dataframes
print("\n")
print("All Summary Stats")
print(device_df.describe())
print("\n")
print("Segment A Summary Stats")
print(device_a_df.describe())
print("\n")
print("Segment B Summary Stats")
print(device_b_df.describe())
print("\n")

# running trended report by A/B Testing Segment for 2018-09-01 to 2018-09-15
# dimensions - prop45(Device ID), evar131(A/B Testing Segment)
# metrics - visits, page views, event22(Article View)

report_definition = ReportDefinition(
    dimensions=[
        {"id": "evar131", "top": 3},
    ],
    metrics=[
        "visits",
        "pageviews",
        "event22",
    ],
    date_from="2018-09-01",
    date_to="2018-09-15",
    granularity="day"
)

# saving output in a dataframe
trended_df = suite.download(report_definition)

# transforming dataframe by converting strings to numeric (where applicable) and dropping na and device id = 000....
trended_df = trended_df.apply(pd.to_numeric, errors='ignore')
trended_df = trended_df.dropna()

# print dataframe head (columns are Datetime, A/B Testing Segment, Visits, Page Views, Article View)
print(trended_df.head())

# subsetting device_df dataframe by A/B Testing Segment value
trended_a_df = trended_df[trended_df["A/B Testing Segment"] == 'A']
trended_b_df = trended_df[trended_df["A/B Testing Segment"] == 'B']

# generating summary statistics of device dataframes
print("\n")
print("All Summary Stats")
print(trended_df.describe())
print("\n")
print("Segment A Summary Stats")
print(trended_a_df.describe())
print("\n")
print("Segment B Summary Stats")
print(trended_b_df.describe())
print("\n")

# plot histograms for device dataframes
fig = plt.figure()
fig.add_subplot(321)
fig.subplots_adjust(hspace=.5)
fig.subplots_adjust(wspace=.25)
plt.hist(device_a_df["Visits"], color="cyan", edgecolor="black", label="Segment A", bins=45)
plt.hist(device_b_df["Visits"], color="pink", edgecolor="black", label="Segment B", bins=45)
plt.xlabel("Visits")
plt.ylabel("Device ID Count")
plt.legend(loc="upper right")

fig.add_subplot(323)
plt.hist(device_a_df["Page Views"], color="cyan", edgecolor="black", label="Segment A", bins=45)
plt.hist(device_b_df["Page Views"], color="pink", edgecolor="black", label="Segment B", bins=45)
plt.xlabel("Page Views")
plt.ylabel("Device ID Count")
plt.legend(loc="upper right")

fig.add_subplot(325)
plt.hist(device_a_df["Article View"], color="cyan", edgecolor="black", label="Segment A", bins=35)
plt.hist(device_b_df["Article View"], color="pink", edgecolor="black", label="Segment B", bins=35)
plt.xlabel("Article Views")
plt.ylabel("Device ID Count")
plt.legend(loc="upper right")

# plot trended data for trended dataframes
fig.add_subplot(322)
plt.plot([datetime.strptime(d, "%Y-%m-%d %H:%M:%S").date() for d in trended_a_df["Datetime"]], trended_a_df["Visits"], color="cyan", label="Segment A")
plt.plot([datetime.strptime(d, "%Y-%m-%d %H:%M:%S").date() for d in trended_b_df["Datetime"]], trended_b_df["Visits"], color="pink", label="Segment B")
plt.ylabel("Visits")
plt.legend(loc="upper right")
plt.xticks(rotation=45)

fig.add_subplot(324)
plt.plot([datetime.strptime(d, "%Y-%m-%d %H:%M:%S").date() for d in trended_a_df["Datetime"]], trended_a_df["Page Views"], color="cyan", label="Segment A")
plt.plot([datetime.strptime(d, "%Y-%m-%d %H:%M:%S").date() for d in trended_b_df["Datetime"]], trended_b_df["Page Views"], color="pink", label="Segment B")
plt.ylabel("Page Views")
plt.legend(loc="upper right")
plt.xticks(rotation=45)

fig.add_subplot(326)
plt.plot([datetime.strptime(d, "%Y-%m-%d %H:%M:%S").date() for d in trended_a_df["Datetime"]], trended_a_df["Article View"], color="cyan", label="Segment A")
plt.plot([datetime.strptime(d, "%Y-%m-%d %H:%M:%S").date() for d in trended_b_df["Datetime"]], trended_b_df["Article View"], color="pink", label="Segment B")
plt.ylabel("Article Views")
plt.legend(loc="upper right")
plt.xticks(rotation=45)

plt.show()

# using the Mann-Whitney U test for comparing independent data samples: the nonparametric version of the Student t-test
# comparing Visits
print("For Visits")
stat, p = mannwhitneyu(device_a_df["Visits"], device_b_df["Visits"])
print('Statistics=%.3f, p=%.3f' % (stat, p))

# interpreting p-value for Visits
alpha = 0.05
if p > alpha:
    print('Same distribution (fail to reject H0)')
else:
    print('Different distribution (reject H0)')

print("\n")

# comparing Page Views
print("For Page Views")
stat, p = mannwhitneyu(device_a_df["Page Views"], device_b_df["Page Views"])
print('Statistics=%.3f, p=%.3f' % (stat, p))

# interpreting p-value for AD Page Views
alpha = 0.05
if p > alpha:
    print('Same distribution (fail to reject H0)')
else:
    print('Different distribution (reject H0)')

print("\n")

# comparing Article Views
print("For Article Views")
stat, p = mannwhitneyu(device_a_df["Article View"], device_b_df["Article View"])
print('Statistics=%.3f, p=%.3f' % (stat, p))

# interpreting p-value for Article Views
alpha = 0.05
if p > alpha:
    print('Same distribution (fail to reject H0)')
else:
    print('Different distribution (reject H0)')
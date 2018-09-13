# adobe_analytics

Test use cases for Adobe Analytics data reporting requests utilizing the Python library adobe_analytics https://github.com/SaturnFromTitan/adobe_analytics 

Utilizes Adobe Analytics reporting API v 1.4

## File Descriptions
### a_b_app_test.py
Testing if key KPIs (visits, page views, article views, time spent etc.) have shown a change that's statistically significant using the Mann Whitney U test (t-test for non-parametric distributions)

### site_section.py
Plotting site section PVs and highlighting the days when the PVs were lower than the mean for the last 3 months (picked this random number as an example)

### top_stories.py
Table showing top performing articles (have to join the unique content ID to the most popular Content Title) for end use reporting ease

## Package Dependencies
### a_b_app_test.py
* pandas
* scipy.stats

### site_section.py
* pandas
* matplotlib.pyplots
* matplotlib.dates
* datetime

### top_stories.py
* pandas
* plotly







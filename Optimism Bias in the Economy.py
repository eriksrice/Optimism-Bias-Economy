import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime as dt

#adding quarterly consumer sentiment index database
csi_df = pd.read_csv('/Users/erikrice/Downloads/tbqics.csv')
print(csi_df.head())

#adding quarterly gdp database
gdp_df = pd.read_csv('/Users/erikrice/Downloads/cleveland_fed_yieldcurve.csv')
print(gdp_df.head())

#preparing to merge tables. comparing data types
print(csi_df.dtypes)
print(gdp_df.dtypes)

#cleaning first dateframe for merge
gdp_df['Date'] = pd.to_datetime(gdp_df['DateTime']).dt.date
print(gdp_df.dtypes)

#cleaning up the other dataframe
csi_df['QUARTER'] = csi_df['QUARTER'].astype(str)
csi_df['QUARTER'] = csi_df['QUARTER'].str.replace('Jan.-Mar.', '03')
csi_df['QUARTER'] = csi_df['QUARTER'].str.replace('Apr.-June', '06')
csi_df['QUARTER'] = csi_df['QUARTER'].str.replace('Jul.-Sep.', '09')
csi_df['QUARTER'] = csi_df['QUARTER'].str.replace('Oct.-Dec.', '12')
csi_df.rename(columns = {'QUARTER': 'Month'}, inplace=True)
csi_df.rename(columns = {'YYYY': 'Year'}, inplace=True)
csi_df['Day'] = '01'
csi_df['Date'] = pd.to_datetime(csi_df[['Year', 'Month', 'Day']]).dt.date
print(csi_df.dtypes)

#merging the tables, dropping incomplete rows
df = pd.merge(gdp_df, csi_df, how='outer', on='Date')
print(df.head())

#cleaning up final dataframe
df = df.set_index('Date')
df = df[['real_gdp', 'ICS_ALL']]
df.columns = ['Real_GDP', 'CSI']

#removing rows with null values
print(df.info())
df = df.dropna()
print(df.head())

#only a moderate correlation
print(df['Real_GDP'].corr(df['CSI']))

#dummy graph to get theme to work
fig = plt.subplots(figsize=(20, 5))
sns.lineplot(x='Date', y='Date', data=df).set(title='Consumer Sentiment Index', xlabel='Year', ylabel='CSI')
sns.set_theme(style='darkgrid')
plt.show()

#charting Consumer Sentiment Index
fig = plt.subplots(figsize=(20, 5))
sns.lineplot(x='Date', y='CSI', data=df).set(title='Consumer Sentiment Index', xlabel='Year', ylabel='CSI')
sns.set_theme(style='darkgrid')
plt.show()

#charting real GDP 
fig = plt.subplots(figsize=(20, 5))
sns.lineplot(x='Date', y='Real_GDP', data=df).set(title='Real GDP', xlabel='Year', ylabel='Real GDP')
sns.set_theme(style='darkgrid')
plt.show()

#combining data into one chart
print(df['Real_GDP'].min())
print(df['Real_GDP'].max())
scaled_GDP = (df['Real_GDP'] + 8.35) / (12.46 + 8.35)
df['scaled_GDP'] = scaled_GDP
print(df['CSI'].min())
print(df['CSI'].max())
scaled_CSI = (df['CSI'] - 54.4) / (110.1 - 54.4)
df['scaled_CSI'] = scaled_CSI
fig = plt.subplots(figsize=(20, 5))
sns.lineplot(data=df, x='Date', y='scaled_GDP', label='Real GDP')
sns.lineplot(data=df, x='Date', y='scaled_CSI', label='Consumer Sentiment Index').set(title='Consumer Sentiment Index Compared to Real GDP', ylabel='Standardized Indicator', xlabel='Year')
sns.set_theme(style='darkgrid')
plt.show()

#importing gallup dataset. past/present and present/future tables merged in excel (easier than Python in this context)
pf_df = pd.read_csv('/Users/erikrice/Downloads/Gallup Personal Finances Poll - Next Year - Sheet1 (2).csv')
print(pf_df.head())

#consolodating dates into one column
pf_df['Date'] = pd.to_datetime(pf_df[['Year', 'Month', 'Day']]).dt.date
print(pf_df)

#cleaning merged tables 
pf_df['Present_Better_Off'] = pf_df['% Better off']
pf_df['Present_Worse_Off'] = pf_df['% Worse off']
pf_df['Future_Better_Off'] = pf_df['Better Off']
pf_df['Future_Worse_Off'] = pf_df['Worse Off']
pf_df = pf_df[['Date','Present_Better_Off', 'Present_Worse_Off', 'Future_Better_Off', 'Future_Worse_Off']]
pf_df.sort_values('Date', inplace=True)
pf_df.dropna()
print(pf_df)

#further cleaning for some summary statistics
numeric_pf_df = pf_df[['Present_Better_Off', 'Present_Worse_Off', 'Future_Better_Off', 'Future_Worse_Off']]
print(numeric_pf_df.dtypes)
numeric_pf_df['Future_Better_Off'] = numeric_pf_df['Future_Better_Off'].astype(float)
numeric_pf_df['Future_Worse_Off'] = numeric_pf_df['Future_Worse_Off'].astype(float)
print(numeric_pf_df.agg(['mean', 'median', 'std']))

#visual for past/present data over the years
sns.set_palette('pastel')
fig = plt.subplots(figsize=(20, 5))
sns.lineplot(data=pf_df, x='Date', y='Present_Better_Off', label='Better Off Than a Year Ago')
sns.lineplot(data=pf_df, x='Date', y='Present_Worse_Off', label='Worse Off Than a Year Ago').set(title='Survey: Are you better off financially than you were a year ago?', xlabel='Year', ylabel='% Response')
sns.set_theme(style='darkgrid')
plt.show()

#what about people's projection of the future?
#charting personal finance data
sns.set_palette('pastel')
fig = plt.subplots(figsize=(20, 5))
sns.lineplot(data=pf_df, x='Date', y='Future_Better_Off', label='Better Off a Year From Now')
sns.lineplot(data=pf_df, x='Date', y='Future_Worse_Off', label='Worse Off a Year From Now').set(title='Survey: Will you be better off financially a year from now?', xlabel='Year', ylabel='% Response')
sns.set_theme(style='darkgrid')
plt.show()

#putting them all on one chart
sns.set_palette('pastel')
fig = plt.subplots(figsize=(20, 5))
sns.lineplot(data=pf_df, x='Date', y='Present_Better_Off', label='Better Off Than a Year Ago')
sns.lineplot(data=pf_df, x='Date', y='Present_Worse_Off', label='Worse Off Than a Year Ago')
sns.lineplot(data=pf_df, x='Date', y='Future_Better_Off', label='Better Off a Year From Now')
sns.lineplot(data=pf_df, x='Date', y='Future_Worse_Off', label='Worse Off a Year From Now').set(title='Combined Survey Responses', xlabel='Year', ylabel='% Response')
sns.set_theme(style='darkgrid')
plt.show()
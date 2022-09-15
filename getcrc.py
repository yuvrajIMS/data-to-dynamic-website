import sys
import json
import warnings
import numpy as np
import pandas as pd
import pyDataverse as pydv
from bs4 import BeautifulSoup
import pyDataverse.api as pydv_api

warnings.filterwarnings("ignore")

DATAVERSE_URL = 'https://data.goettingen-research-online.de/'
DATAVERSE_ACCESS_TOKEN = ''

api = pydv_api.NativeApi(DATAVERSE_URL, DATAVERSE_ACCESS_TOKEN)
data_api = pydv_api.DataAccessApi(DATAVERSE_URL, DATAVERSE_ACCESS_TOKEN)

resp = api.get_info_version()
print(resp.json())

# Load all datasets and datafiles from CRC1456 and INF dataverses
crc1456_dataverses = api.get_children(parent="crc1456", children_types=['datasets'])
inf_dataverses = api.get_children(parent="INF", children_types=['datasets'])

# Concatenating CRC1456 and INF Dataverses 
full_dataset = crc1456_dataverses #+ inf_dataverses

# Create a pandas dataframe from the concatenated list
df_full_dataset = pd.DataFrame(full_dataset)

# Break the dictionaries in 'children' into specific dataframes
print(df_full_dataset.keys())

df_data = []
for i, line in df_full_dataset.iterrows():
	pid = line["pid"]
	df_data.append(api.get_dataset(pid).json()["data"]["latestVersion"]["metadataBlocks"]["citation"]["fields"])

# Making Dataframe (full_df) for all available values in CRC and INF datasets
extracted_dictionary = []
for data in df_data:
	data_entry = {}
	for d in data:
		t_df = pd.DataFrame([d])
		if type(t_df["value"].values[0]) == list:
			if type(t_df["value"].values[0][0]) == dict:
				t_sub_df = pd.DataFrame(t_df["value"].values[0][0])
				titles = t_sub_df.loc["typeName"].values
				values = t_sub_df.loc["value"].values
				for title, value in zip(titles,values):
					data_entry.update({title: value})
		else:
			title = t_df["typeName"].values[0]
			value = t_df["value"].values[0]
			data_entry.update({title: value})
	extracted_dictionary.append(pd.DataFrame([data_entry]))
	
full_df = pd.concat(extracted_dictionary)

# Creating Subject List
Subject_list = []
for data in df_data:
	for d in data:
		t_df = pd.DataFrame([d])
		if t_df.typeName.values[0] == "subject":
			(*t_df["typeName"], ":", *t_df["value"], "\n")
			t = [*t_df["typeName"]]
			v = [*t_df["value"]]
			Subject_list.append(v)
			
# Creating dataframe (df) for Title, Author, Deposit_Date, PID, Subject and Description

df = pd.DataFrame({'TITLE': full_df.title,
		'AUTHOR' : full_df.authorName,
		'DATE_DEPOSITED' : full_df.dateOfDeposit,
		'SUBJECT': Subject_list,
		'PID': pid,
		'DESCRIPTION':full_df.dsDescriptionValue,
		})

# Removing [[]] from SUBJECT COLUMN
df.SUBJECT = df.SUBJECT.apply(lambda x: x[0][0])

# HTML TO PLAIN TEXT	
df['DESCRIPTION'] = df[['DESCRIPTION']].applymap(lambda text: BeautifulSoup(text, 'html.parser').get_text().replace("\n",",").replace(",,",","))

df.index = np.arange(1, len(df)+1)

# df to csv
df.to_csv('crc1.csv')
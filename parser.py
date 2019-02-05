#!/usr/bin/python3
"""
Script based off of https://www.kaggle.com/walterhan/scrape-kenpom-data/code with years changed to 2019
Original script, and my edits, are licensed under Apache 2.0 http://www.apache.org/licenses/LICENSE-2.0
https://github.com/nvitha/Kenpom-Parser
"""

import os
import re
import time
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup


# Create a method that parses a given year and spits out a raw dataframe
def import_kenpom(url):
    """
    Imports raw data from a ken pom year into a dataframe
    """
    f = requests.get(url)
    soup = BeautifulSoup(f.text, features="lxml")
    table_html = soup.find_all('table', {'id': 'ratings-table'})

    # Weird issue w/ <thead> in the html
    # Prevents us from just using pd.read_html
    # Let's find all the thead contents and just replace/remove them
    # This allows us to easily put the table row data into a dataframe using panda
    thead = table_html[0].find_all('thead')

    table = table_html[0]
    for x in thead:
        table = str(table).replace(str(x), '')

    df = pd.read_html(table)[0]
    return df


def format_df(df):
    # Column rename based off of original website
    df.columns = ['Rank', 'Team', 'Conference', 'W-L', 'AdjEM',
                  'AdjO', 'AdjO Rank', 'AdjD', 'AdjD Rank',
                  'AdjT', 'AdjT Rank', 'Luck', 'Luck Rank',
                  'SOS AdjEM', 'SOS AdjEM Rank', 'SOS OppO', 'SOS OppO Rank',
                  'SOS OppD', 'SOS OppD Rank', 'NCSOS AdjEM', 'NCSOS AdjEM Rank']

    # Split W-L column into wins and losses

    df['Wins'] = df['W-L'].apply(lambda x: int(re.sub('-.*', '', x)))  # split out wins to own column
    df['Losses'] = df['W-L'].apply(lambda x: int(re.sub('.*-', '', x)))  # split out losses to own column
    df.drop('W-L', inplace=True, axis=1)  # drop W-L column
    return df


def main():
    current_year = int(datetime.now().year)         # Figure out current season
    current_month = int(datetime.now().month)       # If it's after October, choose new year
    if current_month > 10:
        current_year += 1

    url = 'http://kenpom.com/index.php'
    df = import_kenpom(url)
    df = format_df(df)

    directory = 'out_files/'
    if not os.path.exists(directory):
        os.mkdir(directory)
    filename = directory + str(time.time()) + 'out.csv'
    df.to_csv(filename, float_format='%g', index=False)
    print(df.head(25))


if __name__ == '__main__':
    main()

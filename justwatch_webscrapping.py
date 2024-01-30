# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 11:32:19 2023

@author: entsa
"""

import os
import json
import requests
import pandas as pd

from tqdm.notebook import tqdm

streamings = dict(
    amazon='amp',
    disney='dnp',
    netflix='nfx',
    hulu='hlu'
)

url = "https://apis.justwatch.com/graphql"

headers = {
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32",
    "accept-encoding": "gzip, deflate, br"
}

with open('src/postData.json', 'r', encoding='utf-8') as file:
    post_data = json.load(file)
    
with open('src/query.graphql', 'r', encoding='utf-8') as file:
    query = file.read()   
    
post_data['query'] = query

def set_streaming(key: str):
    """ Set the streaming on query variables. """
    
    post_data['variables']['popularTitlesFilter']['packages'] = [streamings[key]]
    
clusters = [1899, 1950, 1980, 1990, 2000, 2010, 2012, 2014, 2016, 2018, 2020, 2021]

def get_titles(streaming: str, cursor: str = None, titles: list = None, start: bool = True, page_size: int = 100):
    """ Get all titles available of a streaming, with pagination. """
    
    if titles is None:
        titles = []
    
    if cursor and not start:
        post_data['variables']['popularAfterCursor'] = cursor
    else:
        post_data['variables']['popularAfterCursor'] = ""
    
    post_data['variables']['pageSize'] = page_size

    set_streaming(streaming)
    try:
        req = requests.post(url, data=json.dumps(post_data), headers=headers)

        if req.status_code != 200 or 'application/json' not in req.headers.get('Content-Type', ''):
            print(f"Invalid response. Status Code: {req.status_code}, Content-Type: {req.headers.get('Content-Type')}")
            return titles

        response_json = req.json()

        if 'data' in response_json and 'popularTitles' in response_json['data']:
            results = response_json['data']['popularTitles']
        else:
            print("Error: 'data' or 'popularTitles' not found in response")
            return titles

        # Check if 'edges' is not None before extending titles
        if results.get('edges'):
            titles.extend(results['edges'])   
       
        # Check if 'pageInfo' is not None before accessing 'hasNextPage'
        if results.get('pageInfo') and results['pageInfo'].get('hasNextPage'):
            cursor = results['pageInfo']['endCursor']
            get_titles(streaming=streaming, cursor=cursor, titles=titles, start=False, page_size=page_size)

    except Exception as e:
        print(f"An error occurred: {e}")
        return titles
    
    return titles

def parse_title_content(title: dict):
    """ Parse the title content to a dictionary. """
    
    content = {}
    
    title = title['node']
    content['id'] = title['id']
    content['title'] = title['content']['title']
    content['type'] = title['objectType']
    content['description'] = title['content']['shortDescription']
    content['release_year'] = title['content']['originalReleaseYear']
    content['age_certification'] = title['content']['ageCertification']
    content['runtime'] = title['content']['runtime']
    content['genres'] = [i['technicalName'] for i in title['content']['genres']]
    content['production_countries'] = title['content']['productionCountries']
    content['seasons'] = title.get('totalSeasonCount', None)
    content['imdb_id'] = title['content']['externalIds']['imdbId']
    content['imdb_score'] = title['content']['scoring']['imdbScore']
    content['imdb_votes'] = title['content']['scoring']['imdbVotes']
    content['tmdb_popularity'] = title['content']['scoring']['tmdbPopularity']
    content['tmdb_score'] = title['content']['scoring']['tmdbScore']
    
    credits = [
        {
            'person_id': i['personId'],
            'id': content['id'],
            'name': i['name'],
            'character': i['characterName'],
            'role': i['role']
        } for i in title['content']['credits']
    ]
    
    return content, credits

def parse_and_save_data(data: list, save: bool = True, path: str = ''):
    """ Parse a list of titles and save it to a file. """
    
    titles, credits = [], []
    for d in data:
        t, c = parse_title_content(d)
        titles.append(t)
        credits.extend(c)
    
    if save:
        titles_df = pd.DataFrame(titles)
        titles_df.to_csv(path+'titles.csv', index=False)

        credits_df = pd.DataFrame(credits)
        credits_df.to_csv(path+'credits.csv', index=False)

    return titles, credits

def get_all_titles_by_streaming(streaming: str, save: bool = True, path: str = ''):
    """ Get all titles available on a given streaming. """
    raw = []
    for i in range(len(clusters) - 1):
        filter_range = {'min': clusters[i]+1, 'max': clusters[i+1]}
        
        post_data['variables']['popularTitlesFilter']['releaseYear'] = filter_range  # Set the filter
        
        cluster_titles = get_titles(streaming=streaming)
        raw.extend(cluster_titles)
    
    if save:
        file_path = f'{path}/{streaming}/'
        if not os.path.exists(file_path):
            os.mkdir(file_path)
            
    titles, credits = parse_and_save_data(data=raw, save=save, path=file_path)
    
    return titles, credits

def get_all_titles(save: bool = True, path:str = ''):
    """ Get all titles available on the available streamings. """
    
    all_titles = {}
    for key in tqdm(streamings.keys()):
        titles, credits = get_all_titles_by_streaming(streaming=key, save=save, path=path)
        all_titles[key] = {'titles': titles, 'credits': credits}
    
    return all_titles

data = get_all_titles(save=True, path='data')
len(data['netflix']['titles'])
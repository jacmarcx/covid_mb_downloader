import os
import datetime
from github import Github
import time
import requests
import tempfile

from datetime import datetime, timedelta
import json
import pytz # better time zones


# access Github repo
token = os.environ['GH_TOKEN']
g = Github(token)
repo = g.get_repo('jacmarcx/covid_mb_downloader')

# commit string
t = datetime.now(pytz.timezone('America/Winnipeg'))
commit = 'Nightly update: ' + str(t.date())



def dl_file(url, path, file, ext='.json'):
    """save JSONs to Github daily"""
    req = requests.get(url)   
    stamp = (str(datetime.now(pytz.timezone('America/Winnipeg')).date()) + '-') # get file timestamp
    ## save to json
    tmpdir = tempfile.TemporaryDirectory()
    fpath = os.path.join(tmpdir.name, file+ext)
    with open(fpath, 'wb') as writer:
        writer.write(req.content)
        
        with open(fpath, 'r') as reader:
            data = reader.read()
        
            ## commit and push to repo
            repo.create_file(path+stamp+file+ext, commit, data)


while True:

    # MB - Cases by demographics and RHA
    dl_file('https://services.arcgis.com/mMUesHYPkXjaFGfS/arcgis/rest/services/mb_covid_cases_by_demographics_rha_all/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&groupByFieldsForStatistics=Age_Group%2CGender&orderByFields=Age_Group%20desc',
            'json/demographics-rha/',
            'demographics-rha')

    # MB - Cases by status and RHA
    dl_file('https://services.arcgis.com/mMUesHYPkXjaFGfS/arcgis/rest/services/mb_covid_cases_by_status_daily_rha/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&groupByFieldsForStatistics=Date%2CRHA',
            'json/case-summary-rha/',
            'case-summary-rha')

    # MB - Manitoba five-day test positivity rate
    dl_file('https://services.arcgis.com/mMUesHYPkXjaFGfS/arcgis/rest/services/mb_covid_5_day_positivity_rate/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Date%20asc',
            'json/test-positivity-rate/',
            'test-positivity-rate')
            
    # MB - Manitoba district level data
    dl_file('https://services.arcgis.com/mMUesHYPkXjaFGfS/ArcGIS/rest/services/mb_covid_cases_summary_stats_geography/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=OBJECTID%20ASC&outSR=102100&resultOffset=0&resultRecordCount=1000&cacheHint=true',
            'json/details-district/',
            'details-district')
            
    time.sleep(10000)

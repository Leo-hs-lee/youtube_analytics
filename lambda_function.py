#For AWS Lambda
import json
from googleapiclient.discovery import build
import pandas as pd 
import pymysql 
import sqlalchemy 
from sqlalchemy import create_engine, inspect 
import boto3 
import io
from io import BytesIO
import os
import datetime
from datetime import date



def lambda_handler(event, context):
    


    #s3 connection & Read CSV file content from S3 bucket https://www.youtube.com/watch?v=6LvtSmJhVRE

    accessKey = 'Yout AWS Access Key'
    secretKey = 'Your AWS Secret Key'
    region = 'Your AWS Region: (ex) ap-northeast-2'

    s3 = boto3.client('s3',
                    aws_access_key_id=accessKey,
                    aws_secret_access_key=secretKey,
                    region_name=region)

    bucket_name = 'ytchannels'
    csv_name = 'youtube_channels.csv'

    yt_data = s3.get_object(Bucket=bucket_name, Key=csv_name)

    channel_df = pd.read_csv(io.BytesIO(yt_data['Body'].read()))

    
    #Youtube API
    api_key = 'Youtube API Key'
    channel_ids= channel_df['ID'].to_list()

    youtube = build('youtube', 'v3', developerKey=api_key)

    def get_channel_stats(youtube, channel_ids):
        all_data = []
        for i in range(0, len(channel_ids), 50):
            request = youtube.channels().list(
                        part='snippet,contentDetails,statistics',
                        id = ','.join(channel_ids[i:i+50]))
            response = request.execute()
        
            for i in range(len(response['items'])):
                data = dict(channel_name = response['items'][i]['snippet']['title'],
                            published_date = response['items'][i]['snippet']['publishedAt'],
                            subscribers = response['items'][i]['statistics']['subscriberCount'],
                            views = response['items'][i]['statistics']['viewCount'],
                            total_videos = response['items'][i]['statistics']['videoCount'],
                            playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                            retrieved_date = date.today().strftime('%Y/%m/%d')              
                            )
                all_data.append(data)
        return all_data


    channel_statistics = get_channel_stats(youtube, channel_ids)
    channel_data = pd.DataFrame(channel_statistics)

    channel_data['published_date'] = pd.to_datetime(channel_data['published_date']).dt.date
    channel_data['subscribers'] = pd.to_numeric(channel_data['subscribers'])
    channel_data['views'] = pd.to_numeric(channel_data['views'])
    channel_data['total_videos'] = pd.to_numeric(channel_data['total_videos'])
    channel_data['retrieved_date'] = pd.to_datetime(channel_data['retrieved_date']).dt.date

    # Credentials to RDS-mysql connection 
    hostname="MySQL Hostname"
    dbname="MySQL DB Name"
    uname="Username"
    pwd="PW for DB"

    # Create SQLAlchemy engine to connect to MySQL Database
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                    .format(host=hostname, db=dbname, user=uname, pw=pwd))
    
    # Convert dataframe to sql table                               
    result = channel_data.to_sql('Your_DB_Name', engine, if_exists='append', index = False)

    return  {
        'statusCode': 200,
        'body' : json.dumps(result)
    }

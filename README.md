# Youtube Channel Monitoring System

## 🎞️ About the Project
This Youtube channel monitoring system runs on the [AWS Lambda](https://aws.amazon.com/lambda/) serverless framework.\
Once a day, the monitor logs youtube channel statistics such as subscriber count, video count, view count, etc. 

### Built with
* [Python 3.8](https://www.python.org/downloads/release/python-3814/)
* [Youtube API V3](https://developers.google.com/youtube/v3)
* [AWS Lambda](https://aws.amazon.com/lambda/)
* [AWS RDS](https://aws.amazon.com/RDS/)
* [MySQL](https://www.mysql.com/)

## 📈 Result

> We are able to identify high-performing channels among listed channels.  
<img src="https://user-images.githubusercontent.com/113565868/190591500-83b57aca-71f2-40c4-b94b-58e5b8d510e2.PNG" width="800" height="500" />
<img src="https://user-images.githubusercontent.com/113565868/190595693-6748471e-9d9e-4840-9f5e-f8ab056f0f4f.PNG" width="800" height="500" />



> Also, we can depict the viewership trend of high-performing channels.
<img src="https://user-images.githubusercontent.com/113565868/190593869-4e669cfa-c239-4f51-b319-ae61ef142e9a.PNG" width="800" height="300" />



## 🛠 System Structure
![youtube_analysis4](https://user-images.githubusercontent.com/113565868/190601715-39a190fb-5c40-4f52-b2f5-faa5a9d72a89.PNG)
1. Input the list of *Youtube channel names* and *channel IDs* in the database(AWS RDS-MySQL)
2. Request corresponding youtube channel statistics from Youtube Data API v3
3. Store the Youtube channel information in the database automatically, once a day, using AWS Lambda serverless framework
4. data manipulation and visualization(Jupiter Notebook)


### Prerequisites
```
pip install google-api-python-client
pip install pandas
pip install pymysql
pip install sqlalchemy
```
MUST INPUT YOUR OWN Youtube API key & Database credentials
```
api_key = 'Your API Key'
hostname="Host Address"
dbname="Database"
uname="User Name"
pwd="Your Password"
```


## 📊 Data 
### Input data 
| Channel Name    | Channel ID               |
|-----------------|--------------------------|
| Example Channel | UCK9M3uZMNjbqCI3O80-eF1k |
| ...             | ...                      |

**Channel Name**: Name of the Youtube channel\
**Channel ID**: ID of the Youtube channel can be found ['here'](https://support.google.com/youtube/answer/3250431?hl=en)

### Output data
| channel_name    | published_date       | subscribers | views     | total_videos | playlist_id              | retrieved_date |
|-----------------|----------------------|-------------|-----------|--------------|--------------------------|----------------|
| Example Channel | 2015-12-27T21:31:03Z | 1690000     | 680087428 | 185          | UUJCx8aQrdx_ueXPmxTD2odQ | 2022/09/15     |
| ...             | ...                  | ...         | ...       | ...          | ...                      | ...            |

**published_date**: The date channel was published\
**subscribers**: Total subscriber count of the channel (Count in 1000)\
**views**: Total view count of public viddeos in the channel (Decreases if video is unlisted)\
**total_video**: Total number of public videos in the channel\
**playlist_id**: Channel's playlist ID for further analysis\
**retrieved_date**: The the data was retrieved

### Data Manipulation
| channel_name    | sub_diff | view_diff | upload_diff | viewperupload | sub_gain| veiw_gain | videoloads |
|-----------------|----------|-----------|-------------|---------------|---------|-----------|------------|
| Example Channel | 2000     | 310902    | 4           | 777025.5      | 1000    | 42407     | 1          |
| ...             | ...      | ...       | ...         | ...           | ...     | ...       | ...        |

**sub_diff**: How much subscriber has increased overtime (Count in 1000)\
**view_diff**: How much view has increased overtime \
**upload_diff**: How many video was uploaded (or unlisted) overtime\
**viewperupload**: Mean of view count affected per uploads, overtime: (*view_diff/upload_diff*)\
**sub_gain**: Subscriber gain to the day before\
**view_gain**: View gain to the day before


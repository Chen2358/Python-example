import os
import you_get
import pymongo
import urllib.parse
import time
import datetime

html_folder = '/home/cwyalpha/html/acfun/'
acfun_site = 'http://www.acfun.tv/'
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "youku"
MONGODB_VIDEO_COLLECTION = "youku_video_page"
thres = 30
days = 7
del_days = 14
connection = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
db.authenticate('youku', '318yazhang')

video_collection = db[MONGODB_VIDEO_COLLECTION]
video_collection.ensure_index([('dyn.views', pymongo.DESCENDING)])
video_collection.ensure_index([('dyn.favors', pymongo.DESCENDING)])
video_collection.ensure_index([('dyn.comments', pymongo.DESCENDING)])
video_collection.ensure_index([('time', pymongo.DESCENDING)])

def id2folder(_id):
    s = str(_id)
    if len(s) > 3:
        return os.path.join(s[:-3], s[-3:])
    else:
        return s

def del_video():
    start_time = datetime.datetime.now() - datetime.timedelta(days=abs(int(del_days)))
    for video in video_collection.find({'$and':[{'html.timestamp':{'$lt':start_time}}, {'video_download_status':2}]}):
        try:
            print('del ', video['video_filename'])
            os.remove(video['video_filename'])
            
            video_collection.update({"_id" : video['_id']}, \
                                    {'$set':{'video_download_status':3}})
        except:
            print(video['_id'], 'not deleted')

def findAndDownload():
    retries = 0
    video = None
    while 1:
        try:
            del_video()
            start_time = datetime.datetime.now() - datetime.timedelta(days=abs(int(days)))
            cursor = video_collection.find({'$and':[{'$or':[{'video_failed':{'$exists':False}},\
                                                            {'video_failed':0}]}, \
                                                    {'$or':[{'video_download_status':{'$exists':False}}, \
                                                            {'video_download_status':0}, \
                                                            {'video_download_status':1}]}, \
                                                    {'time':{'$gte':start_time}}]})\
                                     .sort([('dyn.favors', pymongo.DESCENDING)])
                
            video = None
            video = cursor.__next__()
            print(video['dyn'][-1]['favors'])
            if int(video['dyn'][-1]['favors']) < thres:
                #pass
                continue
            href = video['href']
            url = urllib.parse.urljoin(acfun_site, href)
            print(url)
            if retries > 5:
                video_collection.update({"_id" : video['_id']}, \
                                            {'$set':{'video_failed':1}})
                retries = 0
                continue
            folder = os.path.join(html_folder, id2folder(video['_id']))
            folderInMongo = id2folder(video['_id'])
            if not os.path.exists(folder):
                os.makedirs(folder)
            video_collection.update({"_id" : video['_id']}, \
                                    {'$set':{'video_download_status':1}})
            you_get.acfun_download(url = url, output_dir = folder)
            video_filename = None
            for filename in os.listdir(str(folder)):
                if filename.split('.')[-1] in set(['hd2', 'mp4', 'flv', '3gp', \
                                                   'f4v', 'asf', 'wmv', 'mp3', 'mp3']):
                    video_filename = os.path.join(folderInMongo, filename)
                    break
            print(video_filename)
            if video_filename != None:
                video_collection.find_and_modify({"_id" : video['_id']}, \
                                                 update={'$set':{'video_download_status':2, \
                                                                 'video_filename':video_filename}}, \
                                                 upsert=True, new=True)
            json_filename = None
            for filename in os.listdir(str(folder)):
                if filename.split('.')[-1] in set(['json']):
                    json_filename = os.path.join(folderInMongo, filename)
                    break
            print(json_filename)
            if json_filename != None:
                video_collection.find_and_modify({"_id" : video['_id']}, \
                                                 update={'$set':{'json_filename':video_filename}}, \
                                                 upsert=True, new=True)
        except (KeyboardInterrupt, SystemExit):
            if video:
                video_collection.update({"_id" : video['_id']}, \
                                        {'$set':{'video_download_status':0}})
            break
        except:
            if video:
                retries += 1
                video_collection.update({"_id" : video['_id']}, \
                                        {'$set':{'video_download_status':0}})

#findAndDownload()
del_video()


import pymongo
import datetime

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "acfun"
MONGODB_VIDEO_COLLECTION = "video"
connection = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
collection = db[MONGODB_VIDEO_COLLECTION]

collection.ensure_index([('count.views', pymongo.DESCENDING)])
collection.ensure_index([('count.favors', pymongo.DESCENDING)])
collection.ensure_index([('count.comments', pymongo.DESCENDING)])
collection.ensure_index([('time', pymongo.DESCENDING)])

def rank():
    start = datetime.datetime.now() - datetime.timedelta(days=7)
    with open('/home/cwyalpha/AB/rank.txt', 'w') as output:
        output.write('views\tfavors\tcomments\turl\tlist_name\ttitle\tdesc\timg\tuploader\tuploader_id\n')
        cursor = collection.find({'time':{'$gte':start}})\
                           .sort([('count.favors', pymongo.DESCENDING)])
        for i in xrange(1000):
            video = cursor.next()
            count = video['count']
            favors = max([i['favors'] for i in count])
            comments = max([i['comments'] for i in count])
            views = max([i['views'] for i in count])
            output.write(str(views)+'\t'+
                         str(favors)+'\t'+
                         str(comments)+'\t'+
                         'www.acfun.tv'+video['href'].encode('utf8')+'\t'+
                         video['list_name'].encode('utf8')+'\t'+
                         video['title'].encode('utf8')+'\t'+
                         video['desc'].encode('utf8')+'\t'+
                         video['img'].encode('utf8')+'\t'+
                         video['uploader'].encode('utf8')+'\t'+
                         'http://www.acfun.tv'+video['uploader_id'].encode('utf8')+'\n')
        
if __name__ == "__main__":             
    rank()

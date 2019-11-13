# -*- coding: gbk -*-
import urllib2
import logging
import datetime
from BeautifulSoup import BeautifulSoup
import pymongo
import re
import time

wait_a_moment = 1

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "acfun"
MONGODB_VIDEO_COLLECTION = "video"

connection = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
db.authenticate('acfun', '318yazhang')
collection = db[MONGODB_VIDEO_COLLECTION]

def get_url(url):
    global wait_a_moment
    content = None
    retry = 0
    wait = wait_a_moment
    while retry < 5:
        try:
            content = urllib2.urlopen(url, timeout = 20).read()
            return content.decode('utf8', 'ignore')
        except:
            logging.info('ERROR\t'+url)
            retry += 1
            time.sleep(wait)
            wait *= 2
    return content

def save_to_db(**kwargs):
    global collection
    p = re.match('.*ac(\d*)', kwargs['href'])
    _id = p.group(1)
    item_static = {'href':kwargs['href'], \
                   'uploader':kwargs['uploader'], \
                   'uploader_id':kwargs['uploader_id'], \
                   'desc':kwargs['desc'], \
                   'title':kwargs['title'], \
                   'list_name':kwargs['list_name'], \
                   'time':kwargs['time'], \
                   'img':kwargs['img']}
    item_dyn = {'views':kwargs['views'], \
                'comments':kwargs['comments'], \
                'favors':kwargs['favors'], \
                'timestamp':kwargs['timestamp']}
    collection.find_and_modify(query = {'_id':_id}, \
                               update = {'$set':item_static, \
                                         '$push':{'dyn':item_dyn}}, \
                               upsert = True, new = True)
    #item_static = {'href':kwargs['href'], \
    #               'uploader':kwargs['uploader'], \
    #               'uploader_id':kwargs['uploader_id'], \
    #               'desc':kwargs['desc'], \
    #               'title':kwargs['title'], \
    #               'list_name':kwargs['list_name'], \
    #               'time':kwargs['time'], \
    #               'img':kwargs['img']}
    #item_dyn = {'views':kwargs['views'], \
    #            'comments':kwargs['comments'], \
    #            'favors':kwargs['favors'], \
    #            'timestamp':kwargs['timestamp']}
    #collection.find_and_modify(query = {'_id':_id}, \
    #                           update = {'$push':{'count':item_dyn}, \
    #                                     '$set':item_static}, \
    #                           upsert = True, new = True)

def parse_soup(soup):
    #items = soup.find('div', {'class':'mainer th-large'})
    #if not items:
    #    return None
    items = soup
    list_name = soup.title.string.split('-')[0].strip().encode('utf8')
    for item in items.findAll('div', {'class':'item unit'}):
        info = item.find('div', {'class':'r'})
        if not info:
            continue
        info_1 = info.find('a', {'class':'title'})
        if not info_1:
            continue
        info_2 = info.find('div', {'class':'info-extra'})
        if not info_2:
            continue
        info_3 = info_2.find('a', {'class':'name'})
        if not info_3:
            continue
        img = item.find('img', {'class':'preview'})['src']
        time = info.find('span', {'class':'time'})['title']
        p = re.search('(\d{4})年(\d{1,2})月(\d{1,2})日\(.*\)(\d{1,2})时(\d{1,2})分'.decode('gbk'),
                      time.replace(' ',''))
        time = datetime.datetime(year = int(p.group(1)),
                                 month = int(p.group(2)),
                                 day = int(p.group(3)),
                                 hour = int(p.group(4)),
                                 minute = int(p.group(5)))
        views = int(info.find('span', {'class':'views'}).contents[1])
        comments = int(info.find('span', {'class':'comments'}).contents[1])
        favors = int(info.find('span', {'class':'favors'}).contents[1])
        desc = info.find('p', {'class':'desc'}).string
        href = info_1['href']
        title = info_1.string
        uploader = info_3.contents[1]
        uploader_id = info_3['href']
        timestamp = datetime.datetime.now()
        
        if not title or not uploader:
            continue
        if not desc:
            desc = ''
        save_to_db(href = href, title = title.encode('utf8'), \
                   uploader = uploader.encode('utf8'), \
                   uploader_id = uploader_id, list_name = list_name, \
                   views = views, comments = comments, favors = favors, \
                   desc = desc.encode('utf8'), timestamp = timestamp, \
                   time = time, img = img)
def task():
    page = 'http://www.acfun.tv/v/list{listid}/index_{pagenum}.htm'
    for listid in ['102', '101', '105', '104', '69', '68', '60', '70', '87', '106','107']:
#    for listid in ['60',]:
        for pagenum in xrange(1,31):
            url = page.format(listid=listid, pagenum=pagenum)
            content = get_url(url)
            if content:
                soup = BeautifulSoup(content)
                parse_soup(soup)
                time.sleep(wait_a_moment)
                logging.info('SUCCED\t'+url)
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename="/home/cwyalpha/AB/logfile", 
                        filemode="a+",
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    task()
    collection.ensure_index([('views', pymongo.DESCENDING)])
    collection.ensure_index([('favors', pymongo.DESCENDING)])
    collection.ensure_index([('comments', pymongo.DESCENDING)])
    collection.ensure_index([('time', pymongo.DESCENDING)])

    
    

# -*- coding: utf8 -*-
import web
from web import form
import urllib2
import os
import pymongo
import datetime

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "acfun"
MONGODB_VIDEO_COLLECTION = "video"
connection = pymongo.MongoClient(MONGODB_SERVER, MONGODB_PORT)
db = connection[MONGODB_DB]
db.authenticate('acfun', '318yazhang')
collection = db[MONGODB_VIDEO_COLLECTION]

collection.ensure_index([('dyn.views', pymongo.DESCENDING)])
collection.ensure_index([('dyn.favors', pymongo.DESCENDING)])
collection.ensure_index([('dyn.comments', pymongo.DESCENDING)])
collection.ensure_index([('time', pymongo.DESCENDING)])

method = ['views', 'favors', 'comments']
urls = (
    '/', 'index', 
    '/(\d*)days_(views|favors|comments)_index_(\d*).htm', 'randompage'
)


render = web.template.render('templates') # your templates
page = item = pagenum = ''
with open('templates/index.html', 'r') as f:
    page = f.read()
with open('templates/item.html', 'r') as f:
    item = f.read()
with open('templates/page.html', 'r') as f:
    pagenum = f.read()

def get_page_index(page_index, t, days):
    info_1 = '<a href="/%(d)sdays_%(t)s_index_%(p)s.htm" class="pager">%(p)s</a>'
    info_2 = '<a class="pager active">%(p)s</a>'
    info_3 = '<a href="/%(d)sdays_%(t)s_index_%(p)s.htm" class="pager next"><i title="下一页" class="icon white icon-chevron-right">下一页</i></a>'
    info_t = '<a href="/%(d)sdays_%(t)s_index_%(p)s.htm" class="pager">%(t1)s</a>'
    result = ''
    t = str(t)
    for i in method:
        if i != t:
            result += info_t % {'p':'1', 'd':str(days), 't':i, 't1':i[0]}
    N = 11
    
    if page_index == 1:
        result += info_3 % {'p':'2', 'd':str(days), 't':t}
        result += info_2 % {'p':'1', 'd':str(days), 't':t}
        for i in xrange(2, N):
            result += '\n' + info_1 % {'p':str(i), 'd':str(days), 't':t}
       
    else:
        result += info_3 % {'p':str(page_index+1), 'd':str(days), 't':t}
        for i in xrange(max(1, page_index-N/2), page_index):
            result += '\n' + info_1 % {'p':str(i), 'd':str(days), 't':t}
        result += info_2 % {'p':str(page_index), 'd':str(days), 't':t}
        for i in xrange(page_index+1, page_index+N/2+1):
            result += '\n' + info_1 % {'p':str(i), 'd':str(days), 't':t}
    return result

def sort_method(days, t, start):
    start_time = datetime.datetime.now() - datetime.timedelta(days=abs(int(days)))
    if t == 'views':
        return collection.find({'time':{'$gte':start_time}})\
                         .sort([('dyn.views', pymongo.DESCENDING)])[start:start+20]
    if t == 'comments':
        return collection.find({'time':{'$gte':start_time}})\
                         .sort([('dyn.comments', pymongo.DESCENDING)])[start:start+20]
    if t == 'favors':
        return collection.find({'time':{'$gte':start_time}})\
                         .sort([('dyn.favors', pymongo.DESCENDING)])[start:start+20]

def get_page(days, t, start, page_index):
    l = []
    items = ''
    videos = sort_method(days, t, start)
    for video in videos:
        dyn = video['dyn'][-1]
        favors = dyn['favors']
        comments = dyn['comments']
        views = dyn['views']
        vds = ''
        if 'video_download_status' not in video:
            vds = '[Not Download]'
        elif video['video_download_status'] == 0:
            vds = '[Not Download]'
        elif video['video_download_status'] == 1:
            vds = '[Downloading]'
        elif video['video_download_status'] == 2:
            vds = '[Downloaded]'
        elif video['video_download_status'] == 3:
            vds = '[Deleted]'
        
        d = {'views':str(views), 'favors':str(favors), 'comments':str(comments), \
             'url':'http://www.acfun.tv'+video['href'].encode('utf8'), \
             'title':'['+video['list_name'].encode('utf8')+']'+video['title'].encode('utf8'), \
             'desc':video['desc'].encode('utf8'), 'img':video['img'].encode('utf8'), \
             'id':(video['href'].encode('utf8')).split('ac')[-1], \
             'uploader':video['uploader'].encode('utf8'), \
             'uploader_id':'http://www.acfun.tv'+video['uploader_id'].encode('utf8'), \
             'time':video['time'].strftime('%Y年 %m月%d日')+vds}
        items += item % d
    #with open('/home/cwyalpha/AB/rank.txt', 'r') as f:
    #    f.readline()
    #    for line in f.xreadlines():
    #        tokens = line.rstrip('\n').split('\t')
    #        l.append(tokens)
    #for i in xrange(start, start + 20):
    #    tokens = l[i%len(l)]
    #    d = {'views':tokens[0], 'favors':tokens[1], 'comments':tokens[2], \
    #         'url':'http://'+tokens[3], 'title':'【'+tokens[4]+'】'+tokens[5], \
    #         'desc':tokens[6], 'img':tokens[7], 'id':tokens[3].split('ac')[-1], \
    #         'uploader':tokens[8], 'uploader_id':tokens[9]}
    #    items += item % d
    pagenum = get_page_index(page_index, t, days)
    result = page.replace('$$$$$List$$$$$', items, 1).replace('$$$$$Page$$$$$', pagenum, 1)
    return result

class randompage:
    def GET(self, days, t, page_number):
        return get_page(days, t, (int(page_number)-1)*20, int(page_number))

class index:
    def GET(self):
        return get_page(7, 'favors', 0, 1)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

#-*- coding: utf-8 -*-
#!/usr/bin/env python3


from random import choice
import MySQLdb

def recommend(user):
	#
	DB = MySQLdb.connect("localhost", "root", "", "recommend")
	#
	c = DB.cursor()

	love = []
	sql = "select anime_id from user_anime where user_id=%s"% user
	c.execute(sql)

	#
	results = c.fetchall()
	for line in results:
		love.append(line[0])

	#
	sql = '''
	select style_id from
		(select user_id, style_id from
		(select user_id, anime_id as id from user_anime where user_id=%s) as s
		natural join anime natural join
		(select anime_id as id, style_id from anime_style) as n
		) as temp group by style_id order by count(user_id) desc limit 3;''' % user
	c.execute(sql)
	results = c.fetchall()
	lis = []
	anime = {}
	for (line,) in results:
		lis.append(line)
	for i in lis:
		#
		sql = "select anime_id from anime_style where style_id="+str(i)+";"
		c.execute(sql)
		results = c.fetchall()
		anime_lis = []
		for result in results:
			anime_lis.append(result[0])
		#
		anime[str(i)] = anime_lis
	#
	s = set(anime[str(lis[0])]) & set(anime[str(lis[1])]) & set(anime[str(lis[2])])

	#
	loveSet = set(love)

	#
	if loveSet > s:
		s = set(anime[str(lis[0])])

	#
	set_lis = []
	for i in s:
		set_lis.append(i)
	#
	recommend = choice(set_lis)

	#
	while recommend in love:
		recommend = choice(set_lis)
	dic = {}
	#
	sql = "select name, brief from anime where id="+str(recommend)+";"
	c.execute(sql)
	results = c.fetchall()
	dic['name'] = results[0][0]
	dic['brief'] = results[0][1]

	DB.close()
	return dic

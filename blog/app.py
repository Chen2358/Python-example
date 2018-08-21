# coding: utf-8

#!/usr/bin/env python3

import datetime
import functools
import os
import re
import urllib

from flask import (Flask, abort, flash, Markup, redirect, render_template,
					request, Response, session, url_for)
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from micawber import bootstrap_basic, parse_html
from micawber.cache import Cache as  OEmbedCache
from peewee import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
from playhouse.sqlite_ext import *

ADMIN_PASSWORD = 'admin'
APP_DIR = os.path.dirname(os.path.realpath(__file__))
#数据库地址
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'blog.db')
DEBUG = False
#Flask app中加密会话 cookie 的密钥
SECRET_KEY = 'hahahh, secret!'    
SITE_WIDTH = 800

app = Flask(__name__)
app.config.from_object(__name__)

#FlaskDB是一个用于创建请求前/请求后的peewee数据库的包装器
#用于管理数据库连接的钩子
flask_db = FlaskDB(app)
database = flask_db.database

#micawber提供的嵌入内容服务组件
oembed_providers = bootstrap_basic(OEmbedCache())



class Entry(flask_db.Model):
	title = CharField()	
	#基于标题生成的链接地址
	slug = CharField(unique=True)	
	content = TextField()
	published = BooleanField(index=True)
	timestamp = DateTimeField(default=datetime.datetime.now, index=True)

	#Markdown转化为html
	@property
	def html_content(self):
		hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
		extras = ExtraExtension()
		markdown_content = markdown(self.content, extensions=[hilite, extras])
		oembed_content = parse_html(
			markdown_content,
			oembed_providers,
			urlize_all=True,
			maxwidth=app.config['SITE_WIDTH'])
		return Markup(oembed_content)
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = re.sub('[^\w]+', '-', self.title.lower()).strip('-')
		ret = super(Entry, self).save(*args, **kwargs)

		self.update_search_index()
		return ret
	
	#更新索引
	def update_search_index(self):
		try:
			fts_entry = FTSEntry.get(FTSEntry.entry_id == self.id)
		except FTSEntry.DoesNotExist:
			fts_entry = FTSEntry(entry_id=self.id)
			force_insert = True
		else:
			force_insert = False
		fts_entry.content = '\n'.join((self.title, self.content))
		fts_entry.save(force_insert=force_insert)

	@classmethod
	def public(cls):
		return Entry.select().where(Entry.published == True)
	
	#未公开的博文
	@classmethod
	def drafts(cls):
		return Entry.select().where(Entry.published == False)

	@classmethod
	def search(cls, query):
		words = [word.strip() for word in query.split() if word.strip()]
		if not words:
			return Entry.select().where(Entry.id == 0)
		else:
			search = ' '.join(words)
		return (FTSEntry
				.select(
					FTSEntry,
					Entry,
					FTSEntry.rank().alias('score'))
				.join(Entry, on=(FTSEntry.entry_id == Entry.id).alias('entry'))
				.where(
					(Entry.published == True) &
					(FTSEntry.match(search)))
				.order_by(SQL('score').desc()))

#创建或更新搜索索引
class FTSEntry(FTSModel):
	entry_id = IntegerField(Entry)
	content = TextField()

	class Meta:
		database = database

#定义装饰器，使用session中的logged_in 判断是否已经登录
def login_required(fn):
	@functools.wraps(fn)
	def inner(*args, **kwargs):
		if session.get('logged_in'):
			return fn(*args, **kwargs)
		return redirect(url_for('login', next=request.path))
	return inner

@app.route('/login/', methods=['GET', 'POST'])
def login():
	next_url = request.args.get('next') or request.form.get('next')
	if request.method == 'POST' and request.form.get('password'):
		password = request.form.get('password')
		if password == app.config['ADMIN_PASSWORD']:
			session['logged_in'] = True
			session.permanent = True
			flash('You are now logged in.', 'success')
			return redirect(next_url or url_for('index'))
		else:
			flash('Incorrect password.', 'failture')
	return render_template('login.html', next_url=next_url)

#登出，清空session返回登录
@app.route('/logout/',methods=['GET', 'POST'])
def logout():
	if request.method == 'POST':
		session.clear()
		return redirect(url_for('login'))
	return render_template('logout.html')

@app.route('/')
def index():
	search_query = request.args.get('q')
	if search_query:
		query = Entry.search(search_query)
	else:
		query = Entry.public().order_by(Entry.timestamp.desc())
	return object_list('index.html', query, search=search_query, check_bounds=False)

@app.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
	if request.method == 'POST':
		if request.form.get('title') and request.form.get('content'):
			entry = Entry.create(
				title=request.form['title'],
				content=request.form['content'],
				published=request.form.get('published') or False)
			flash('Entry created successfully.', 'success')
			if entry.published:
				return redirect(url_for('detail', slug=entry.slug))
			else:
				return redirect(url_for('edit', slug=entry.slug))
		else:
			flash('Title and content are required.', 'danger')
	return render_template('create.html')

#草稿，未公开的
@app.route('/drafts/')
@login_required
def drafts():
	query = Entry.drafts().order_by(Entry.timestamp.desc())
	return object_list('index.html', query, check_bounds=False)

@app.route('/<slug>/')
def detail(slug):
	if session.get('logged_in'):
		query = Entry.select()
	else:
		query = Entry.public()
	entry = get_object_or_404(query, Entry.slug == slug)
	return render_template('detail.html', entry=entry)

@app.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
	entry = get_object_or_404(Entry, Entry.slug == slug)
	if request.method == 'POST':
		if request.form.get('title') and request.form.get('content'):
			entry.title = request.form['title']
			entry.content = request.form['content']
			entry.published =  request.form.get('published') or False
			entry.save()

			flash('Entry saved successfully.', 'sucess')
			if entry.published:
				return redirect(url_for('detail', slug=entry.slug))
			else:
				return redirect(url_for('edit', slug=entry.slug))
		else:
			flash('Title and content are required.', 'danger')

	return render_template('edit.html',entry=entry)

#全文搜索时试用Temperate Filter 过滤搜索文字中不需要的内容，保证搜索的准确性
@app.template_filter('clean_querystring')
def clean_querystring(request_args, *keys_to_remove, **new_values):
	querystring = dict((key, value) for key, value in request_args.items())
	for key in keys_to_remove:
		querystring.pop(key, None)
	querystring.update(new_values)
	return urllib.urlencode(querystring)

#自定义404页面
@app.errorhandler(404)
def not_found(exc):
	return Response('<h3>Page not found</h3>'), 404


def main():
	database.create_tables([Entry, FTSEntry], safe=True)
	app.run(debug=True)

if __name__ == '__main__':
	main()


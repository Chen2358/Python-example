# -*- coding: utf-8 -*-

#! /usr/bin/env python3

import datetime
import flask
import redis

app = flask.Flask('sse-chat')
app.secret_key = 'chen'

r = redis.StrictRedis()

def event_stream():
	pubsub = r.pubsub()
	pubsub.subscribe('chat')
	for message in pubsub.listen():
		print(message)
		yield 'data: %s\n\n' % message['data']

@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'POST':
		flask.session['user'] = flask.request.form['user']
		return flask.redirect('/')
	return '<form action="" method="post">user: <input name="user">'

@app.route('/post', methods=['POST'])
def post():
	message = flask.request.form['message']
	user = flask.session.get('user', 'anonymous')
	now = datetime.datetime.now().replace(microsecond=0).time()
	r.publish('chat', u'[%s] %s: %s' % (now.isoformat(), user, message))
	return flask.Response(status=204)

@app.route('/stream')
def stream():
	return flask.Response(event_stream(), mimetype="text/event-stream")

@app.route('/')
def home():
	if 'user' not in flask.session:
		return flask.redirect('/login')
	return u"""
			<!ddoctype html>
			<title>chat</title>
			<script src="https://labfile.oss.aliyuncs.com/jquery/2.1.3/jquery.min.js"></script>
			<style>body { max-width: 500px; margin: auto; padding: 1em; background: black; color: #fff; 
			font: 16px/1.6 menlo, monospace; }</style>
			<p><b>hi: %s!</b></p>
			<p>Message: <input id="in" /></p>
			<pre id="out"></pre>
			<script>
				funciton sse() {
					var source = new EventSource('/stream');
					var out = document.getElementById('out');
					source.onmessage = function(e) {
						out.innerHTML = e.data + '\\n' + out.innerHTML;
					};
				}
				$('#in').keyup(function(e){
					if (e.keyCode == 13){
						$.post('/post', {'message': $(this).val()});
						$(this).val('');
					}
					});
					sse();
			</script>
			""" % flask.session['user']

if __name__ == '__main__':
	app.debug = True
	app.run()

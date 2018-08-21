# -*- coding: utf-8 -*-

#!/usr/bin/env python


import datetime
import flask
import redis


app = flask.Flask(__name__)
app.secret_key = 'asdf'
#设置redis 链接
red = redis.StrictRedis(host='localhost', port=6379, db=6)

#消息生成器
def event_stream():
    pubsub = red.pubsub()
    #订阅'chat'频道
    pubsub.subscribe('chat')
    # 开始监听消息，如果有消息则返回消息
    for message in pubsub.listen():
        print (message)
        yield 'data: %s\n\n' % message['data']

#登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        #记录用户信息
        flask.session['user'] = flask.request.form['user']
        return flask.redirect('/')
    return '<form action="" method="post">user: <input name="user">'

#接受 Javascript post 的消息
@app.route('/post', methods=['POST'])
def post():
    message = flask.request.form['message']
    user = flask.session.get('user', 'anonymous')
    now = datetime.datetime.now().replace(microsecond=0).time()
    #将消息发布到'chat'频道中
    red.publish('chat', u'[%s] %s: %s' % (now.isoformat(), user, message))
    return flask.Response(status=204)

#事件流接口
@app.route('/stream')
def stream():
    #返回的类型时'text/event-stream'
    return flask.Response(event_stream(),
                          mimetype="text/event-stream")


@app.route('/')
def home():
    if 'user' not in flask.session:
        return flask.redirect('/login')
    return u"""
        <!doctype html>
        <title>chat</title>
        <script src="http://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
        <style>body { max-width: 500px; margin: auto; padding: 1em; background: black; color: #fff; font: 16px/1.6 menlo, monospace; }</style>
        <p><b>hi, %s!</b></p>
        <p>Message: <input id="in" /></p>
        <pre id="out"></pre>
        <script>
            function sse() {
                //接入服务器的事件流
                var source = new EventSource('/stream');
                var out = document.getElementById('out');
                source.onmessage = function(e) {
                    // XSS in chat is fun
                    out.innerHTML =  e.data + '\\n' + out.innerHTML;
                };
            }
            // POST 消息到服务端
            $('#in').keyup(function(e){
                if (e.keyCode == 13) {
                    $.post('/post', {'message': $(this).val()});
                    $(this).val('');
                }
            });
            sse();
        </script>

    """ % flask.session['user']


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8989, threaded=True)


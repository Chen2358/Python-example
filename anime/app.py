#-*- coding: utf-8 -*-
#!/usr/bin/env python3

from flask import Flask, render_template, request
import recommend

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')
@app.route('/search/')
def search():
	#request为全局变量可得到用户输入信息
	n = request.args.get('user')
	
	dic = recommend.recommend(n)
	
	return render_template('search.html', Data=dic)

if __name__ == '__main__':
	app.run(debug=True)

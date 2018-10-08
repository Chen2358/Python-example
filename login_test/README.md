1、环境依赖

sudo pip3 install django==1.10.0

2、运行测试页面

python3 manage.py runserver

3、原理

（1）session：

session的意思是会话，服务器通过session存储和维护与单个用户之间的会话信息。

不同的用户在服务器端有不同的session，并且为了确保正常通信，每个用户的session都是唯一的。

登录过程其实就是在验证用户登录信息后在session中存储用户登录标识的过程。

（2）sessionid:

每个用户的session都有独立的、唯一的编号sessionid用来标识用户身份。

用户登录后，服务器通过从用户的session中读取登录标识来进行身份认证，因此必须要知道sessionid来访问用户的session，而使用cookie正是满足这个需求的方法。

服务器将需要浏览器存储的信息通过Set-Cookie响应头发送给浏览器，浏览器会将cookie存储在本地，并在每次访问该网站时附带发送指定的cookie以满足服务器的需求，

而通过cookie存储sessionid就是其中的一种应用。

4、构造登录请求

一个http请求由3部分组成：请求url、请求头以及请求实体(附带数据)。

在Python的urllib2库中，由urllib2.Request对象描述一个request。其中url是一个字符串、请求头是一个dict，key是请求头名称，value是请求头的内容。

5、发送请求并保存cookie

一般情况下，打开url默认使用urllib2的urlopen()函数，但是它不能处理cookie。创建能够存储cookie的opener。python内置有cookielib库来处理cookie，其中的MozillaCookieJar可以将cookie存储到文件中，并可以从文件中读取cookie。

（1）先创建MozillaCookieJar对象，再使用urllib2.HTTPCookieProcessor创建cookie处理器，

（2）最后使用urllib2.build_opener创建opener。接下来就可以用opener发送请求并存储cookie了。

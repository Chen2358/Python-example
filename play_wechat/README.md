1、微信公众平台的后台配置，服务器地址只能是80端口或者443端口，必须以 http:// 或 https:// 开头，分别对应80端口和443端口。

2、ngrok 内网穿透配置

（1）官网

https://natapp.cn/

（2）配置步骤

.注册账号，得到ngrok的Token
.下载需要的Ngrok版本，解压
.运行适合平台的执行命令
.随即就会显示登陆成功，否则显示失败

Windows使用
https://natapp.cn/article/natapp_newbie

Linux使用
https://natapp.cn/article/nohup

# 此处 ngrok 安装包下载地址以官网为准
$ wget http://download.natapp.cn/assets/downloads/clients/2_3_8/natapp_linux_386_2_3_8.zip
$ unzip natapp_linux_386_2_3_8.zip # 解压会获得一个可执行文件
$ chmod +770 ./natapp  # 给文件添加 执行权限
$ ./natapp -authtoken=xxxxx  # authtoken在配置项中

3、配置公众号

.URL 是服务器地址,头部需要加入 http://
Token 是填写，传输过程不传输 Token，需要在代码中写入
EncodingAESKey ，也可以点随机输入
加密方式：建议明文或者兼容模式
配置完成过后，点击提交。

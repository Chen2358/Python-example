依赖

sudo pip3 install itchat --upgrade

itchat

https://itchat.readthedocs.io/zh/latest/

1、微信消息获取

import itchat

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print(msg['Text'])

#避免每次运行都扫码
itchat.auto_login(hotReload=True)
itchat.run()

其中第三行即注册的操作，通过装饰符将print_content注册为处理文本消息的函数。

微信有各种类型的数据，例如图片、语音、名片、分享等，也对应不同的注册参数：

图片对应itchat.content.PICTURE

语音对应itchat.content.RECORDING

名片对应itchat.content.CARD


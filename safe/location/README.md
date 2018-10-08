1、Exif

Exif 是一种图像文件格式，它的数据存储与 JPEG 格式是完全相同的。实际上 Exif 格式就是在 JPEG 格式头部插入了数码照片的信息，包括拍摄时的光圈、快门、白平衡、ISO、焦距、日期时间等各种和拍摄条件以及相机品牌、型号、色彩编码、拍摄时录制的声音以及 GPS 全球定位系统数据、缩略图等。

2、PyQt5

PyQt 是由 Phil Thompson 开发的一个创建 GUI 应用程序的工具包。它是 Python 编程语言和 Qt 库的成功融合。目前有两个分支，分别是 PyQt5 和 PyQt4。PyQt4 基于 Qt4 开发，PyQt5 则是 Python 基于 Qt5 开发的。

3、信号与槽

信号 与 槽是 Qt 中的 核心机制。在创建事件循环之后，通过建立信号与槽的连接可以实现对象之间的通信。当信号发射时，连接的槽函数将会自动执行。在 PyQt5 中信号和槽通过 object.signal.connect() 的方式连接。

4、环境配置

（1）切换python3.5到python3.4

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.4 70 --slave /usr/bin/python3m python3m /usr/bin/python3.4m

（2）安装piexif、PyQt5模块

sudo pip3 install piexif

（3）安装Qt

wget http://mirror.bit.edu.cn/qtproject/archive/qt/5.7/5.7.0/qt-opensource-linux-x64-5.7.0.run

sudo chmod 777 qt-opensource-linux-x64-5.7.0.run

./qt-opensource-linux-x64-5.7.0.run


（4）安装PyQt5及QWebKit模块

sudo apt-get install python3-pyqt5

sudo apt-get install python3-pyqt5.qtwebkit

5、用到PyQt5的组件

（1）QLineEdit 允许用户输入或者编辑单行的纯文本，用它来显示图片路径。

（2）QPushButon 是一个按钮，当用户点击的时候会发射clicked()信号。用它来实现一个选择图片的按钮和定位的按钮。

（3）QWebView 是一个可以显示和编辑Web文档的组件，相当于一个最简单的浏览器，用它来加载地图，实现定位功能。



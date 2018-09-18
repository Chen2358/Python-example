识别图片是否是色情图片

依赖

（1）安装Pillow依赖包

sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

（2）安装Pillow

sudo pip3 install Pillow

运行

 python3 nude.py -v 1.jpg

依赖模块 

（1）numpy 
sudo python3 -m pip install --upgrade pip

sudo pip3 install numpy

（2）scipy

sudo pip3 install scipy

（3）pillow

sudo pip3 install pillow

（4）docopt

docopt 能自动地根据帮助文档构建出命令行解析器，然后从 Shell 操作命令中解析出参数字段。docopt(__doc__, version=__version__) 函数能自动根据三个双引号中的文档内容（存储于 __doc__ 中）生成命令行解析器，并将解析结果以字典对象返回。

sudo pip3 install docopt

http://docopt.org/

运行

python3 filter.py <curves> <image>

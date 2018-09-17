依赖

sudo pip3 install pygame

Pygame

Pygame 是跨平台 Python 模块，专为电子游戏设计。包含图像、声音。创建在 SDL 基础上，允许实时电子游戏研发而无需被低级语言，如 C 语言或是更低级的汇编语言束缚。基于这样一个设想，所有需要的游戏功能和理念都（主要是图像方面）完全简化位游戏逻辑本身，所有的资源结构都可以由高级语言提供

官方文档
http://www.pygame.org/docs/

常用模块

模块	              主要作用
pygame.display	  用于配置显示窗口
pygame.event	    用于管理事件队列
pygame.draw	      用于绘制图像
pygame.image	    用于加载、存储图片资源等
pygame.Rect	      自由可控的矩形容器
pygame.Surface	  图像与屏幕的对象


pygame.display 是 Pygame 中一个很重要的模块，它主要负责控制播放窗口与屏幕的模块。它有以下几个常用的方法。

（1）pygame.display.set_mode(resolution=(0,0), flags=0, depth=0) 这个函数将创建一个窗口，为我们后续的图片加载显示提供最基本的展示舞台。函数接受三个参数，并返回一个 pygame.Surface 对象。第一个参数为一个整型元组 (w, h) 分别指定了所创建窗口的宽与高；第二个参数负责控制窗口的展示模式（比如：全屏，允许改变窗口大小等），这里我们不对此做深入介绍，只是简单地将其设置为默认模式；第三个参数指定了颜色深度，这里我们也只是将其设置为默认，程序将自动为系统适配最佳的值。
（2）pygame.display.set_caption(title) 这个函数用于设置窗口的标题。
（3）pygame.display.update(rectangle=None) 该函数用于更新窗口中指定部分的内容，如果没有传入任何值，则更新整个窗口的内容。

Pygame 的事件交由 pygame.event 模块进行管理。通过 pygame.event.get() 方法可以获得事件队列。

通过循环遍历事件队列来判断我们需要的事件是否被触发，从而执行相应的操作。

常见的事件如下：

事件	                说明
QUIT	              关闭程序
KEYDOWN	            按键按下
MOUSEBUTTONDOWN	    鼠标按键按下
MOUSEMOTION	        鼠标移动
MOUSEBUTTONUP	      鼠标按键松开

ip =  "0.0.0.0"
port = 21
#上传速度	300Kb/sec (300*1024)
max_upload = 300 * 1024
#下载速度 300Kb/sec (300*1024)
max_download = 300 * 1024
#最大连接数
max_cons = 256
#最多IP连接数
max_pre_ip = 10

#被动连接端口，必须比客户端连接数多否则客户端不能连接
passive_ports = (2223, 2233)

#是否允许匿名访问
enable_anonymous = False

#是否打开记录
enable_logging = False

#日记记录文件名称
logging_name= r"pyftp.log"

#公网IP
masquerade_address = "127.0.0.1"
#欢迎标题
welcom_banner = r"Welcome to private ftp."
#默认的匿名用户路径
anonymous_path = r"/home"

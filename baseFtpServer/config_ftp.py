#

ip =  "0.0.0.0"
port = 21
#shangchuansudu	300Kb/sec (300*1024)
max_upload = 300 * 1024
#xiazaisudu 300Kb/sec (300*1024)
max_download = 300 * 1024
#
max_cons = 256
#
max_pre_ip = 10

#
passive_ports = (2223, 2233)

#
enable_anonymous = False

#
enable_logging = False

#
logging_name= r"pyftp.log"

#
masquerade_address = "127.0.0.1"
#
welcom_banner = r"Welcome to private ftp."
#
anonymous_path = r"/home"

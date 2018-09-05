from .constants import *

#打印环境变零
def getenv(args):
	if len(args) > 0:
		print(os.getenv(args[0]))
	return SHELL_STATUS_RUN

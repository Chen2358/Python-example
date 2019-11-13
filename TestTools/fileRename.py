#-*-coding: utf-8 -*-

'''
更改特定的文件名
如：将美国风格日期的文件名改为欧洲风格日期
（1）创建一个正则表达式， 可以识别美国风格日期的文本模式。
（2）调用 os.listdir()，找出工作目录中的所有文件。
（3）循环遍历每个文件名， 利用该正则表达式检查它是否包含日期。
（4）如果它包含日期，用 shutil.move()对该文件改名
'''

import shutil, os, re

#Create a regex that matches files with the American date format.
datePattern = re.compile(r"""^(.*?)
    ((0|1)?\d)-
    ((0|1|2|3)?\d)-
    ((19|20)\d\d)
    (.*?)$
    """, re.VERBOSE)

#Loop over the files in the working directory
for amerFilename in os.listdir('.'):
    mo = datePattern.search(amerFilename)
    #Skip files without a date.
    if mo == None:
        continue

    #Get the different parts of the filename.
    beforePart = mo.group(1)
    monthPart = mo.group(2)
    dayPart = mo.group(4)
    yearPart = mo.group(6)
    afterPart = mo.group(8)
    #Form the European-style filename.
    euroFilename = beforePart + dayPart + '-' + monthPart + '-' + yearPart + afterPart
    #Get the full, absolute file paths.
    absWorkingDir = os.path.abspath('.')
    amerFilename = os.path.join(absWorkingDir, amerFilename)
    euroFilename = os.path.join(absWorkingDir, euroFilename)
    #Rename the files.
    print('Renaming "%s" to "%s"...' % (amerFilename, euroFilename))
    shutil.move(amerFilename, euroFilename)

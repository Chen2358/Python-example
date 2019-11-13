#-*- coding: utf-8 -*-

import time
import re


class Processor():
    def date(self, datetime):
        """
        ����ʱ��
        :param datetime: ԭʼʱ��
        :return: �����ʱ��
        """
        if re.match('\d+����ǰ', datetime):
            minute = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(minute) * 60))
        if re.match('\d+Сʱǰ', datetime):
            hour = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - float(hour) * 60 * 60))
        if re.match('����', datetime):
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60))
        if re.match('\d+��ǰ', datetime):
            day = re.match('(\d+)', datetime).group(1)
            datetime = time.strftime('%Y-%m-%d', time.localtime(time.time()) - float(day) * 24 * 60 * 60)
        return datetime
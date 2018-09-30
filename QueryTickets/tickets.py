#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""minglinghang huochepiao chakanqi

Usage:
	tickets -[gdtkz] <from> <to> <date>

Options:
	-h, --help		xianshibangzhu caidan
	-g 				gaotie
	-d 				dongche
	-t    			tekuai
	-k				kuaisu
	-z				zhidao

Example:
	tickets beijing shanghai 2018-10-10
	tickets -dg chengdu nanjin 2018-10-10
"""

from docopt import docopt
from stations import stations
import requests
from prettytable import PrettyTable
from colorama import init, Fore

init()


#
class TrainsCollection:
	header = 'checi chezhan shijian lishi yideng erdeng gaojiruanwo ruanwo yingwo yingzuo wuzuo'.split()

	def __init__(self, available_trains, available_place, options):
		"""chanxunde huochebanci jihe
		:param available_trains: yigeliebiao, baohankehuode de huochebanci, meige
								 huochebancishiyige zidian
		:param available_place: chaxunde xuanxiang, ru gaotie, dongche etc...

		"""
		self.available_trains = available_trains
		self.available_place = available_place
		self.options =options

	@property
	def trains(self):
		for raw_train in self.available_trains:
			raw_train_list = raw_train.split('|')
			train_no =raw_train_list[3]
			initial = train_no[0].lower()
			duration = raw_train_list[10]
			if not self.options or initial in self.options:
				train = [
					train_no,
					'\n'.join([Fore.LIGHTGREEN_EX + self.available_place[raw_train_list[6]] + Fore.RESET,
																										Fore.LIGHTRED_EX + self.available_place[raw_train_list[7]] + 
																										Fore.RESET]),
					'\n'.join([Fore.LIGHTGREEN_EX + raw_train_list[8] + Fore.RESET,
																					Fore.LIGHTRED_EX + raw_train_list[9] +Fore.RESET]),
					duration,
					raw_train_list[-6] if raw_train_list[-6] else '--',
					raw_train_list[-7] if raw_train_list[-7] else '--',
					raw_train_list[-15] if raw_train_list[-15] else '--',
					raw_train_list[-8] if raw_train_list[-8] else '--',
					raw_train_list[-14] if raw_train_list[-14] else '--',
					raw_train_list[-11] if raw_train_list[-11] else '--',
					raw_train_list[-9] if raw_train_list[-9] else '--',
				]
				yield train 

	def pretty_print(self):
		pt = PrettyTable()
		pt._set_field_names(self.header)
		for train in self.trains:
			pt.add_row(train)
		print(pt)


def cli():
	"""command-line interface"""
	arguments = docopt(__doc__)
	from_station = stations.get(arguments['<from>'])
	to_station = stations.get(arguments['<to>'])
	date = arguments['<date>']

	url = ('https://kyfw.12306.cn/otn/leftTicket/queryO?'
		   'leftTicketDTO.train_date={}&'
		   'leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT').format(
		   		date, from_station, to_station
		   )

	r = requests.get(url, verify=False)
	available_trains = r.json()['data']['result']
	available_place = r.json()['data']['map']
	options = ''.join([
		key for key, value in arguments.items() if value is True
		])

	TrainsCollection(available_trains, available_place,options).pretty_print()


if __name__ == '__main':
	cli()
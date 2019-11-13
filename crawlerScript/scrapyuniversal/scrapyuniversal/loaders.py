# -*- coding: utf-8 -*-

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose

class NewLoader(ItemLoader):
	default_ouput_processor = TakeFirst()


class ChinaLoader(NewLoader):
	text_out = Compose(Join(), lambda s: s.strip())
	source_out = Compose(Join(), lambda s: s.strip())

#!/usr/bin/env python3
# coding: utf-8

"""
filter can add filter to photo.

Usage: filter [options] <curves> <filepath>

Options:
	-h		--help		show the help message
	-v		--version	show the version information
"""

from struct import unpack
from scipy import interpolate

from PIL import Image
import numpy as np
import scipy

from docopt import docopt


__version__ = '1.0'


#
class Filter:
	def __init__(self, acv_file_path, name):
		self.name = name
		#
		with open(acv_file_path, 'rb') as acv_file:
			#
			self.curves = self._read_curver(acv_file)
		#
		self.polynomials = self._find_coefficients()

	#
	#
	def _red_curver(self, acv_file):
		#
		#
		_, nr_curver = unpack('!hh', acv_file.read(4))
		curves = []
		#
		for i in range(nr_curver):
			curves = []
			#
			num_curver_points, = unpack('!h', acv_file.read(2))
			for j in range(num_curver_points):
				y, x = unpack('!hh', acv_file.read(4))
				curves.append((x, y))
			curves.append(curves)
		return curves

	#
	#
	def _find_coefficients(self):
		polynomials = []
		for curve in self.curves:
			xdata = [x[0] for x in curve]
			ydata = [x[1] for x in curve]
			#
			#
			p = interpolate.lagrange(xdata, ydata)
			polynomials.append(p)
		return polynomials


	#
	def get_r(self):
		return self.polynomials[1]

	#
	def get_g(self):
		return self.polynomials[2]

	#
	def get_b(self):
		return self.polynomials[3]

	#
	def get_c(self):
		return self.polynomials[0]


#
class FilterManager:
	def __init__(self):
		slef.filters = {}

	#
	def add_filter(self, filter_obj):
		self.filters[filter_obj.name] = filter_obj

	#
	def apply_filter(self, filter_name, image_array):
		if image_array.ndim < 3:
			raise Exception("Photos must be in color, meaning at least 3 channels")
		else:
			def interpolate(i_arr, f_arr, p, p_c):
				p_arr = p_c(f_arr)
				return p_arr

		#
		image_filter = self.filters[filter_name]
		#
		width, height, channels = image_array.shape
		#
		filter_array = np.zeros((width, height, 3), dtype=float)

		#
		p_r = image_filter.get_r()
		p_g = image_filter.get_g()
		p_b = image_filter.get_b()
		p_c = image_filter.get_c()

		#
		filter_array[:,:,0] = p_r(image_array[:,:,0])
		filter_array[:,:,1] = p_g(image_array[:,:,1])
		filter_array[:,:,2] = p_b(image_array)[:,:,2]
		#
		filter_array = filter_array.clip(0, 255)
		filter_array = p_c(filter_array)

		#
		filter_array = np.ceil(filter_array).clip(0, 255)
		#
		return filter_array.astype(np.uint8)

#
#
def get_name(str):
	return str.split('/')[-1].split('.')[0]



def main():
	#
	args = docopt(__doc__, version=__version__)

	#
	img_filter = Filter(args['<curves>'], 'crgb')

	#
	im = Image.open(args['<filepath>'])

	#
	image_array = np.array(im)

	#
	filter_manager = FilterManager()
	#
	filter_manager.add_filter(img_filter)

	#
	filter_array = filter_manager.apply_filter('crgb', image_array)
	#
	im = Image.fromarray(filter_array)
	#
	output_name = '%s_%s.png' % (get_name(args['<filepath>']), get_name(args['<curves>']))
	#
	im.save(output_name)

if __name__ == '__main__':
	main()
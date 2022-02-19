'''This is the __init__ file that will load the pyauto.* things'''
import os

from highlevel import Bench, scan_bench

dirname = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(dirname,'inst'))

for directory in os.listdir(os.path.join(dirname,'inst')):
	if os.path.isdir(directory):
		sys.path.append(os.path.join(dirname, 'inst', directory))
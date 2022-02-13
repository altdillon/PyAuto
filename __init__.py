'''This is the __init__ file that will load the pyauto.* things'''
import os

dirname = os.path.dirname(os.path.abspath(__file__))

for directory in os.listdir(os.path.join(dirname,'inst')):
	if os.path.isdir(directory):
		sys.path.append(os.path.join(dirname, 'inst', directory))
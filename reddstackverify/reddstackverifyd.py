#!venv/bin/python
from reddstackverify import core, config

def run_reddstackverifyd():
	"""
	Run the Reddstack API server
	"""
	print ("\nStarting Verify Server v{0}\n".format(config.VERSION))
	core.run()


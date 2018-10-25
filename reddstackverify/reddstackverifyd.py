#!venv/bin/python
from reddstackverify import core, config

log = config.log

def run_reddstackverifyd():
	"""
	Run the Reddstack API server
	"""
	print ("\n\n*******************************\n Starting Verify Server v{0}\n*******************************\n\n".format(config.VERSION))
	log.info("\n\n*******************************\n Starting Verify Server v{0}\n*******************************\n\n".format(config.VERSION))
	core.run()


#!venv/bin/python
from reddstackverify import core, config
import argparse
import sys
import os
import subprocess
import time
import signal

import daemonize

verify_server = None  # server subprocess handle

log = config.log


def get_pidfile_path():
    working_dir = config.get_working_dir()
    pid_filename = config.get_pid_filename() + ".pid"
    return os.path.join(working_dir, pid_filename)


def get_pid_from_pidfile(pidfile_path):

    with open(pidfile_path, "r") as f:
        txt = f.read()

    try:
        pid = int(txt.strip())
    except:
        raise Exception("Invalid PID '%s'" % pid)

    return pid


def put_pidfile(pidfile_path, pid):

    with open(pidfile_path, "w") as f:
        f.write("%s" % pid)

    return


def start_server():
	global verify_server

	pid_file = get_pidfile_path()
	server_logfile = config.get_working_dir() + '/server.log'

	try:
		if os.path.exists(server_logfile):
			logfile = open(server_logfile, "a")
		else:
			logfile = open(server_logfile, "a+")
	except OSError, oe:
		print("Failed to open '%s': %s" % (server_logfile, oe.strerror))
		sys.exit(1)

	# become a daemon
	try:
		child_pid = os.fork()
		if child_pid > 0:
			print 'PID: %d' % child_pid
			os._exit(0)

	except OSError, error:
		print 'Unable to fork. Error: %d (%s)' % (error.errno, error.strerror)
		os._exit(1)



	# if child_pid == 0:
	# 	print ("Child pid {0}".format(os.getpid()))
	#
	# 	# child! detach, setsid, and make a new child to be adopted by init
	# 	sys.stdin.close()
	# 	os.dup2(logfile.fileno(), sys.stdout.fileno())
	# 	os.dup2(logfile.fileno(), sys.stderr.fileno())
	# 	os.setsid()
	#
	# 	daemon_pid = os.fork()
	# 	if daemon_pid == 0:
	#
	# 		# daemon!
	# 		os.chdir("/")
	#
	# 	elif daemon_pid > 0:
	#
	# 		# parent (intermediate child)
	# 		sys.exit(0)
	#
	# 	else:
	#
	# 		# error
	# 		sys.exit(1)
	#
	# elif child_pid > 0:
	# 	print ("Parent pid {0}".format(os.getpid()))
	#
	# 	# grand-parent
	# 	# wait for intermediate child
	# 	pid, status = os.waitpid(child_pid, 0)
	# 	sys.exit(status)
	os.dup2(logfile.fileno(), sys.stdout.fileno())
	os.dup2(logfile.fileno(), sys.stderr.fileno())
	os.setsid()

	# start REST server
	put_pidfile(pid_file, os.getpid())

	core.run()

	#verify_server = subprocess.Popen(core.run(), shell=False)
	#put_pidfile(pid_file, verify_server.pid)

	# wait for the REST server to die
	#verify_server.wait()

	#return verify_server.returncode


def stop_server():
	global verify_server

	pid_file = get_pidfile_path()

	try:
		fin = open(pid_file, "r")
	except Exception, e:
		pass

	else:
		pid_data = fin.read().strip()
		fin.close()

		pid = int(pid_data)

		try:
			os.kill(pid, signal.SIGTERM)
		except Exception, e:
			pass

		# takes at most 3 seconds
		time.sleep(3.0)

	print("server stopped")


def run_reddstackverifyd():

	"""
	Run the Reddstack Verify server
	"""

	argparser = argparse.ArgumentParser()
	subparsers = argparser.add_subparsers(dest='action', help='the action to be taken')

	parser = subparsers.add_parser('start', help='start the Verify server')
	parser = subparsers.add_parser('stop', help='stop the Verify server')
	parser = subparsers.add_parser('version', help='Print version and exit')
	args, _ = argparser.parse_known_args()

	if args.action == 'version':
		print config.VERSION
		sys.exit(0)

	if args.action == 'start':
		print ("starting server")
		start_server()

	if args.action == 'stop':
		print ("stopping server")
		stop_server()


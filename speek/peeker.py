import psutil as ps
import platform
import socket
import distro
from datetime import datetime

system_info = {
	'ram_total': ps.virtual_memory().total / 1000**3,
	'swap_total': ps.swap_memory().total / 1000**3,
	'disk_total': ps.disk_usage('/').total / 1000**3,
	'cpu_cores': ps.cpu_count(),
	'hostname': socket.gethostname(),
	'operating_system': {
		'type': platform.system(),
	}
}

if system_info['operating_system']['type'] == 'Linux':
	system_info['operating_system']['distro'] = {
		'id': distro.id(),
		'name': distro.name(),
		'version': distro.version()
	}


def peek():
	state = {}
	load = ps.getloadavg()
	state['load'] = {
		'percent': load[0] * 100 / system_info['cpu_cores'],
		'load': [x / system_info['cpu_cores'] for x in load]
		}
	state['cpu'] = {
		'percent' : ps.cpu_percent()
	}
	mem = ps.virtual_memory()
	state['ram'] = {
		'percent' : mem.percent,
		'used' : (mem.total - mem.available) / 1000**3
	}
	disk = ps.disk_usage('/')
	state['disk'] = {
		'percent' : disk.percent,
		'used': disk.used / 1000**3
	}
	swap = ps.swap_memory()
	state['swap'] = {
		'percent': swap.percent,
		'used': swap.used / 1000**3
	}

	return state

class PeekNetwork:
	'''
		Class to help with network usage. psutil only gives psutil.net_io_counters
		so it's needed to keep the previous values in order to get speed.
	'''
	def __init__(self):
		if_stats = ps.net_if_stats()
		self.nics = list(if_stats.keys())
		
		self.time_prev = None
		self.sent_prev = []
		self.recv_prev = []
		self.total_sent_prev = None
		self.total_recv_prev = None
		for _ in self.nics:
			self.sent_prev.append(None)
			self.recv_prev.append(None)

	def peek(self, pernic = False, b = 1024):
		'''
			:param: pernic: give result per NIC
			:param: b: multiplier 1000 to get kB, 10**6 to get MB and so on
		'''
		counts = ps.net_io_counters(pernic=pernic, nowrap=True)

		if self.time_prev == None:
			self.time_prev = datetime.now()

			if pernic:
				for i, nic in enumerate(self.nics):
					self.sent_prev[i] = counts[nic].bytes_sent
					self.recv_prev[i] = counts[nic].bytes_recv
			else:
				self.total_sent_prev = counts.bytes_sent
				self.total_recv_prev = counts.bytes_recv

			return

		now = datetime.now()
		dt = (now - self.time_prev).total_seconds()

		if pernic:
			usage = []
			for i, nic in enumerate(self.nics):
				sent = (counts[nic].bytes_sent - self.sent_prev[i]) / (dt * b)
				recv = (counts[nic].bytes_recv - self.recv_prev[i]) / (dt * b)
				usage.append((sent, recv))

				self.sent_prev[i] = counts[nic].bytes_sent
				self.recv_prev[i] = counts[nic].bytes_recv
		else:
			sent = (counts.bytes_sent - self.total_sent_prev) / (dt * b)
			recv = (counts.bytes_recv - self.total_recv_prev) / (dt * b)
			usage = (sent, recv)

			self.total_sent_prev = counts.bytes_sent
			self.total_recv_prev = counts.bytes_recv


		self.time_prev = now

		return {'timestamp' : now.timestamp() , 'usage': usage}
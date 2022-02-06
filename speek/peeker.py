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
	def __init__(self, soften_span = 10):
		'''
			:param: soften_span: amount of previous timesteps to perform the soften average
		'''
		if_stats = ps.net_if_stats()
		self.nics = list(if_stats.keys())
		
		self.soften_span = soften_span
		self.counter = 0
		self.time_prev = [None for _ in range(self.soften_span)]
		self.total_sent_prev = [[] for _ in range(self.soften_span)]
		self.total_recv_prev = [[] for _ in range(self.soften_span)]

		# for pernics
		self.sent_prev = []
		self.recv_prev = []
		for _ in self.nics:
			self.sent_prev.append([[] for _ in range(self.soften_span)])
			self.recv_prev.append([[] for _ in range(self.soften_span)])

	def peek(self, pernic = False, b = 1024):
		'''
			:param: pernic: give result per NIC
			:param: b: multiplier 1000 to get kB, 10**6 to get MB and so on
		'''
		counts = ps.net_io_counters(pernic=pernic, nowrap=True)

		now = datetime.now()
		if self.time_prev[self.counter]:
			dt = (now - self.time_prev[self.counter]).total_seconds()
		else:
			dt = None

		if pernic:
			usage = []
			for i, nic in enumerate(self.nics):
				if dt:
					sent = (counts[nic].bytes_sent - self.sent_prev[i][self.counter]) / (dt * b)
					recv = (counts[nic].bytes_recv - self.recv_prev[i][self.counter]) / (dt * b)
					usage.append((sent, recv))

				self.sent_prev[i][self.counter] = counts[nic].bytes_sent
				self.recv_prev[i][self.counter] = counts[nic].bytes_recv
		else:
			usage = None
			if dt:
				sent = (counts.bytes_sent - self.total_sent_prev[self.counter]) / (dt * b)
				recv = (counts.bytes_recv - self.total_recv_prev[self.counter]) / (dt * b)
				usage = (sent, recv)

			self.total_sent_prev[self.counter] = counts.bytes_sent
			self.total_recv_prev[self.counter] = counts.bytes_recv


		self.time_prev[self.counter] = now
		self.counter = (self.counter + 1) % self.soften_span

		return {'timestamp' : now.timestamp() , 'usage': usage}
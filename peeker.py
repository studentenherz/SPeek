import psutil as ps

system_info = {
	'ram_total': ps.virtual_memory().total / 1000**3,
	'swap_total': ps.swap_memory().total / 1000**3,
	'disk_total': ps.disk_usage('/').total / 1000**3,
	'cpu_cores': ps.cpu_count()
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
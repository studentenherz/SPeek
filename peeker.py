import psutil as ps

def peek():
	state = {}
	state['load'] = ps.getloadavg()[0] * 100 / ps.cpu_count()
	state['cpu_percent'] = ps.cpu_percent()
	state['memory_percent'] = ps.virtual_memory().percent
	state['disk_usage'] = ps.disk_usage('/').percent
	state['swap_percent'] = ps.swap_memory().percent

	return state
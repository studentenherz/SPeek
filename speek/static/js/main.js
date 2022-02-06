window.onload = () => {
	main();
	socket();
};

socket = () => {
	let socket = io('/socket');
	socket.on('connect', () => {
		socket.emit('ready');
	});

	let plot = new Plot('plot', 4 * 60, 2000, 2);

	socket.on('networkdata', (data) => {
		if (data != undefined) {
			let t = parseFloat(data['timestamp']);
			usage = data['usage']
			plot.push([[t, parseFloat(usage[0])], [t, parseFloat(usage[1])]])
		}
	});
}

main = () => {

	const load_status_message = {
		'ok': 'Runing smoothly',
		'warning': 'Runing slowly',
		'error': 'Running heavily'
	};

	let setLevel = (id, value) => {
		let level = 'ok';
		if (value > 50) level = 'warning';
		if (value > 90) level = 'error';

		document.querySelector(`#${id} .gauge`).classList.remove('ok', 'warning', 'error');
		document.querySelector(`#${id} .gauge`).classList.add(level);

		return level;
	}

	let change_favicon = (level) => {
		let link = document.querySelector("link[rel~='icon']");
		if (!link) {
			let link = document.createElement('link');
			link.rel = 'icon';
			document.getElementsByTagName('head')[0].appendChild(link);
		}
		link.href = `/static/img/favicon-${level}.svg`;
	};

	updateStatus = () => {
		fetch('/getStatus')
			.then(response => response.json())
			.then(data => {
				// Update Dashboard

				// Load
				setGaugeValue('load', data['load']['percent']);
				load_level = setLevel('load', data['load']['percent']);
				document.querySelector('#load .extra').textContent = load_status_message[load_level];
				change_favicon(load_level);

				// CPU
				setGaugeValue('cpu', data['cpu']['percent']);
				setLevel('cpu', data['cpu']['percent']);

				// RAM
				setGaugeValue('ram', data['ram']['percent']);
				setLevel('ram', data['ram']['percent']);
				document.querySelector('#ram .extra span').textContent = parseFloat(data['ram']['used']).toFixed(1);

				// Swap
				setGaugeValue('swap', data['swap']['percent']);
				setLevel('swap', data['swap']['percent']);
				document.querySelector('#swap .extra span').textContent = parseFloat(data['swap']['used']).toFixed(1);

				// Disk usage '/'
				setGaugeValue('disk-root', data['disk']['percent']);
				setLevel('disk-root', data['disk']['percent']);
				document.querySelector('#disk-root .extra span').textContent = parseFloat(data['disk']['used']).toFixed(1);
			});
	};

	updateStatus();
	setInterval(updateStatus, 2000);
}
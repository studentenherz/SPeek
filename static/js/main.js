window.onload = () => {
	main();
};

main = () => {

	updateStatus = () => {
		fetch('/getStatus')
			.then(response => response.json())
			.then(data => {
				setGaugeValue('cpu', data['cpu_percent']);
				setGaugeValue('ram', data['memory_percent']);
				setGaugeValue('swap', data['swap_percent']);
				setGaugeValue('disk-root', data['disk_usage']);
			});
	};

	updateStatus();
	setInterval(updateStatus, 2000);
}
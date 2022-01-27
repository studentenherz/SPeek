window.onload = () => {
	setGaugeValue('cpu', Math.random() * 100);
	setGaugeValue('ram', Math.random() * 100);
	setGaugeValue('swap', Math.random() * 100);
	setGaugeValue('disk', Math.random() * 100);
};
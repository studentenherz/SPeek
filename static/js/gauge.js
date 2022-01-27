const successColor = '#11921c';
const warningColor = '#ff7900';
const errorColor = '#ff3333';
const softColor = '#cacaca';

let setGaugeValue = (id, value) => {
	let text = document.querySelector(`#${id} .gauge__value`);
	let gauge = document.querySelector(`#${id} .gauge`);

	const delay = 4;
	const steps = 100;

	let currentValue = parseInt(text.textContent)
	let delta = (value - currentValue) / steps;

	let counter = 0;
	let setValue = setInterval(() => {
		currentValue += delta;
		counter++;
		if (counter == steps) clearInterval(setValue);
		text.textContent = `${currentValue.toFixed(currentValue < 10 ? 1 : 0)}`
		gauge.style.background = `conic-gradient(${successColor} ${currentValue}%, ${softColor} ${currentValue}%)`;
	}, delay);
}
const gagueLength = getComputedStyle(document.documentElement).getPropertyValue('--gauge-lenght')

console.log(gagueLength)

let setGaugeValue = (id, value) => {
	let text = document.querySelector(`#${id} .gauge__value`);
	let gauge = document.querySelector(`#${id} .gauge-fill`);

	text.textContent = `${value.toFixed(value < 10 ? 1 : 0)}`
	gauge.style.strokeDashoffset = `calc(${gagueLength} * (1 - ${value / 100}))`;
}
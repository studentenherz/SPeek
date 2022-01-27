let setGaugeValue = (id, value) => {
	let gauge = document.querySelector(`#${id} .gauge`);
	gauge.style.background = `conic-gradient(#11921c ${value}%, #acacac ${value}%)`;

	let text = document.querySelector(`#${id} .gauge__text`);
	text.textContent = `${value}%`
}
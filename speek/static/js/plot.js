plot = (id) => {
	const svg = document.getElementById(id);
	width = svg.getBoundingClientRect().width
	height = svg.getBoundingClientRect().height
	let hscale = width / height;

	const xGrid = svg.querySelector('#xGrid');
	const yGrid = svg.querySelector('#yGrid');

	const xLabel = svg.querySelector('#xLabel');
	const yLabel = svg.querySelector('#yLabel');

	for (let y = 0; y <= 100; y += 20) {
		let line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
		line.setAttribute('x1', 0);
		line.setAttribute('x2', hscale * 100);
		line.setAttribute('y1', y);
		line.setAttribute('y2', y);
		yGrid.appendChild(line);

		let label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
		label.textContent = y;
		label.setAttribute('x', hscale * 100 + 5);
		label.setAttribute('y', (100 - y));
		yLabel.appendChild(label);
	}

	for (let x = 0; x <= 100; x += 20) {
		let l = document.createElementNS('http://www.w3.org/2000/svg', 'line');
		l.setAttribute('x1', x * hscale);
		l.setAttribute('x2', x * hscale);
		l.setAttribute('y1', 0);
		l.setAttribute('y2', 100);
		xGrid.appendChild(l);

		let label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
		label.textContent = x;
		label.setAttribute('x', x * hscale);
		label.setAttribute('y', 105);
		xLabel.appendChild(label);
	}
};
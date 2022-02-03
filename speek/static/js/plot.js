class Plot {
	constructor(id, nseries = 1) {
		this.svg = document.getElementById(id);
		this.series = [];
		for (let i = 0; i < nseries; i++) {
			let path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
			path.id = `${id}-${i}`;
			path.classList.add('series');
			this.svg.appendChild(path)
			this.series.push({ 'path': path, 'data': [] });
		}
		const width = this.svg.getBoundingClientRect().width;
		const height = this.svg.getBoundingClientRect().height;
		this.hscale = width / height;

		const xGrid = this.svg.querySelector('#xGrid');
		const yGrid = this.svg.querySelector('#yGrid');

		const xLabel = this.svg.querySelector('#xLabel');
		const yLabel = this.svg.querySelector('#yLabel');

		for (let y = 0; y <= 100; y += 20) {
			let line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
			line.setAttribute('x1', 0);
			line.setAttribute('x2', this.hscale * 100);
			line.setAttribute('y1', y);
			line.setAttribute('y2', y);
			yGrid.appendChild(line);

			let label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
			label.textContent = y;
			label.setAttribute('x', this.hscale * 100 + 5);
			label.setAttribute('y', (100 - y));
			yLabel.appendChild(label);
		}

		for (let x = 0; x <= 100; x += 20) {
			let lines = document.createElementNS('http://www.w3.org/2000/svg', 'line');
			lines.setAttribute('x1', x * this.hscale);
			lines.setAttribute('x2', x * this.hscale);
			lines.setAttribute('y1', 0);
			lines.setAttribute('y2', 100);
			xGrid.appendChild(lines);

			let label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
			label.textContent = x;
			label.setAttribute('x', x * this.hscale);
			label.setAttribute('y', 100 + 5);
			xLabel.appendChild(label);
		}
	}

	_update() {
		this.series.forEach(serie => {
			let d = `M${100 * this.hscale} 0`;
			serie.data.forEach(point => {
				console.log(point);
				d = d.concat(`L${point[0] * this.hscale} ${100 - point[1]}`);
			});
			serie.path.setAttribute('d', d);
		});
	}



	plot(series) {
		this.series.forEach((serie, i) => {
			serie.data = series[i];
		});
		this._update();
	}
};
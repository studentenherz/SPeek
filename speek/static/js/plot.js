class Plot {
	constructor(id, xspan = 100, yspan = 100, series = ['graph-0']) {
		/** 
		 * id: id of svg in which to draw the plot
		 * xspan, yspan: the span in user units of the graph
		 * series: ids of series
		 * 
		 * Internally graph is represented in base 100 for the smaller axis 
		 * (supposed to be y) and 100 * hscale for the biggest;
		 * 
		 * **/
		this.nseries = series.length;
		this.xspan = xspan;
		this.yspan = yspan;
		this.svg = document.getElementById(id);
		this.series = [];
		for (let i = 0; i < this.nseries; i++) {
			let path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
			path.id = series[i];
			path.classList.add('series');
			this.svg.appendChild(path)
			this.series.push({ 'path': path, 'data': [] });
		}

		this.xGrid = this.svg.querySelector('.x-grid');
		this.yGrid = this.svg.querySelector('.y-grid');

		this.xLabel = this.svg.querySelector('.x-label');
		this.yLabel = this.svg.querySelector('.y-label');

		this.draw_grids();
	}

	draw_grids() {
		const width = this.svg.getBoundingClientRect().width;
		const height = this.svg.getBoundingClientRect().height;
		this.hscale = width * (130 / 120) / height;

		this.svg.querySelectorAll('line').forEach(line => line.remove());
		this.svg.querySelectorAll('text').forEach(text => text.remove());

		for (let y = 0; y <= 100; y += 20) {
			let line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
			line.setAttribute('x1', 0);
			line.setAttribute('x2', this.hscale * 100);
			line.setAttribute('y1', y);
			line.setAttribute('y2', y);
			this.yGrid.appendChild(line);

			let label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
			label.textContent = (y * this.yspan / 100).toFixed(2);
			label.setAttribute('x', this.hscale * 100 + 5);
			label.setAttribute('y', (100 - y));
			this.yLabel.appendChild(label);
		}

		for (let x = 0; x <= 100; x += 20) {
			let lines = document.createElementNS('http://www.w3.org/2000/svg', 'line');
			lines.setAttribute('x1', x * this.hscale);
			lines.setAttribute('x2', x * this.hscale);
			lines.setAttribute('y1', 0);
			lines.setAttribute('y2', 100);
			this.xGrid.appendChild(lines);

			let label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
			label.textContent = ((100 - x) * this.xspan / 100).toFixed(2);
			label.setAttribute('x', x * this.hscale);
			label.setAttribute('y', 100 + 5);
			this.xLabel.appendChild(label);
		}
	}

	_update() {
		this.series.forEach(serie => {
			serie.data.reverse();
			const last = serie.data[0];
			let d = `M${100 * this.hscale} ${(1 - last[1] / this.yspan) * 100}`;
			serie.data.slice(1).forEach((point, i) => {
				if (last[0] - point[0] > this.xspan)
					serie.data.splice(i);
				else
					d = d.concat(`L${(this.xspan - last[0] + point[0]) * 100 * this.hscale / this.xspan} ${(1 - point[1] / this.yspan) * 100}`);
			});
			serie.path.setAttribute('d', d);
			serie.data.reverse();
		});
	}

	plot(series) {
		this.series.forEach((serie, i) => {
			serie.data = series[i];
		});
		this._update();
	}

	push(points) {
		this.series.forEach((serie, i) => {
			serie.data.push(points[i]);
		});
		this._update();
	}
};
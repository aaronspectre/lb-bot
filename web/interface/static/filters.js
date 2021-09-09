html_cards = document.getElementsByClassName('cashbox-card')
cards = Array()

for (var i = 1; i < html_cards.length; i++) {
	cards[i] = html_cards[i]
}



function filter_analyse(){
	current_filter = document.getElementById('analysisfilter').value
	if (current_filter == 'All'){
		for (var i = 1; i < cards.length; i++) {
			cards[i].style.display = 'block'
		}
		return
	}


	current_filter = 'cashbox-card-'+current_filter.toLowerCase()

	for (var i = 1; i < cards.length; i++) {
		cards[i].style.display = 'block'
		disable = false
		cards[i].classList.forEach(item => {
			if (item == current_filter)
				disable = false
			else
				disable = true
		})

		if (disable)
			cards[i].style.display = "none"
		else
			continue
	}
}



function drawGraph(){
	daysSet = []
	for (var i = 0; i <= 31; i++) {
		daysSet[i] = i+1
	}



	var dailyOrdersOptions = {
		chart: {
			type: 'line'
		},
		title: {
			text: 'Daily Orders Report',
			align: 'left'
		},
		series: [{
			name: 'Orders',
			data: [80,92,150,100,105,120,132]
		}],
		xaxis: {
			categories: daysSet
		}
	}

	var dailyPriceOptions = {
		chart: {
			type: 'line'
		},
		title: {
			text: 'Daily Income Report',
			align: 'left'
		},
		series: [{
			name: 'Income',
			data: [30,40,35,50,49,60,70,91,125]
		}],
		xaxis: {
			categories: [1991,1992,1993,1994,1995,1996,1997,1998,1999]
		}
	}

	var dailyBotOptions = {
		chart: {
			type: 'line'
		},
		title: {
			text: 'Daily Bot Report',
			align: 'left'
		},
		series: [
		{
			name: 'Orders',
			data: [50,20,35,60,99,60,75,90,87]
		},
		{
			name: 'Income',
			data: [82,63,67,57,34,56,97,91,64]
		}],
		xaxis: {
			categories: daysSet
		}
	}

	var dailyCashboxOptions = {
		chart: {
			type: 'line'
		},
		title: {
			text: 'Daily Cashbox Report',
			align: 'left'
		},
		series: [{
			name: 'Orders',
			data: [82,63,67,57,34,56,97,91,64]
		},
		{
			name: 'Income',
			data: [50,20,35,60,99,60,75,41,109]
		}
		],
		xaxis: {
			categories: daysSet
		}
	}

	var dailyOrdersChart = new ApexCharts(document.querySelector("#dailyOrdersChart"), dailyOrdersOptions);
	var dailyPriceChart = new ApexCharts(document.querySelector("#dailyPriceChart"), dailyPriceOptions);
	var dailyBotChart = new ApexCharts(document.querySelector("#dailyBotChart"), dailyBotOptions);
	var dailyCashboxChart = new ApexCharts(document.querySelector("#dailyCashboxChart"), dailyCashboxOptions);

	dailyOrdersChart.render();
	dailyPriceChart.render();
	dailyBotChart.render();
	dailyCashboxChart.render();
}
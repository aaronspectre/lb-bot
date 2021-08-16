
price = document.getElementById('price')
amount = document.getElementById('amount')
order_list = document.getElementById('order_list')
product_list = document.getElementById('product_list')
order = document.getElementById('order')


price_list = {
	'Taco': 9000,
	'Taco with Cheese': 12000,
}

function add_order(){
	if (amount.value < 0 || amount.value == 0){
		alert('Please Check Amount')
		return
	}
	let bill = product_list.value+' x'+amount.value
	let node = document.createElement('span')
	let node_text = document.createTextNode(bill)
	node.appendChild(node_text)
	node.classList.add('badge')

	order_list.appendChild(node)
	order.value += bill+'|'
	price.value = Number(price.value)+(Number(price_list[product_list.value]) * Number(amount.value))

	amount.value = '1'
}
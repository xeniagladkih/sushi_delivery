var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    var myuser = user;
	updateBtns[i].addEventListener('click', function(){
        var itemId = this.dataset.item
		var action = this.dataset.action

		console.log('itemId:', itemId, 'Action:', action)
		
        console.log('USER:', myuser)

		if (myuser === 'AnonymousUser'){
			addCookieItem(itemId, action)
		}else{
			updateUserOrder(itemId, action)
		}
	})
}

function addCookieItem(itemId, action){
	console.log('User is not authenticated')

	if(action == 'add'){
		if(cart[itemId] == undefined){
			cart[itemId] = {'quantity':1}
		}else{
			cart[itemId]['quantity'] += 1
		}
	}

	if(action == 'remove'){
		cart[itemId]['quantity'] -= 1

		if(cart[itemId]['quantity'] <= 0){
			console.log('Remove item')
			delete cart[itemId]
		}
	}

	if(action == 'delete'){
		console.log('Remove item')
		delete cart[itemId]
	}

	console.log('CART:', cart)
	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
	location.reload()
}

function updateUserOrder(itemId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'itemId':itemId, 'action':action})
		})
		.then((response) => {
            if (!response.ok) {
                // error processing
                throw 'Error';
            }
            return response.json()
        })
		.then((data) => {
		    console.log('Data:', data)
            location.reload()
		})
}
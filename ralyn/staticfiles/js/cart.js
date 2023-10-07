var updateCart = document.getElementsByClassName("update-cart")

for (var i = 0; i < updateCart.length; i++){
    updateCart[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)

        console.log('User:', user)
        if(user === 'AnonymousUser'){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action){
    console.log("Not logged in")

    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log("Remove Item")
            delete cart[productId]
        }

    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    
}

function updateUserOrder(productId, action){
    console.log("User is authenticated sending data")

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action':action})
    })
    
    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:',data)
        document.getElementById('addCart').innerHTML = `${data.total_quantity}`
    })
}

let inputfields = document.getElementsByTagName('input')
for(i = 0; i < inputfields.length; i++){
    inputfields[i].addEventListener('change', updateQuantity)   
        
}

function updateQuantity(e){
    let inputvalue = e.target.value
    let productId = e.target.dataset.product

    const data = {prod_id: productId, val: inputvalue};
    let url = '/update_quantity/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify(data)
    })
    .then(res => res.json())

    .then((data) =>{
        console.log('Success:', data);
        document.getElementById('sub_total').innerHTML = `${data.sub_total.toFixed(1)}`
        document.getElementById('final_total').innerHTML = `${data.final_total.toFixed(1)}`
        // document.getElementById('sum_quantity').innerHTML = `${data.total_quantity}`
        // document.getElementById('addCart').innerHTML = `${data.total_quantity}`
        location.reload()
    })
}
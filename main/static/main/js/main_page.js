function reg() {
            document.getElementById('registration_all').style.display='block'
            document.getElementById('logins').style.display='none'

        }


function users_btn(){
    var name = document.getElementById('user').innerHTML
    if(name != 'AnonymousUser'){
        document.getElementById('login').style.display = 'none'
        document.getElementById('logout').style.display = 'block'
    }
}
users_btn()


var count = 0
function catalog(){
    count += 1
    var el = document.getElementById('panels')
    if(count % 2 == 1){
        el.style.display='block'
    } else {
        el.style.display='none'
    }
}


window.onload = (function just_test(){
    var item = document.getElementsByClassName('cart_price')
    var product_title = document.getElementsByClassName('cart_title')
    var items = document.getElementById('detail_title')
    document.getElementById('value_cart').innerHTML = item.length
    for(var i = 0; i <= product_title.length; i++){
        if(items.innerHTML == product_title[i].innerHTML){
               document.getElementById('cart_buy_item').style.display = 'none'
               document.getElementById('cart_sold').style.display = 'block';
        }
       }
    })

// slider for price filter//
function price_sliders(){
    var slider = document.getElementById('price_slider')
    var slider_2 = document.getElementById('price_slider_2')
    document.getElementById('price_from').value=slider.value
    document.getElementById('price_to').value=slider_2.value
    slider.max = slider_2.value
    slider_2.min = slider.value

}
price_sliders()


function reject_like(){
    var user_name = document.getElementById('user').innerHTML
    if( user_name == 'AnonymousUser'){
        window.alert('необхідно увійти у систему!')
        return false
    } else {
        return true
    }
}


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


function comp_item(){
    document.getElementById('computers').style.display='block'
    document.getElementById('smartphones').style.display='none'
    document.getElementById('home_appliances').style.display='none'
    return false
}



function smart() {
    document.getElementById('smartphones').style.display='block'
    document.getElementById('computers').style.display='none';
    document.getElementById('home_appliances').style.display='none'
    return false
}

function home_stuff(){
    document.getElementById('home_appliances').style.display='block'
    document.getElementById('smartphones').style.display='none'
    document.getElementById('computers').style.display='none';
    return false
}


function itemHover1(){
    document.getElementById('item_hover1').style.backgroundColor='#396620'
}

function itemHover1_out(){
    document.getElementById('item_hover1').style.backgroundColor='transparent';

}


function itemHover2(){
    document.getElementById('item_hover2').style.backgroundColor='#396620';
}

function itemHover2_out(){
    document.getElementById('item_hover2').style.backgroundColor='transparent';
    }


function itemHover3(){
    document.getElementById('item_hover3').style.backgroundColor='#396620';
}

function itemHover3_out(){
    document.getElementById('item_hover3').style.backgroundColor='transparent';
    }

/*const req_url ='http://127.0.0.1:8000/notebook_api/9'
function send_req(){
    const xhr = new XMLHttpRequest()
    xhr.open('get', req_url)
    xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
    xhr.onload = function(){
        console.log(JSON.parse(xhr.response))
      }
    xhr.send(data)
  }
*/



function reg() {
            document.getElementById('registration_all').style.display='block'
            document.getElementById('logins').style.display='none'

        }

//change buttons login/logout//
function users_btn(){
    if(document.URL != 'https://my-petshop.herokuapp.com'){
        document.getElementById('login').style.display = 'none'
        var name = document.getElementById('user').innerHTML
        if(name != 'AnonymousUser'){
            document.getElementById('logout').style.display = 'block'
         }
    } else{
        var name = document.getElementById('user').innerHTML
        if(name != 'AnonymousUser'){
            document.getElementById('login').style.display = 'none'
            document.getElementById('logout').style.display = 'block'
         }
      }
    }
users_btn()

//active menu//
var count_panel = 0
function active_panel(){
    count_panel += 1
    if(count_panel % 2 == 1){
        document.getElementById('main_panels').style.transform = 'translateX(0%)'
        if(window.screen.width > 1200){
            document.getElementById('main_panels').style.width = '25%'
          } else {
            document.getElementById('main_panels').style.width = '35%'
          }

    } else {
        document.getElementById('main_panels').style.transform = 'translateX(-103%)'



     }
}


//active menu on phone///
function manage_panel(){
    count_panel += 1
    if(count_panel % 2 == 1){
        document.getElementById('main_panels').style.transform='translateX(0%)'
        } else {
            document.getElementById('main_panels').style.transform='translateX(-110%)'
        }
    }

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


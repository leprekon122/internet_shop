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
}



function smart() {
    document.getElementById('smartphones').style.display='block'
    document.getElementById('computers').style.display='none';
    document.getElementById('home_appliances').style.display='none'
}

function home_stuff(){
    console.log('true')
    document.getElementById('home_appliances').style.display='block'
    document.getElementById('smartphones').style.display='none'
    document.getElementById('computers').style.display='none';
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


function users_btn(){
    if(document.URL != 'http://127.0.0.1:8000/'){
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


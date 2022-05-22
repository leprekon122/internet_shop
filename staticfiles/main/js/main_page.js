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


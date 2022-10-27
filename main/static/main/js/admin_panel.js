function find_username(){
    var res = document.getElementsByClassName('username')

    if (res[0].innerHTML == 'None'){
        document.getElementById('personal_data').style.display = 'none'
    }

}
find_username()
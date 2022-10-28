function pay_status(){
    document.getElementById('pay_with_card').style.display = 'block'
}

function pay_status_off(){
    document.getElementById('pay_with_card').style.display = 'none'
}

/* check order form */

function write_data(){
    res = document.getElementsByClassName('personal_data')
    for (let i = 0; i <= res.length; i++){
        data = res[i].value
        console.log(data)
        if (data == ''){
            window.alert('Заповніть усі поля позначені (*)')
            return false
        }
    }
}
var count = 0
function manage_panel(){
    count += 1
    if(count % 2 == 1){
        document.getElementById('main_panels').style.display='block'
        } else {
            document.getElementById('main_panels').style.display='none'
        }
}
function start_hover(){
    document.getElementById('detail_start_a').style.color = '#13cf2b'
}
start_hover()

function add_comm(){
    var user = document.getElementById('user').innerHTML
    if(user == 'AnonymousUser'){
          window.alert('Вам потрібно авторезуватись!')
          return false
        }
    return true
    }



function detail_color_video(){
    document.getElementById('detail_pic').style.display = 'none'
    document.getElementById('video_youtube').style.display = 'block'
    document.getElementById('detail_comments').style.color = '#fff'
    document.getElementById('detail_question').style.color = '#fff'
    document.getElementById('detail_start_a').style.color = '#fff'
    document.getElementById('detail_video').style.color = '#13cf2b'
}


function detail_color_comments(){
    document.getElementById('detail_comment').style.display = 'block'
    document.getElementById('detail_pic').style.display = 'block'
    document.getElementById('detail_questions').style.display = 'none'
    document.getElementById('video_youtube').style.display = 'none'
    document.getElementById('detail_comments').style.color = '#13cf2b'
    document.getElementById('detail_question').style.color = '#fff'
    document.getElementById('detail_start_a').style.color = '#fff'
    document.getElementById('detail_video').style.color = '#fff'
}


function detail_color_question(){
    document.getElementById('detail_questions').style.display = 'block'
    document.getElementById('detail_pic').style.display = 'block'
    document.getElementById('detail_comment').style.display = 'none'
    document.getElementById('video_youtube').style.display = 'none'
    document.getElementById('detail_comments').style.color = '#fff'
    document.getElementById('detail_question').style.color = '#13cf2b'
    document.getElementById('detail_start_a').style.color = '#fff'
    document.getElementById('detail_video').style.color = '#fff'
}





/*var csrf_token = ''
function get_csrf_token(){
    var token = document.cookie.split('=')
    csrf_token = token[1]
}
get_csrf_token() */




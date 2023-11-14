let menu = document.getElementById('bg')


function toggle () {
    let ul = document.getElementById('link-ul')
    if (ul.classList.contains('link-ul2')){
        menu.src = "./img/close.png"
        ul.classList.remove('link-ul2')
    }
    else{
        menu.src = "./img/open.png"
        ul.classList.add('link-ul2')
    }

}
menu.addEventListener("click", toggle)
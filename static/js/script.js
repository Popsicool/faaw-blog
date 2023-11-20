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

let arrow = document.getElementById('down-arrow')
function offLast(){
    document.getElementById('last-comment').style.display = "none"
    document.getElementById('all-comment').style.display = "block"
}
arrow.addEventListener('click', offLast)

let arrow2 = document.getElementById('up-arrow')
function offAll(){
    document.getElementById('last-comment').style.display = "block"
    document.getElementById('all-comment').style.display = "none"
}
arrow2.addEventListener('click', offAll)
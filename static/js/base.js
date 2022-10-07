function changeTopnav() {
    var navbar = document.getElementById('topnav');
    var scrollvalue = window.scrollY;
    console.log(scrollvalue);
    if(scrollvalue < 30) {
        navbar.classList.remove('topnav-color');
    } else {
        navbar.classList.add('topnav-color');
    }
}

window.addEventListener('scroll', changeTopnav);

setTimeout(() => {
    $('.alert').alert('close')
}, 5000)
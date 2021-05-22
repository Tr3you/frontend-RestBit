let menutoggle = document.querySelector('.menu-toggle');
let menutoggle_icon = document.querySelector('.menu-toggle i');
let menu = document.getElementById('menu');

menutoggle.addEventListener('click', e=>{
    menu.classList.toggle('show')
});
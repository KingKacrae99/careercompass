const menuBtn = document.querySelector(".menu-btn");
const navBar = document.querySelector("nav");
const getYear = document.querySelector('#year');
const date = new Date()
const year = date.getFullYear()

window.addEventListener("load", ()=> {
    const loader = document.querySelector(".loader");

    setTimeout(() => {
      loader.classList.add("loader-hidden")  
    }, 2500)

    loader.addEventListener("transitionend", () => {
        loader.remove()
    })
})

getYear.innerHTML = year;

menuBtn.addEventListener('click', () => {
    navBar.classList.toggle('open');
});

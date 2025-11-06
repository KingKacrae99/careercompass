const header = document.querySelector("header");
const footer = document.querySelector("footer");
const menu = document.getElementById("menu");
const sideBar = document.querySelector(".nav-details");
const closeModal = document.getElementById("closeModal");

menu.addEventListener('click', () => {
    sideBar.showModal()
    menu.style.display = "none";
})
closeModal.addEventListener('click', () => {
    sideBar.close()
    menu.style.display = "flex";
})
header.style.display = "none";
footer.style.display = "none";
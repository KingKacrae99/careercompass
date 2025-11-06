const menuBtn = document.querySelector(".menu-btn");
const SidebarList = document.querySelector(".menu-list ul")

if (menuBtn && SidebarList) {
    menuBtn.addEventListener('click', () => {
        SidebarList.classList.toggle('open');
    });
}

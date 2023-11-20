console.log("cargando codigo");

window.addEventListener("DOMContentLoaded", (event) =>{
    console.log("DOM completamente cargado y procesado");

    const menuBtn = document.getElementById("menu");
    const nav = document.querySelector(".menu nav");
    const body = document.querySelector("body");

    menuBtn.addEventListener("click", (event) =>  {
        menuBtn.classList.toggle("salir");
        nav.classList.toggle("visible");
        body.classList.toggle("no.scroll");
    })
    }
    )

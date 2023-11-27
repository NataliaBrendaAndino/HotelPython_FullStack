console.log("cargando codigo");

window.addEventListener("DOMContentLoaded", (event) =>{

    const menuBtn = document.getElementById("menu");
    const nav = document.querySelector(".menu nav");
    const body = document.querySelector("body");

    menuBtn.addEventListener("click", (event) =>  {
        menuBtn.classList.toggle("salir");
        nav.classList.toggle("visible");
        body.classList.toggle("no.scroll");

        console.log("DOM completamente cargado y procesado");
    })
    }
    )

// Rendu des notes en étoiles
rate_value = document.body.querySelectorAll("p.rate")
if (rate_value){
    rate_value.forEach(element => {
        var rate = parseInt(element.innerHTML, 10);
        element.innerHTML = ''
        if (!isNaN(rate)){
            for (var i = 0; i < rate; i++) {
                var img = new Image(20)
                img.src = "/static/images/star.png"
                element.append(img)
            }
        }
        
    });
}

// Menu sticky

window.onscroll = function(){
    stickyFunction()
}

var navbar = document.getElementById("header");
var sticky = navbar.offsetTop;

function stickyFunction(){
    if (window.scrollY > sticky){
        navbar.classList.add("sticky")
    } else {
        navbar.classList.remove("sticky")
    }
}


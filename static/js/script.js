rate_value = document.body.querySelectorAll("p.rate")

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


setInterval(function getData(){
    var direction = document.getElementById('direction')
    var velocity = document.getElementById('velocity')
    var power = document.getElementById('power')
    var object = document.getElementById('object')

    fetch(`${window.origin}/`).then((resp) => resp.json())
    .then(function(text){
            direction.innerText = text.direction;
            velocity.innerText = text.velocity+" m/s";
            power.innerText = text.power+" Watts";
    }).catch(function(error){
            console.log(error)
    })
    fetch(`${window.origin}/shape`).then((resp) => resp.json())
    .then(function(text){
            if (text.shape != ""){
                object.innerText = text.shape
            }
            else{
                object.innerText = "Nothing yet"
            }
    }).catch(function(error){
            console.log(error)
    })

},1000);



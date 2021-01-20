setInterval(function getData(){
    var direction = document.getElementById('direction')
    var velocity = document.getElementById('velocity')
    var power = document.getElementById('power')
    var object = document.getElementById('object')

    fetch(`${window.origin}/`).then((resp) => resp.json())
    .then(function(text){
            direction.innerText = text.direction;
            velocity.innerText = text.velocity+" m/s";
            power.innerText = text.power+" mWatts";
    }).catch(function(error){
            console.log(error)
    })
//     fetch(`${window.origin}/shape`).then((resp) => resp.json())
//     .then(function(text){
//             if (text.shape != ""){
//                 object.innerText = text.shape
//             }
//     }).catch(function(error){
//             console.log(error)
//     })

},500);



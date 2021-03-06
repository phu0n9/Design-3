var myGamePiece;
var str;

var data = {}
var myGamePiece;
var firstLand;
var startLocation;
var secondLand;
var thirdLand;
var first_manual_land;
var second_manual_land;
var transfer_data;
var count = 0;

// Drawing multiple rectangles
function startGame() {
    myGameArea.start();
    firstLand = new component(410,10,"orange",50,240,"");
    secondLand = new component(15,220,"orange",445,20,"");
    thirdLand = new component(185,10,"orange",275,20,"");
    first_manual_land = new component(243,10,"purple",45,20,"");
    second_manual_land = new component(15,220,"purple",30,20,"");
    startLocation = new component(30,30,"green",20,230,"start Location");
    myGamePiece = new component(10, 10, "red", 40, 240,"");
}

var myGameArea = {
    canvas : document.createElement("canvas"),
    start : function() {
        this.canvas.width = 480;
        this.canvas.height = 270;
        this.text = "";
        this.context = this.canvas.getContext("2d");
        document.body.insertBefore(this.canvas, document.body.childNodes[0]);
        this.interval = setInterval(updateGameArea, 10);
        window.addEventListener('keydown', function (e) {
            myGameArea.key = e.keyCode;
        })
        window.addEventListener('keyup', function (e) {
            myGameArea.key = false;
        })
    }, 
    clear : function(){
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
}

// Create rectangles boxes using this
function component(width, height, color, x, y,text) {
    this.gamearea = myGameArea;
    this.width = width;
    this.height = height;
    this.speedX = 0;
    this.speedY = 0;    
    this.x = x;
    this.y = y;    
    this.text = text;
    this.update = function() {
        ctx = myGameArea.context;
        ctx.fillStyle = color;
        ctx.fillText(text,x+30,y+5);
        ctx.font = '10px Courier';
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
    this.newPos = function() {
        this.x += this.speedX;
        this.y += this.speedY;        
    }
}

// get turn right API from back end
function get_turn_right_button(){
    fetch(`${window.origin}/right`).then((resp) => resp.json())
    .then(function(text){
        //do nothing
     })
    .catch(function(error){
            console.log(error)
    })
    myGamePiece.speedY = -1;
}

// get turn left API from back end
function get_turn_left_button(){
    fetch(`${window.origin}/left`).then((resp) => resp.json())
    .then(function(text){
        //do nothing
     })
    .catch(function(error){
            console.log(error)
    })
    myGamePiece.speedY = 1;
}

// get going up API from back end
function get_turn_up_button(){
    fetch(`${window.origin}/up`).then((resp) => resp.json())
    .then(function(text){
        //do nothing
     })
    .catch(function(error){
            console.log(error)
    })
    myGamePiece.speedX = -1;
}

// get going down API from back end
function get_turn_down_button(){
    fetch(`${window.origin}/down`).then((resp) => resp.json())
    .then(function(text){
        //do nothing
     })
    .catch(function(error){
            console.log(error)
    })
    myGamePiece.speedX = 1;
}

// get forklift up API from back end
function lift_up(){
    fetch(`${window.origin}/lift_up`).then((resp) => resp.json())
    .then(function(text){
       //do nothing
    }).catch(function(error){
            console.log(error)
    })
}

// get forklift down API from back end
function lift_down(){
    fetch(`${window.origin}/lift_down`).then((resp) => resp.json())
    .then(function(text){
        //do nothing
     })
    .catch(function(error){
            console.log(error)
    })
}

// detecting if keyboard is pressed
function manualControl(){
    if (myGameArea.key && myGameArea.key == 65) {get_turn_left_button() }
    if (myGameArea.key && myGameArea.key == 68) { get_turn_right_button()}
    if (myGameArea.key && myGameArea.key == 83) { get_turn_down_button()}
    if (myGameArea.key && myGameArea.key == 87) { get_turn_up_button()}
    if (myGameArea.key == 79){lift_up()}
    if (myGameArea.key == 80){lift_down()}
    if (myGameArea.key != 65 && myGameArea.key != 68 && myGameArea.key != 87 && myGameArea.key != 83 && myGameArea.key != 79 && myGameArea.key != 80){myGamePiece.speedY = 0; myGamePiece.speedX = 0;}
}

// get start API from back end
function startButton(){
    fetch(`${window.origin}/stop`).then((resp) => resp.json())
    .then(function(text){
        //do nothing
    }).catch(function(error){
            console.log(error)
    })
}

// get change mode API from back end
function changeState(){
    fetch(`${window.origin}/mode`).then((resp) => resp.json())
    .then(function(text){
        //do nothing
    }).catch(function(error){
        console.log(error)
    })
}

// chceck if start keyboard or change mode keyboard is pressed
function checkStartOnPressed(){
    if (myGamePiece.x == 40 && myGamePiece.y == 240){
        if (myGameArea.key == 82){
            startButton()
            count = 1
        }
    }
    else if(myGamePiece.x == 285 && myGamePiece.y == 20){
        if(myGameArea.key == 77){
            changeState()
            count = 2
        }
    }
    return count
}

function updateGameArea() {
    myGameArea.clear();
    myGamePiece.speedX = 0;
    myGamePiece.speedY = 0;    
    if(myGamePiece.x -myGamePiece.width <= 0){
        myGamePiece.x = 0 + myGamePiece.width
    }
    else if(myGamePiece.x - myGamePiece.width > myGameArea.width){
        myGamePiece.x = myGameArea.width - myGamePiece.width
    }
    else if(myGamePiece.y - myGamePiece.height < myGameArea.height){
        myGamePiece.y = myGameArea.height + myGamePiece.height
    }

    if (checkStartOnPressed() == 1){                                                            // if start keyboard is pressed
        if(myGamePiece.x  - myGamePiece.width < second_manual_land.width){
            myGamePiece.x = second_manual_land.width + myGamePiece.width + 8
        }
        else if(myGamePiece.y - myGamePiece.height > startLocation.y){
            myGamePiece.y = startLocation.y + myGamePiece.height 
        }
    
        if (myGamePiece.y == firstLand.y && myGamePiece.x != secondLand.x){
            myGamePiece.speedX += 1;
            myGamePiece.speedY = 0;
        }
        else if(myGamePiece.y == firstLand.y && myGamePiece.x == secondLand.x){
            myGamePiece.speedX = 0;
            myGamePiece.speedY -= 1;
        }
        else if(myGamePiece.y != thirdLand.y && myGamePiece.x == secondLand.x){
            myGamePiece.speedX = 0;
            myGamePiece.speedY -= 1;
        }
        else if(myGamePiece.y == thirdLand.y && myGamePiece.x - myGamePiece.width > thirdLand.x){
            myGamePiece.speedX -= 1;
            myGamePiece.speedY = 0;
        }
    }
    else if (checkStartOnPressed() == 2){                                                       // if the state is in manual mode, press m to switch state
        myGamePiece.speedX = 0;
        myGamePiece.speedY = 0;    
        manualControl()
        if(myGamePiece.y  - myGamePiece.height < first_manual_land.height){
            myGamePiece.y = first_manual_land.height + myGamePiece.height
        }
        else if(myGamePiece.y + myGamePiece.height > second_manual_land.height){
            myGamePiece.y = second_manual_land.height - myGamePiece.height
        }
    
    }
    firstLand.update();
    secondLand.update();
    thirdLand.update();
    first_manual_land.update();
    second_manual_land.update();
    startLocation.update();
    myGamePiece.newPos();    
    myGamePiece.update();
}

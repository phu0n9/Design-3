var myGamePiece;
var firstLand;
var startLocation;
var secondLand;
var thirdLand;
var first_manual_land;
var second_manual_land;
var str;

var data = {}

function addLocation(){
    fetch(`${window.origin}/`,{
        method: "POST",
        credentials: "include",
        body: JSON.stringify(data),
        cache: "no-cache",
        headers: new Headers({
            'Accept':'application/json',
            'Content-Type':'application/json'
        })
    }).then(function(){
	manualControl()
	console.log("Added")
    })        
    .catch(err => console.log(err))           
}

function updateLocation(){
    fetch(`${window.origin}/`,{
        method: "PUT",
        credentials: "include",
        body: JSON.stringify({id:0,data}),
        cache: "no-cache",
        headers: new Headers({
            'Accept':'application/json',
            'Content-Type':'application/json'
        })
    }).then(function(){
        updateGameArea();
        console.log("Updated")
    })        
    .catch(err => console.log(err))      
}

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
        this.canvas.width = 580;
        this.canvas.height = 460;
        this.text = "";
        this.context = this.canvas.getContext("2d");
        document.body.insertBefore(this.canvas, document.body.childNodes[0]);
        this.interval = setInterval(updateGameArea, 20);
        window.addEventListener('keydown', function (e) {
            myGameArea.key = e.keyCode;
            addLocation();
        })
        window.addEventListener('keyup', function (e) {
            myGameArea.key = false;
        })
    }, 
    clear : function(){
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
}

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

function manualControl(){
    if (myGameArea.key && myGameArea.key == 65) {myGamePiece.speedX = -1; str = "a";}
    if (myGameArea.key && myGameArea.key == 68) {myGamePiece.speedX = 1; str = "d";}
    if (myGameArea.key && myGameArea.key == 87) {myGamePiece.speedY = -1; str = "s";}
    if (myGameArea.key && myGameArea.key == 83) {myGamePiece.speedY = 1; str = "w";}
    data = {
            'key':str
        }
}

function updateGameArea() {
    myGameArea.clear();
    myGamePiece.speedX = 0;
    myGamePiece.speedY = 0;    

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
    else{
        myGamePiece.speedX = 0;
        myGamePiece.speedY = 0;    
        manualControl();
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


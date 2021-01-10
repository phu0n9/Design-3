var myGamePiece;
var str;

var data = {}
function startGame() {
    myGameArea.start();
    myGamePiece = new component(45, 30, "blue", 10, 120);
}

var myGameArea = {
    canvas : document.createElement("canvas"),
    start : function() {
        this.context = this.canvas.getContext("2d");
        document.body.insertBefore(this.canvas, document.body.childNodes[2]);
        this.interval = setInterval(updateGameArea, 20);
        window.addEventListener('keydown', function (e) {
            myGameArea.key = e.keyCode;
            addLocation();
            // updateLocation();
        })
        window.addEventListener('keyup', function (e) {
            myGameArea.key = false;
        })
    }, 
    clear : function(){
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }
}

function component(width, height, color, x, y) {
    this.gamearea = myGameArea;
    this.width = width;
    this.height = height;
    this.speedX = 0;
    this.speedY = 0;    
    this.x = x;
    this.y = y;    
    this.update = function() {
        ctx = myGameArea.context;
        ctx.fillStyle = color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
    }
    this.newPos = function() {
        this.x += this.speedX;
        this.y += this.speedY;        
    }
}

function updateGameArea() {
    myGameArea.clear();
    myGamePiece.speedX = 0;
    myGamePiece.speedY = 0;    
    if (myGameArea.key && myGameArea.key == 65) {myGamePiece.speedX = -1; str = "a";}
    if (myGameArea.key && myGameArea.key == 68) {myGamePiece.speedX = 1; str = "d";}
    if (myGameArea.key && myGameArea.key == 87) {myGamePiece.speedY = -1; str = "s";}
    if (myGameArea.key && myGameArea.key == 83) {myGamePiece.speedY = 1; str = "w";}
    data = {
            'key':str
        }
    myGamePiece.newPos();    
    myGamePiece.update();
}

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
        updateGameArea();
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

var myGamePiece;

var data = {'x':0,'y':0}
function startGame() {
    myGameArea.start();
    myGamePiece = new component(30, 30, "blue", 10, 120);
}

var myGameArea = {
    canvas : document.createElement("canvas"),
    start : function() {
        this.canvas.width = 480;
        this.canvas.height = 270;
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
    data = {
            'x':myGamePiece.x,
            'y':myGamePiece.y
        }
    if (myGameArea.key && myGameArea.key == 65) {myGamePiece.speedX = -1; }
    if (myGameArea.key && myGameArea.key == 68) {myGamePiece.speedX = 1; }
    if (myGameArea.key && myGameArea.key == 87) {myGamePiece.speedY = -1; }
    if (myGameArea.key && myGameArea.key == 83) {myGamePiece.speedY = 1; }

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
    }).then(response => updateGameArea())
        console.log('Added')
}

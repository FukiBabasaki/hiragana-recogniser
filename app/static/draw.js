var canvas;
var context;
var clickX = new Array();
var clickY = new Array();
var clickDrag = new Array();
var paint = false;
var curColor = "#000000";

/**
    - Preparing the Canvas : Basic functions
**/
function drawCanvas() {
    canvas = document.getElementById('canvas');
    
    side = Math.min(window.innerWidth, window.innerHeight, 420)
    canvas.width = side;
    canvas.height = side;

    context = canvas.getContext("2d");
    context.fillStyle = "rgb(200,0,0)";

    $('#canvas').mousedown(function (e) {
        var mouseX = e.pageX - this.offsetLeft;
        var mouseY = e.pageY - this.offsetTop;

        paint = true;
        addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop);
        redraw();
    });

    $('#canvas').mousemove(function (e) {
        if (paint) {
            addClick(e.pageX - this.offsetLeft, e.pageY - this.offsetTop, true);
            redraw();
        }
    });

    $('#canvas').mouseup(function (e) {
        paint = false;
    });

    window.addEventListener('resize', resizeCanvas, false);
}

/**
    - Saves the click postition
**/
function addClick(x, y, dragging) {
    clickX.push(x);
    clickY.push(y);
    clickDrag.push(dragging);
}

/**
    - Clear the canvas and redraw
**/
function redraw() {
    context.clearRect(0, 0, context.canvas.width, context.canvas.height); // Clears the canvas
    context.strokeStyle = curColor;
    context.lineJoin = "round";
    context.lineWidth = 3;
    for (var i = 0; i < clickX.length; i++) {
        context.beginPath();
        if (clickDrag[i] && i) {
            context.moveTo(clickX[i - 1], clickY[i - 1]);
        } else {
            context.moveTo(clickX[i] - 1, clickY[i]);
        }
        context.lineTo(clickX[i], clickY[i]);
        context.closePath();
        context.stroke();
    }
}

function clearDraw() {
    context.clearRect(0, 0, context.canvas.width, context.canvas.height);
    clickX = new Array();
    clickY = new Array();
    clickDrag = new Array();
}



/**
    - Encodes the image into a base 64 string.
    - Add the string to an hidden tag of the form so Flask can reach it.
**/
function save() {

    var hiragana = document.getElementById("hiragana");

    $.ajax({
        type: "POST",
        url: "/predict",
        data: JSON.stringify(canvas.toDataURL("image/png", 1.0)),
        contentType: "application/json",
        success: function(result) {
            hiragana.innerHTML = "Predicted " + result.result +" !";

            ul = document.getElementById('conf-list');
            ul.innerHTML = "";
            
            topFive = result.top_five;
            topFive.forEach(
                function(item) {
                    let li = document.createElement('li');
                    ul.appendChild(li)
                    li.innerHTML += item;
                }
            )
        }
    });
}

function resizeCanvas() {
    canvas = document.getElementById('canvas');
    
    side = Math.min(window.innerWidth - 30, window.innerHeight - 30, 420)
    canvas.width = side;
    canvas.height = side;
}

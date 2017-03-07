
$(document).ready(function() {

    var viewportWidth = window.innerWidth < 750 ? window.innerWidth  / 4 * 3 : window.innerWidth / 2;
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var isDrawing, points = [ ];

    canvas.width = viewportWidth;
    canvas.height = window.innerWidth < 750 ? viewportWidth * 4 / 3 : viewportWidth * 3 / 4;

    context.lineWidth = 10;
    context.strokeStyle = '#E51415';
    context.lineJoin = context.lineCap = 'round';

    document.body.appendChild(canvas);

    // dom actions

    $('#clear').click(function() {
        clearCanvas();
    });

    $('#save').click(function(){
        saveDrawing();
    });

    // helper functions

    function saveDrawing() {
        var dataURL = canvas.toDataURL("image/png");
        window.open(dataURL);
    }

    function addPoint(x, y, dragging) {
        var trueX = x - canvas.getBoundingClientRect().left;
        var trueY = y - canvas.getBoundingClientRect().top;

        points.push({ x: trueX, y: trueY });
    }

    function drawCanvas() {
        context.beginPath();
        if (points.length == 1) {
            context.moveTo(points[0].x, points[0].y);
            context.lineTo(points[0].x+0.1, points[0].y+0.1); // To draw a dot
        }
        else {
            context.moveTo(points[0].x, points[0].y);

            for (var i = 1; i < points.length - 2; i++) {
                var c = (points[i].x + points[i + 1].x) / 2;
                var d = (points[i].y + points[i + 1].y) / 2;

                context.quadraticCurveTo(points[i].x, points[i].y, c, d);
            }
        }

        context.stroke();
    }

    function clearCanvas() {
        points.length = 0;
        context.clearRect(0, 0, context.canvas.width, context.canvas.height);
    }

    // touch events

    canvas.ontouchstart = function(e) {
        if(e.touches) {
            if (e.touches.length == 1) {
                isDrawing = true;
                var touch = e.touches[0];
                touchX=touch.pageX-touch.target.offsetLeft;
                touchY=touch.pageY-touch.target.offsetTop;
                points.push({ x: touchX, y: touchY });
                drawCanvas();
            }
        }
        e.preventDefault();
    };

    canvas.ontouchmove = function(e) {
        if (!isDrawing) return;
        if(e.touches) {
            if (e.touches.length == 1) {
                isDrawing = true;
                var touch = e.touches[0];
                touchX=touch.pageX-touch.target.offsetLeft;
                touchY=touch.pageY-touch.target.offsetTop;
                points.push({ x: touchX, y: touchY });
                drawCanvas();
            }
        }
        e.preventDefault();
    };

    canvas.ontouchend = function(e) {
        isDrawing = false;
        points.length = 0;
        e.preventDefault();
    };

    // mouse events

    canvas.onmousedown = function(e) {
        isDrawing = true;
        addPoint(e.clientX, e.clientY);
        drawCanvas();
    };

    canvas.onmousemove = function(e) {
        if (!isDrawing) return;
        addPoint(e.clientX, e.clientY);
        drawCanvas();
    };

    canvas.onmouseup = function() {
        isDrawing = false;
        points.length = 0;
    };

    canvas.mouseleave = function() {
        isDrawing = false;
        points.length = 0;
    };
});

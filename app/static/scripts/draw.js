
$(document).ready(function() {
    var canvas = document.getElementById('drawing');
    var context = canvas.getContext('2d');

    context.lineWidth = 10;
    context.strokeStyle = '#E51415';
    context.lineJoin = context.lineCap = 'round';

    var isDrawing, points = [ ];

    $('#clear').click(function() {
        clearCanvas();
    });

    $('#send').click(function() {
        saveDrawing();
    });

    function saveDrawing() {
        var savedPNG = canvas.toDataURL("drawing.png");
        window.open(savedPNG);
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
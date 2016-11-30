
var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');

// resize the canvas
resize = function() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

// global tweakables
resolution = 50; // px
slowdown = 100;
offset_r = -25;
offset_g = 0;
offset_b = 25;
x_sampling = 100;
y_sampling = 100;
noise_function = 'perlin3';

// value sampling
get_value = function(x,y,t) {
  var value = noise[noise_function](x / x_sampling, y / y_sampling, t);
  return Math.floor(((value + 1) / 2) * 255);
}

get_style = function(x,y,t1, t2, t3) {
  return 'rgb(' + get_value(x,y,t1) + ',' + get_value(x,y,t2) + ',' + get_value(x,y,t3) + ')'
}

var frame = 0;
repaint = function() {  
  for (var y = 0; y < canvas.height; y += resolution) {
    for (var x = 0; x < canvas.width; x += resolution) {
     var fillStyle = get_style(x,y, (frame + offset_r)/slowdown, (frame + offset_g)/slowdown, (frame + offset_b)/slowdown);
      ctx.fillStyle = fillStyle;
      
      ctx.fillRect(x,y, resolution, resolution)
    }
  }
  
  frame++;
  requestAnimationFrame(repaint);
}

repaint();
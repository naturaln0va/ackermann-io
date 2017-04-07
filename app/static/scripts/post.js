
function buttonClicked(elem) {
	window.location.href = '/drafts/edit/' + elem.name;
}

var counter = 0;
var interval = setInterval(tick, 1000);

function tick() {
	counter++;

	if (counter == 30) {
		clearInterval(interval);

		xhr = new XMLHttpRequest();
		var url = "http://127.0.0.1:8080/analytics";
		xhr.open("POST", url, true);
		xhr.setRequestHeader("Content-type", "application/json");
		var path = window.location.href.toString().split(window.location.host)[1].split("/").filter(String).join(".");
		var data = JSON.stringify({"service":"ackermannio","path":path + ".sessions"});
		xhr.send(data);
	}
}

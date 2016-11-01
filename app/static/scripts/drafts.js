
function buttonClicked(elem) {
	var comps = elem.name.split(',');
	var name = comps[0];
	var id = comps[1];

	if (elem.value == 'Delete') {
		var result = confirm("Are you sure you want to delete '" + name + "'?");
		if (result == true) {
			window.location.href = '/drafts/rm/' + id;
		}
	}
	else if (elem.value == 'Edit') {
		window.location.href = '/drafts/edit/' + id;
	}
	else {
		var result = confirm("Are you sure you want to publish '" + name + "'?");
		if (result == true) {
			window.location.href = '/drafts/publish/' + id;
		}
	}
}
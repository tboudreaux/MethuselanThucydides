function format_icon(category){
	iconPaths = paths[category];

	let icon = document.createElement('svg');
	icon.setAttribute('viewBox', '0 16 16');
	icon.setAttribute('width', '16');
	icon.setAttribute('height', '16');
	icon.setAttribute('stroke', 'currentColor');
	icon.classList.add('bi');
	icon.classList.add('bi-collection');
	icon.setAttribute('xmlns', 'http://www.w3.org/2000/svg');

	// loop over each path in the paths list
	for (var i = 0; i < iconPaths.length; i++){
		let path = document.createElement('path');
		path.setAttribute('d', iconPaths[i]);
		icon.appendChild(path);
	}

	return icon;
}

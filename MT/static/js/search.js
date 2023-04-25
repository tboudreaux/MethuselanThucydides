async function fill_search_results(event) {
/**
 * Fills the search results with the search results for a query.
 *
 * @param {event} event The event that triggered the function.
 * @param {string} query The query to search for.
 */
	event.preventDefault();

	let resultsBox = document.getElementById('search-results-list');
	let searchButton = document.getElementById('search-button');
	let searchResultDropdown = new bootstrap.Dropdown(document.getElementById('search-results').querySelector("[data-bs-toggle='dropdown']"));

	let resultTemplate = document.getElementById('search-result-template');

	if (event.key == 'Enter') {
		searchResultDropdown.hide();
		searchButton.click();
	}
	
	let query = document.getElementById('search-query').value;
	if (query.length > 3) {
		console.log("======================")
		resultsBox.innerHTML = '';
		searchResultDropdown.show();
		let searchReulst = await get_search_results(query);
		for (var key in searchReulst['results']){
			var results = searchReulst['results'][key];
			for (let i = 0; i < results.length; i++) {
				let resultTemplateClone = resultTemplate.content.cloneNode(true);
				let resultItem = resultTemplateClone.querySelector('.search-result-item');
				resultItem.id = key + "_" + results[i]['uuid'];
				if (resultsBox.querySelector("#" + resultItem.id)) {
					continue;
				}
				let result = results[i];
				console.log(result);
				if (key === "papers") {
					resultItem.innerHTML = result['title'];
				} else if (key === "authors") {
					resultItem.innerHTML = result['full_name'].join(' ');
				} else if (key === "users") {
					resultItem.innerHTML = result['username'];
				}
				resultsBox.appendChild(resultItem);
			}
		}
	} else {
		searchResultDropdown.hide();
	}
}

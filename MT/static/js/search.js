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
		resultsBox.innerHTML = '';
		searchResultDropdown.show();
		let searchReulst = await get_search_results(query);
		for (var key in searchReulst['results']){
			var results = searchReulst['results'][key];
			sectionHeaderKey = key + "_search_section_header";
			if (!resultsBox.querySelector("#" + sectionHeaderKey)) {
				let sectionHeader = document.createElement('li');
				sectionHeader.innerHTML = key;
				sectionHeader.id = sectionHeaderKey;
				let seperator = document.createElement('hr');
				seperator.classList.add('dropdown-divider');
				sectionHeader.classList.add('dropdown-header');
				resultsBox.appendChild(sectionHeader);
			}
			for (let i = 0; i < results.length; i++) {
				let resultTemplateClone = resultTemplate.content.cloneNode(true);
				let resultItem = resultTemplateClone.querySelector('.search-result-item');

				let resultLink = resultItem.querySelector('.search-result-link');

				resultItem.id = key + "_" + results[i]['uuid'];
				if (resultsBox.querySelector("#" + resultItem.id)) {
					continue;
				}

				let result = results[i];
				if (key === "papers") {
					resultLink.innerHTML = result['title'];
				} else if (key === "authors") {
					resultLink.innerHTML = result['full_name'].join(' ');
				} else if (key === "users") {
					resultLink.innerHTML = result['username'];
				}
				resultLink.addEventListener('click', async() => {
					if (key === "papers") {
						await display_single_paper(result['arxiv_id']);
					}
				});
				resultsBox.appendChild(resultItem);
			}
		}
	} else {
		searchResultDropdown.hide();
	}
}

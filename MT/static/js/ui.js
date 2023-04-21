async function getDailyCategorySummaries() {
  const response = await fetch('/api/gpt/summarize/categories/latest');
  const summaries = await response.json();
  return summaries;
}

async function formatHomePage() {
	let paperList = document.getElementById('paperList');
	paperList.style.display = "none";
	let homepageDiv = document.getElementById('home');
	homepageDiv.innerHTML = "";
	homepageDiv.style = "display: block;";

	let categoryTitle = document.getElementById('category-title');
	categoryTitle.innerHTML = "";
	let summaryTemplate = document.getElementById('summary-template');
	let clonedTemplate = summaryTemplate.content.cloneNode(true);
	let summaryDiv = clonedTemplate.getElementById('cat-summary-container');

	// Get the daily category summaries
	let summaries = await getDailyCategorySummaries();
	console.log(summaries);

	for (var category in summaries['subjectSummaries']) {
		let summaryDivClone = summaryDiv.cloneNode(true);
		if (summaries['subjectSummaries'].hasOwnProperty(category)) {
			summaryDivClone.id = category + '-summary-container';
			// Get the category name
			console.log("Adding category: " + category + " to homepage");
			summaryDivClone.getElementsByClassName('card-title')[0].innerHTML = category;
			summaryDivClone.getElementsByClassName('card-text')[0].innerHTML = summaries['subjectSummaries'][category];
			summaryDivClone.getElementsByClassName('card-link')[0].addEventListener('click', function(event) { openCat(event, category); });
			summaryDivClone.getElementsByClassName('card-link')[0].innerHTML = "View " + category + " Articles";
			homepageDiv.appendChild(summaryDivClone);
		}
	}
}

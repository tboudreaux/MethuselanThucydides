/////////////////////////////
// Authentication API calls//
/////////////////////////////
async function logged_in() {
/**
 * Checks if the user is logged in by checking if the token is valid.
 *
 * @return {boolean} True if the user is logged in, false otherwise.
 */
	const response = await fetch("/login/test", {
		method: "GET",
		headers: {
			"x-access-tokens": localStorage.getItem("token"),
		},
	});
	// json = await response.json();
	if (response.status == 401){
		return false;
	} else {
		return true;
	}
}

async function get_user_from_token(){
/**
 * Gets the username of the user from the token.
 *
 * @return {string} The username of the user.
 * @return {boolean} False if the user is not logged in.
 */
	const response = await fetch("/login/test", {
		method: "GET",
		headers: {
			"x-access-tokens": localStorage.getItem("token"),
		},
	});
	json = await response.json();
	if (response.status == 401){
		return false;
	} else {
		return json.username;
	}
}


/////////////////////
// Fetch API Calls //
/////////////////////
async function getPaperList(category) {
/**
 * Gets the list of papers from the server.
 *
 * @param {string} category The category of papers to get.
 *
 * @return {object} The list of papers.
 */
	let response = await fetch('/api/papers/date/category/latest/' + category);
	let data = await response.json();
	return data;
}
async function getCategories() {
/**
 * Gets the list of categories from the server.
 *
 * @return {object} The list of categories.
 */
	let response = await fetch('/api/utils/categories');
	let data = await response.json();
	return data;
}
async function getSummary(paper_id) {
/**
 * Gets the summary of a paper from the server.
 *
 * @param {string} paper_id The id of the paper to get the summary of.
 *
 * @return {object} The summary of the paper.
 */
	let response = await fetch('/api/gpt/summarize/' + paper_id);
	let data = await response.json();
	return data;
}

async function getPaperAuthors(paper_id) {
/**
 * Gets the authors of a paper from the server.
 * @param {string} paper_id The id of the paper to get the authors of.
 *
 * @return {object} The authors of the paper.
 */
	let response = await fetch('/api/authors/paper/' + paper_id);
	let data = await response.json();
	return data;
}

async function get_user_paper_queries(arxiv_id){
/**
 * Gets the queries for a paper from the server (for the current user).
 *
 * @param {string} arxiv_id The arxiv id of the paper to get the queries of.
 *
 * @return {object} The queries for the paper.
 */
	let token = localStorage.getItem('token');
	let response = await fetch('/api/query/user/paper/' + arxiv_id, {
		method: 'GET',
		headers: {
			'x-access-tokens': token,
		},
	});
	let data = await response.json();
	return data;
}

async function get_user_all_queries(){
/**
 * Gets all the queries for the current user.
 *
 * @return {object} The queries for the user.
 */
	let token = localStorage.getItem('token');
	let response = await fetch('/api/query/all/user', {
		method: 'GET',
		headers: {
			'x-access-tokens': token,
		},
	});
	let data = await response.json();
	return data;
}

async function getDailyCategorySummaries() {
/**
 * Gets the daily summaries for each category.
 *
 * @return {object} The daily summaries for each category.
 */
  const response = await fetch('/api/gpt/summarize/categories/latest');
  const summaries = await response.json();
  return summaries;
}

async function get_paper(paper_id){
/**
 * Gets the paper from the server.
 *
 * @param {string} paper_id The id of the paper to get.
 *
 * @return {object} The paper.
 */
	let response = await fetch('/api/papers/id/' + paper_id);
	let data = await response.json();
	return data['paper'];
}

async function get_total_pages_in_category(category, resultsPerPage){
/**
 * Gets the total number of pages in a category.
 * 
 * @param {string} category The category to get the number of pages of.
 * @param {int} resultsPerPage The number of results per page.
 *
 * @return {int} The total number of pages in the category.
 */
	let response = await fetch('/api/papers/page/category/' + category + '/' + resultsPerPage + '/numPages');
	let data = await response.json();
	return data['numPages'];
}

async function get_papers_in_category_page(category, page, resultsPerPage){
/**
 * Gets the papers in a category for a given page.
 *
 * @param {string} category The category to get the papers of.
 * @param {int} page The page to get the papers of.
 * @param {int} resultsPerPage The number of results per page.
 *
 * @return {object} The papers in the category for the given page.
 */
	let response = await fetch('/api/papers/page/category/' + category + '/' + page + '/' + resultsPerPage);
	let data = await response.json();
	return data['results'];
}

//////////////////////
// Author API Calls //
//////////////////////
async function get_author(author_id) {
/**
 * Gets the author from the server.
 *
 * @param {string} author_id The id of the author to get.
 *
 * @return {object} The author.
 */
	let response = await fetch('/api/authors/uuid/' + author_id);
	let data = await response.json();
	return data;
}


////////////////////
// Info API Calls //
////////////////////
async function checkBookmark(paper_id) {
/**
 * Checks if a paper is bookmarked by the user.
 *
 * @param {string} paper_id The id of the paper to check.
 *
 * @return {boolean} True if the paper is bookmarked.
 * @return {boolean} False if the user is not logged in.
 */
	let token = localStorage.getItem('token');
	if (token == null) {
		return false;
	}
	let response = await fetch('/api/papers/bookmark/check/' + paper_id , {
		method: 'GET',
		headers: {
			'x-access-tokens': token,
		},
	});
	let data = await response.json();
	return data['bookmarked'];
}

async function resolve_category(category){
/**
 * Gets the category name and field from the category id.
 *
 * @param {string} category The category id to get the name of.
 *
 * @return {string} The name of the category.
 */
	let response = await fetch('/api/arxiv/resolve/category/' + category);
	let json = await response.json();
	return json;
}

async function checkMode(arxivID) {
/**
 * Checks if the paper is in advanced mode.
 *
 * @param {string} arxivID The arxiv id of the paper to check.
 *
 * @return {object} The mode of the paper.
 */
	let response = await fetch('/api/utils/hasFullText/' + arxivID);
	let data = await response.json();
	return data;
}

async function first_time_setup(){
/**
 * Checks if the user has completed the first time setup.
 *
 * @return {boolean} True if the user has completed the first time setup.
 * @return {boolean} False if the user has not completed the first time setup.
 */
	let response = await fetch("/api/utils/first_time_setup");
	let data = await response.json();
	if (data["first_time_setup"] == true) {
		return true;
	}
	else {
		return false;
	}
}

async function is_admin(){
/**
 * Checks if the user is an admin.
 *
 * @return {boolean} True if the user is an admin.
 * @return {boolean} False if the user is not an admin.
 */
	let response = await fetch("/api/user/is_admin", {
		headers: {
			"x-access-tokens": localStorage.getItem("token"),
		},
	});
	let data = await response.json();
	if (data["admin"] === true) {
		return true;
	}
	else {
		return false;
	}
}

async function get_search_results(query, category=null, sort=null, order=null, author=null, year=null, month=null, day=null, limit=null){
/**
 * Gets the search results for a query.
 *
 * @param {string} query The query to search for.
 * @param {string} category The category to search in.
 * @param {string} sort The sort method to use.
 * @param {string} order The order to sort in.
 * @param {string} author The author to search for.
 * @param {string} year The year to search for.
 * @param {string} month The month to search for.
 * @param {string} day The day to search for.
 * @param {string} limit The number of results to return.
 *
 * @return {object} The search results.
 *
 * @throws {string} If the query is empty.
 */
	if (query == "") {
		throw new Error("Query cannot be empty");
	}
	let endpoint = '/search'
	let payload = {
		"query": query,
		"category": category,
		"sort": sort,
		"order": order,
		"author": author,
		"year": year,
		"month": month,
		"day": day,
		"limit": limit,
	}
	let response = await fetch(endpoint, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(payload),
	});
	let data = await response.json();
	return data;
}


/////////////////////////
// Set State API Calls //
/////////////////////////
async function bookmark_paper(paper_id, on){
/**
 * Bookmarks or unbookmarks a paper.
 *
 * @param {string} paper_id The id of the paper to bookmark.
 * @param {boolean} on True to bookmark, false to unbookmark.
 *
 * @return {object} The response from the server.
 * @return {boolean} False if the user is not logged in.
 */
	console.log("bookmarking paper " + paper_id);
	let token = localStorage.getItem('token');
	if (token == null) {
		alert ('Please login to bookmark papers!');
		return false;
	}
	endpoint = on ? '/api/papers/bookmark/' : '/api/papers/unbookmark/';
	let response = await fetch(endpoint + paper_id, {
		method: 'GET',
		headers: {
			'x-access-tokens': token,
		},
	});
	let data = await response.json();
	bookmarked = await checkBookmark(paper_id);
	bookmark = document.getElementById(paper_id + '_bookmark');
	if (bookmarked) {
		bookmark.classList.add('bookmarked');
		bookmark.innerHTML = '<i class="bi bi-bookmark-check-fill"></i>';
	} else {
		bookmark.classList.remove('bookmarked');
		bookmark.innerHTML = '<i class="bi bi-bookmark"></i>';
	}
	return data;
}

async function activateAdvancedMode(arxivID) {
/**
 * Activates advanced mode for a paper.
 *
 * @param {string} arxivID The arxiv id of the paper to activate advanced mode for.
 */
	let advancedModeBtn = document.getElementById(arxivID + '_advancedMode');
	advancedModeBtn.classList.add('disabled');
	advancedModeBtn.innerHTML = 'Fetching...';

	token = localStorage.getItem('token');

	if (token == null) {
		alert ('Please login to view full text!');
		advancedModeBtn.innerHTML = 'Fetch Full Text';
		advancedModeBtn.classList.remove('disabled');
		return;
	}
	let response = await fetch('/api/fetch/ID/' + arxivID + '/long', {
		method: 'GET',
		headers: {
			'x-access-tokens': token,
		},
	});
	advancedModeBtn.innerHTML = 'Full Text Mode!';
	advancedModeBtn.classList.add('fullTextMode')
}



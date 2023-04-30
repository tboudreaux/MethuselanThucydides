async function formatHomePage() {
/**
 * Formats the home page.
 */
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

	for (var category in summaries['subjectSummaries']) {
		let summaryDivClone = summaryDiv.cloneNode(true);
		if (summaries['subjectSummaries'].hasOwnProperty(category)) {
			summaryDivClone.id = category + '-summary-container';
			summaryDivClone.classList.add('scrollFade');
			// Get the category name
			console.log("Adding category: " + category + " to homepage");
			summaryDivClone.getElementsByClassName('card-title')[0].innerHTML = category;
			summaryDivClone.getElementsByClassName('card-text')[0].innerHTML = summaries['subjectSummaries'][category];
			summaryDivClone.getElementsByClassName('card-link')[0].addEventListener('click', function(event) { openCat(event, category); });
			summaryDivClone.getElementsByClassName('card-link')[0].innerHTML = "View " + category + " Articles";
			homepageDiv.appendChild(summaryDivClone);
		}
	}
	let searchBox = document.getElementById('search-query');
	searchBox.addEventListener('keyup', async (event) => {
		fill_search_results(event);
	});
}




async function format_all_bookmarks(){
	if (await logged_in()){
		let bookmarks = document.getElementsByClassName('bookmark');
		for (let i = 0; i < bookmarks.length; i++){
			let bookmark = bookmarks[i];
			let arxiv_id = bookmark.id.split('_')[0];
			let bookmarked = await checkBookmark(arxiv_id);
			if (bookmarked){
				bookmark.classList.add('bookmarked');
				bookmark.innerHTML = '<i class="bi bi-bookmark-check-fill"></i>';
				bookmark.addEventListener('click', async () => {
					bookmark_paper(arxiv_id, false);
				});
			} else {
				bookmark.classList.remove('bookmarked');
				bookmark.innerHTML = '<i class="bi bi-bookmark"></i>';
				bookmark.addEventListener('click', async () => {
					bookmark_paper(arxiv_id, true);
				});
			}
		}
	}
}

////////////////////////
// Sidebar formatting //
////////////////////////
async function formatCategoryButtonList() {
/**
 * Formats the category button list.
 */
	let categories = Object.keys(stateInfo['paperInfo']);
	let categoryMenu = document.getElementById('cat-menu');
	
	homeButtonContainer = await format_home_button();
	categoryMenu.appendChild(homeButtonContainer);

	for (let i = 0; i < categories.length; i++) {
		navItem = await formatSingleCatButton(categories[i], categories[i]);
		categoryMenu.appendChild(navItem);
	}
}

async function format_home_button(){
/**
 * Formats the home button.
 *
 * @return {object} - The home button.
 */
	let buttonTemplate = document.getElementById('category-button-template');
	let homeButtonContainer = await buttonTemplate.content.cloneNode(true).querySelector('.nav-item');
	homeButtonContainer.id = "navItem_home";

	let homeButton = homeButtonContainer.querySelector('.nav-link');
	homeButton.href = "#home-page";
	homeButton.id = "categoryButton_home";
	homeButton.addEventListener('click', function(event) { formatHomePage(); });

	let homeButtonIcon = homeButton.querySelector('.bi');
	homeButtonIcon.classList.add('bi-house');
	homeButtonIcon.style.fontSize = "3rem";

	homeButtonName = homeButton.querySelector('.category-name');
	homeButtonName.innerHTML = " Home";

	console.log(homeButtonContainer);

	return homeButtonContainer;
}

async function formatSingleCatButton(key, name) {
/**
 * Formats a single category button.
 *
 * @param {string} key - The category key.
 * @param {string} name - The category name.
 *
 * @return {object} - The category button.
 */
	let buttonTemplate = document.getElementById('category-button-template');
	let navItem = await buttonTemplate.content.cloneNode(true).querySelector('.nav-item');
	navItem.id = "navItem_" + key;

	let button = navItem.querySelector('.nav-link');
	button.id = "categoryButton_" + key;
	button.href="#" + key;
	// button.addEventListener('click', function(event) { openCat(key, 1); });

	let icon = button.querySelector('.icon-img');
	icon.src = "/static/icons/" + key + ".webp";
	icon.alt = key;
	icon.style.maxHeight = "3rem";
	icon.style.display = "inline-block";

	let navNameContainer = button.querySelector('.category-name');
	navNameContainer.innerHTML = key;
	return navItem;
}

async function openCat(catID, currentPage) {
	const homescreen = document.getElementById("home");
	homescreen.style.display = "none";

	const footer = document.getElementById("main-content-footer");
	const paperListContainer = document.getElementById("paperList");
	const paperList = document.getElementById("paperListMain");
	const paperListPages = document.getElementById("paperListPages");
	const numPages = await get_total_pages_in_category(catID, 10);
	console.log("Number of pages: " + numPages);

	if (numPages <= 1) {
		footer.classList.add("invisibe");
	}
	else {
		footer.classList.remove("invisible");
		footer.classList.add("visible");
	}

	paperListContainer.style.display = "block";
	paperList.innerHTML = "";
	paperListPages.innerHTML = "";
	let pageSelector = await format_page_selector(catID, numPages, currentPage);
	let papers = await get_papers_in_category_page(catID, currentPage, 10);
	paperListPages.appendChild(pageSelector);
	for (let i = 0; i < papers.length; i++) {
		let paper = papers[i];
		let paperDiv = await format_paper_new(paper, stateInfo['userQueries']);
		if (paperDiv != null) {
			paperList.appendChild(paperDiv);
		} else {
			console.log("paperDiv is null");
		}
	}
}

async function format_page_selector(catID, numPages, currentPage){
	let pageSelectorTemplate = document.getElementById('page-selector-template');
	let pageSelector = pageSelectorTemplate.content.cloneNode(true).querySelector('.page-selector');

	let nextPage = pageSelector.querySelector('#next-page');
	let prevPage = pageSelector.querySelector('#prev-page');
	
	let pagation = pageSelector.querySelector('.pagination');

	let nextPageLink = nextPage.querySelector('.page-link');
	let prevPageLink = prevPage.querySelector('.page-link');

	nextPageLink.href = "#" + catID + "_" + (currentPage + 1);
	prevPageLink.href = "#" + catID + "_" + (currentPage - 1);

	if (currentPage === 1){
		prevPage.classList.add('disabled');
	} else {
		prevPage.classList.remove('disabled');
	}
	if (currentPage === numPages){
		nextPage.classList.add('disabled');
	} else {
		nextPage.classList.remove('disabled');
	}

	for (let i = 1; i <= numPages; i++){
		let pageSelectorItem = document.createElement('li');
		pageSelectorItem.classList.add('page-item');
		if (i === currentPage){
			pageSelectorItem.classList.add('active');
		}
		pageLink = document.createElement('a');
		pageLink.classList.add('page-link');
		pageLink.href = "#" + catID + "_" + i;
		pageLink.innerHTML = i;
		pageSelectorItem.appendChild(pageLink);
		pagation.insertBefore(pageSelectorItem, nextPage);
	}
	return pageSelector;
}

////////////////////////////
// User Button Formatting //
////////////////////////////
async function formatUserMeanu(){
	let loggedIn = await logged_in();
	console.log(loggedIn);
	userMeanu = document.getElementById("usr-meanu");
	userMeanu.innerHTML = "";
	if (loggedIn === true) {

		ProfileContainer = document.createElement("li");
		ProfileLink = document.createElement("a");
		ProfileLink.setAttribute("onclick", "editProfile(); return false;");
		ProfileLink.innerHTML = "Profile";
		ProfileLink.classList.add("dropdown-item");
		ProfileContainer.appendChild(ProfileLink);
		userMeanu.appendChild(ProfileContainer);

		if (await is_admin() === true) {
			newUserContainer = document.createElement("li");
			newUserLink = document.createElement("a");
			newUserLink.setAttribute("onclick", "launchNewUserModal(); return false;");
			newUserLink.innerHTML = "New User";
			newUserLink.classList.add("dropdown-item");
			newUserContainer.appendChild(newUserLink);
			userMeanu.appendChild(newUserContainer);

			generateAPIKeyContainer = document.createElement("li");
			generateAPIKeyLink = document.createElement("a");
			generateAPIKeyLink.setAttribute("onclick", "launchGenerateAPIKeyModal(); return false;");
			generateAPIKeyLink.innerHTML = "Generate API Key";
			generateAPIKeyLink.classList.add("dropdown-item");
			generateAPIKeyContainer.appendChild(generateAPIKeyLink);
			userMeanu.appendChild(generateAPIKeyContainer);
		}


		breakContainer = document.createElement("li");
		hr = document.createElement("hr");
		breakContainer.appendChild(hr);
		userMeanu.appendChild(breakContainer);

		LogOutContainer = document.createElement("li");
		LogOutLink = document.createElement("a");
		LogOutLink.setAttribute("onclick", "logout(); return false;");
		LogOutLink.innerHTML = "Log Out";
		LogOutLink.classList.add("dropdown-item");
		LogOutContainer.appendChild(LogOutLink);
		userMeanu.appendChild(LogOutContainer);
	} else {
		CreateAccountContainer = document.createElement("li");
		CreateAccountLink = document.createElement("a");
		CreateAccountLink.setAttribute("onclick", "launchRegisterModal(); return false;");
		CreateAccountLink.innerHTML = "Create Account";
		CreateAccountLink.classList.add("dropdown-item");
		CreateAccountContainer.appendChild(CreateAccountLink);
		userMeanu.appendChild(CreateAccountContainer);

		breakContainer = document.createElement("li");
		hr = document.createElement("hr");
		breakContainer.appendChild(hr);
		userMeanu.appendChild(breakContainer);

		LogInContainer = document.createElement("li");
		LogInLink = document.createElement("a");
		LogInLink.setAttribute("onclick", "launchLoginModal(); return false;");
		LogInLink.innerHTML = "Log In";
		LogInLink.classList.add("dropdown-item");
		LogInContainer.appendChild(LogInLink);
		userMeanu.appendChild(LogInContainer);
	}
}

async function formatUserButton(){
	let loggedIn = await logged_in();
	if (loggedIn === true){
		username = await get_user_from_token();
		let userButton = document.getElementById("dsp-user");
		userButton.innerHTML = username;
	} else {
		let userButton = document.getElementById("dsp-user");
		userButton.innerHTML = "Guest";
	}
	await formatUserMeanu();
}

/////////////////////////////
// Single Paper Formatting //
/////////////////////////////
async function display_single_paper(arxiv_id){
	paper = await get_paper(arxiv_id);
	paperDiv = await format_paper_new(paper, stateInfo['userQueries']);
	searchResultsContainer = document.getElementById("search-results-container");
	searchResultsContainer.innerHTML = "";
	searchResultsContainer.appendChild(paperDiv);
	launchSearchResultsModel();
}

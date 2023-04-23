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
	
	let homeButtonContainer = document.createElement('li');
	homeButtonContainer.classList.add('nav-item');
	homeButtonContainer.id = "navItem_home";
	let homeButton = document.createElement('a');
	homeButton.classList.add('nav-link');
	// homeButton.classList.add('categoryButton');
	homeButton.href = "#home";
	homeButton.classList.add('px-0');
	homeButton.classList.add('align-middle');
	homeButton.id = "categoryButton_home";
	homeButton.addEventListener('click', function(event) { formatHomePage(); });
	homeButtonIcon = document.createElement('i');
	homeButtonIcon.classList.add('bi');
	homeButtonIcon.classList.add('bi-house');
	homeButtonIcon.style.fontSize = "3rem";
	homeButtonName = document.createElement('span');
	homeButtonName.innerHTML = " Home";
	homeButtonName.classList.add('ms-1');
	homeButtonName.classList.add('d-none');
	homeButtonName.classList.add('d-sm-inline');
	homeButton.appendChild(homeButtonIcon);
	homeButton.appendChild(homeButtonName);
	
	homeButtonContainer.appendChild(homeButton);
	categoryMenu.appendChild(homeButtonContainer);


	for (let i = 0; i < categories.length; i++) {
		navItem = await formatSingleCatButton(categories[i], categories[i]);
		categoryMenu.appendChild(navItem);
	}
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
	let navItem = document.createElement('li');
	navItem.classList.add('nav-item');
	navItem.id = "navItem_" + key;

	let button = document.createElement('a');
	// button.classList.add('categoryButton');
	button.classList.add('px-0');
	button.classList.add('align-middle');
	button.classList.add('nav-link');
	button.id = "categoryButton_" + key;
	button.href="#" + key;
	
	button.addEventListener('click', function(event) { openCat(event, key); });

	let iconNameContainer = document.createElement('span');

	let icon = document.createElement('img');
	icon.classList.add('img-fluid');
	icon.src = "/static/icons/" + key + ".webp";
	icon.alt = key;
	icon.style.maxHeight = "3rem";

	iconNameContainer.appendChild(icon);



	let navNameContainer = document.createElement('span');
	navNameContainer.classList.add('ms-1');
	navNameContainer.classList.add('d-none');
	navNameContainer.classList.add('d-sm-inline');
	// navNameContainer.classList.add('col-md-10');
	navNameContainer.innerHTML = key;


	iconNameContainer.appendChild(navNameContainer);
	button.appendChild(iconNameContainer);
	navItem.appendChild(button);

	return navItem;
}

async function openCat(evt, catID) {
	const homescreen = document.getElementById("home");
	homescreen.style.display = "none";
	const paperList = document.getElementById("paperList");
	paperList.innerHTML = "";
	paperList.style.display = "block";
	for (var arxiv_id in stateInfo['paperInfo'][catID]) {
		if (stateInfo['paperInfo'][catID].hasOwnProperty(arxiv_id)) {
			let paper = stateInfo['paperInfo'][catID][arxiv_id];
			paperDiv = await format_paper_new(paper, stateInfo['userQueries']);
			if (paperDiv != null) {
				paperList.appendChild(paperDiv);
			} else {
				console.log("paperDiv is null");
			}
		}
	}
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
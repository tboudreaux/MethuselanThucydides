async function loadStateInfo() {
	let categories = await getCategories();
	stateInfo['paperInfo'] = {};
	for (var category in categories['categories']) {
		if (categories['categories'].hasOwnProperty(category)) {
			papers = await getPaperList(category);
			if (papers['papers'].length > 0) {
				stateInfo['paperInfo'][category] = {};
			}
			for (let i = 0; i < papers['papers'].length; i++) {
				let paper = papers['papers'][i];
				stateInfo['paperInfo'][category][paper.arxiv_id] = paper;
			}
		}
	}
	stateInfo['userQueries'] = await get_user_all_queries();
	// stateInfo['userBookmarks'] = await get_user_all_bookmarks();
}

async function return_to_fragment(){
	style_for_current_user();
	PAGEREGEX = "((?:[a-z]+|[A-Z]+)(?:-?)(?:(?:[a-z]+|[A-Z]+)?)(?:(?:\.?)(?:[a-z]+|[A-Z]+))?)(_?)(([1-9]+)?)";
	ISAUTHOR  = "(Author-)((?:[a-zA-Z0-9]+-){4}[a-zA-Z0-9_]+)$";
	if (window.location.hash){
		let hash = window.location.hash;
		let catID = hash.split('#')[1];
		let authorMatch = catID.match(ISAUTHOR);
		if ((catID != "home-page") && (authorMatch == null)){
			match = catID.match(PAGEREGEX);
			if (match[4] != null){
				console.log("Page number: " + match[4]);
				let pageNumber = parseInt(match[4]);
				openCat(match[1], pageNumber);

			} else{
				openCat(match[1], 1);
			}
		} else if ((catID == "home-page") && (authorMatch == null)){
			let paperList = document.getElementById('paperList');
			paperList.style.display = "none";
			let homepageDiv = document.getElementById('home');
			homepageDiv.style = "display: block;";
			let footer = document.getElementById('main-content-footer');
			footer.classList.add('invisible');
		} else {
			console.log("Going To Author")
			let authorID = authorMatch[2];
			let authorInfo = await get_author(authorID);
			format_author_page(authorInfo['info'], authorInfo['papers']);
		}
	}
}

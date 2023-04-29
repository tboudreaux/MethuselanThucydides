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

function return_to_fragment(){
	if (window.location.hash){
		let hash = window.location.hash;
		let catID = hash.split('#')[1];
		if (catID != "home-page"){
			openCat(catID);
		}
	}
}

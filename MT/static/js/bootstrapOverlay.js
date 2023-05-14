async function launchLoginModal(){
	modal = new bootstrap.Modal(document.getElementById("login"), {
		keyboard: false
	});
	modal.show();
}

async function launchNewUserModal(){
	modal = new bootstrap.Modal(document.getElementById("newUser"), {
		keyboard: false
	});
	modal.show();
}

async function launchRegisterModal(){
	modal = new bootstrap.Modal(document.getElementById("selfRegisterNewUser"), {
		keyboard: false
	});
	modal.show();
}

async function launchGenerateAPIKeyModal(){
	modal = new bootstrap.Modal(document.getElementById("generateAPIKey"), {
		keyboard: false
	});
	modal.show();
}

async function launchSearchResultsModel(){
	modal = new bootstrap.Modal(document.getElementById("displayPaperResults"), {
		keyboard: false
	});
	modal.show();
}

async function launchProfileModal(){
	modal = new bootstrap.Modal(document.getElementById("profile"), {
		keyboard: false
	});
	modal.show();
}

async function launchAuthorResultsModal(author, papers){
	console.log("Papers: ", papers);
	modalDiv = document.getElementById("author");
	modalAuthorName = document.getElementById("author-page-display-name");
	modalAuthorName.innerHTML = author;
	paperList = document.getElementById("author-papers-container");
	for (let i = 0; i < papers.length; i++){
		paper = papers[i];
		paperDiv = await format_paper_new(paper, stateInfo['userQueries']);
		paperList.appendChild(paperDiv);
	}
	modal = new bootstrap.Modal(document.getElementById("author"), {
		keyboard: false
	});
	modal.show();
}

async function clear_api_key_modal(){
	APIKeyp = document.getElementById("APIKey");
	APIKeyp.innerHTML = "";
	APIKeyp.style.display = "none";

	APIKeyMessage = document.getElementById("APIKeyMessage");
	APIKeyMessage.style.display = "block";

	generateAPIKeyButton = document.getElementById("generateKeyButton");
	generateAPIKeyButton.classList.remove("disabled");
}


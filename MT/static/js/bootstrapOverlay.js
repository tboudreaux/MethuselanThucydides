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

async function clear_api_key_modal(){
	APIKeyp = document.getElementById("APIKey");
	APIKeyp.innerHTML = "";
	APIKeyp.style.display = "none";

	APIKeyMessage = document.getElementById("APIKeyMessage");
	APIKeyMessage.style.display = "block";

	generateAPIKeyButton = document.getElementById("generateKeyButton");
	generateAPIKeyButton.classList.remove("disabled");
}


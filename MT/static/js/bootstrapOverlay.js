  $(document).ready(function () {
    function toggleSidebar() {
		console.log("toggleSidebar");
      $(".sidebar").toggleClass("sidebar-visible");
      $(".overlay").toggleClass("overlay-visible");
    }

    function hideSidebar() {
      $(".sidebar").removeClass("sidebar-visible");
      $(".overlay").removeClass("overlay-visible");
    }

    $(".toggle-sidebar").click(function () {
      toggleSidebar();
    });

    $(".overlay").click(function () {
      hideSidebar();
    });

    $(".tablinks").click(function (event) {
      event.preventDefault();
      const categoryName = $(this).text().trim();
      console.log("Clicked category: " + categoryName);
      if ($(window).width() < 992) {
        hideSidebar();
      }
    });
	      // Add a click event listener for the toggle-sidebar-button
    $(".toggle-sidebar-button").click(function () {
      toggleSidebar();
    });
  });


  function openCat(evt, catID) {
    const paperList = document.getElementById("paperList");
	  console.log(paperList);
	const catLists = paperList.getElementsByClassName("tabcontent");
    for (let i = 0; i < catLists.length; i++) {
      catLists[i].style.display = "none";
    }

    document.getElementById(catID + "-list").style.display = "block";
  }

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

async function clear_api_key_modal(){
	APIKeyp = document.getElementById("APIKey");
	APIKeyp.innerHTML = "";
	APIKeyp.style.display = "none";

	APIKeyMessage = document.getElementById("APIKeyMessage");
	APIKeyMessage.style.display = "block";

	generateAPIKeyButton = document.getElementById("generateKeyButton");
	generateAPIKeyButton.classList.remove("disabled");
}


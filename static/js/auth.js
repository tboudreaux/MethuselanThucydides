async function logged_in() {
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


async function login() {
	userName = document.getElementById("username").value;
	password = document.getElementById("password").value;
	console.log("username" + " " + userName + " : " + password);
	payload = {
		"username": userName,
		"password": password,
	};
	payloadStr = JSON.stringify(payload);
	console.log(payloadStr);
	const response = await fetch("/login", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: payloadStr,
	});

	if (response.status == 200) {
		console.log("Login successful");
		json = await response.json();
		localStorage.setItem("token", json.token);
		loginStyleUpdate(userName);
	} else {
		console.log("Login failed");
		logoutStyleUpdate();
	}
}

async function logout(){
	localStorage.removeItem("token");
	logoutStyleUpdate();
}

async function unauthorized_user_warn() {
	console.log("Unauthorized user check");
	loggeedIn = await logged_in();
	console.log("logged_in: " + loggeedIn);
	if (!loggeedIn) {
		console.log("Unauthorized user");
		myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'), {
			keyboard: false
		});
		myModal.toggle();
		logoutStyleUpdate();
	} else {
		console.log("Authorized user");
		userName = await get_user_from_token();
		loginStyleUpdate(userName);
	}
}

function loginStyleUpdate(userName){
		signInButton = document.getElementById("signIn-btn");
		signInButton.style.display = "none";
		signOutButton = document.getElementById("signOut-btn");
		signOutButton.style.display = "block";
		userText = document.getElementById("user");
		userText.innerHTML = userName;
		newUser = document.getElementById("newUser-btn");
	    newUser.style.display = "block";
	// TODO Only display this when the user is an admin
}

function logoutStyleUpdate(){
		signInButton = document.getElementById("signIn-btn");
		signInButton.style.display = "block";
		signOutButton = document.getElementById("signOut-btn");
		signOutButton.style.display = "none";
		userText = document.getElementById("user");
		userText.innerHTML = "Guest (Query Disabled)";
		newUser = document.getElementById("newUser-btn");
	    newUser.style.display = "none";
}

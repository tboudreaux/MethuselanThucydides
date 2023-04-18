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
	} else {
		console.log("Login failed");
	}
	await style_for_current_user();
}

async function logout(){
	localStorage.removeItem("token");
	await style_for_current_user();
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
	} else {
		console.log("Authorized user");
		userName = await get_user_from_token();
	}
	await style_for_current_user();
}


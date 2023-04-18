async function first_time_setup(){
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


async function enroll_user(){
	newUserName = document.getElementById("newUserUsername").value;
	newUserPassword = document.getElementById("newUserPassword").value;
	newUserEmail = document.getElementById("newUserEmail").value;
	newUserIsAdmin = document.getElementById("newUserIsAdmin").checked;

	payload = {
		"new_user": newUserName,
		"new_pass": newUserPassword,
		"new_email": newUserEmail,
		"new_user_is_admin": newUserIsAdmin,
		"new_user_is_enabled": true,
	};

	payloadStr = JSON.stringify(payload);


	const response = await fetch("/api/user/enroll_user", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"x-access-tokens": localStorage.getItem("token"),
		},
		body: payloadStr,
	});

	if (response.status == 201) {
		alert("User enrolled successfully");
	}
	else if (response.status == 409) {
		alert("User already exists");
	}
	else if (response.status == 401) {
		alert("Unauthorized");
	}
	else {
		alert("Unknown error");
	}
}

async function self_enroll_user(){
	newUserName = document.getElementById("selfNewUserUsername").value;
	newUserPassword = document.getElementById("selfNewUserPassword").value;
	newUserEmail = document.getElementById("selfNewUserEmail").value;
	newUserSecret = document.getElementById("selfNewUserSecret").value;

	payload = {
		"new_user": newUserName,
		"new_pass": newUserPassword,
		"new_email": newUserEmail,
		"new_user_secret": newUserSecret,
	};

	payloadStr = JSON.stringify(payload);

	let response = await fetch("/api/user/enroll_user/secret", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: payloadStr,
	});

	if (response.status == 201) {
		alert("User enrolled successfully");
	}
	else if (response.status == 409) {
		alert("User already exists");
	}
	else if (response.status == 401) {
		alert("Unauthorized");
	}
	else {
		alert("Unknown error");
	}
}

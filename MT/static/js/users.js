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

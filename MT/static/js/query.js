async function get_user_paper_queries(arxiv_id){
	let token = localStorage.getItem('token');
	let response = await fetch('/api/query/user/paper/' + arxiv_id, {
		method: 'GET',
		headers: {
			'x-access-tokens': token,
		},
	});
	let data = await response.json();
	return data;
}

async function format_stored_chat_log(arxiv_id) {
	allPaperDivs = document.getElementsByClassName('paper');
	for (let i = 0; i < allPaperDivs.length; i++) {
		let arxiv_id = allPaperDivs[i].id;
		let chat_log = await get_user_paper_queries(arxiv_id);
		let chat = document.getElementById(arxiv_id + '_chat');
		queries = chat_log['queries'];
		for (let i = 0; i < queries.length; i++) {
			let userMessage = document.createElement('p');
			userMessage.classList.add('user');
			userMessage.innerHTML = '<i class="fa fa-user" aria-hidden="true"></i>  ' + queries[i]['query'];
			chat.appendChild(userMessage);
			let responseMessage = document.createElement('p');
			responseMessage.classList.add('chatElement');
			responseMessage.innerHTML = '<i class="fa fa-robot" aria-hidden="true"></i>  ' + queries[i]['response'];
			chat.appendChild(responseMessage);
		}
	}
}

async function submitQuery(arxivID) {
	token = localStorage.getItem('token');
	if (token === null) {
		alert ("You must be logged in to ask questions");
		return;
	}
	modeCheck = await checkMode(arxivID);
	if (modeCheck['hasFullText'] === false) {
		console.log("Using simple mode");
		endpoint = '/api/gpt/query/simple/' + arxivID;
	}
	else{
		console.log("Using advanced mode");
		endpoint = '/api/gpt/query/complex/' + arxivID;
	}
    var http = new XMLHttpRequest();
    http.open("POST", endpoint, true);
    http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	http.setRequestHeader("x-access-tokens", token);
	let query = document.getElementById(arxivID + '_queryBox').value;
	// let fullQuery = ''
	// if (qamap.has(arxivID)) {
	// 	let fullState = qamap.get(arxivID);
	// 	for (let i = 0; i < fullState.length; i++) {
	// 		fullQuery += 'Question #' + i+1 + ': ' + fullState[i][0] + ', Answer #' + i+1 + ': ' + fullState[i][1] + '\n';
	// 	}
	// }
	// fullQuery += 'Current Question: ' + query;
    var params = "query=" + query; 
    http.send(params);
	// Show the spinner
	waitSpinner = document.getElementById(arxivID + '_waitSpinner');
	submitQueryButton = document.getElementById(arxivID + '_submitButton');
	waitSpinner.style.display = 'block';
	submitQueryButton.classList.add('disabled');

	let chat = document.getElementById(arxivID + '_chat');
	let userMessage = document.createElement('p');
	userMessage.classList.add('user');

	userMessage.innerHTML = '<i class="fa fa-user" aria-hidden="true"></i>  ' + query;
	chat.appendChild(userMessage);
	document.getElementById(arxivID + '_queryBox').value = '';

    http.onload = function() {
		let responseOBJ = JSON.parse(http.responseText);
		let responseMessage = document.createElement('p');
		responseMessage.classList.add('chatElement');
		responseMessage.innerHTML = '<i class="fa fa-server" aria-hidden="true"></i>  ' + responseOBJ['answer'];
		responseMessage.classList.add('bot');
		chat.appendChild(responseMessage);
		let currentState = [[query, responseOBJ['answer']]];
		if (qamap.has(arxivID)) {
			let fullState = qamap.get(arxivID).push(currentState);
		}
		else {
			qamap.set(arxivID, currentState);
		}
		waitSpinner.style.display = 'none';
		submitQueryButton.classList.remove('disabled');


    }


}

	

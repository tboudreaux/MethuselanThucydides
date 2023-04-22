
async function format_stored_chat_log() {
	if (await logged_in() === true){
		console.log("Calling format_stored_chat_log full");
		let userQueries = await get_user_all_queries();
		for (var arxiv_id in userQueries['queries']) {
			let chatID = arxiv_id + '_chat';
			queries = userQueries['queries'][arxiv_id];
			let chat = document.getElementById(chatID);
			if (chat != null) {
				console.log("Formatting stored chat log for " + arxiv_id);
				format_single_paper_chat_log(chat, queries);
			}
		}
	} else {
		console.log("Clearning all chat logs");
		let allChats = document.getElementsByClassName('chat');
		if (allChats != null) {
			for (let i = 0; i < allChats.length; i++) {
				allChats[i].innerHTML = "";
			}
		}
	}
}

function format_single_paper_chat_log(chat, queries) {
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
    var params = "query=" + query; 
    http.send(params);
	// Show the spinner
	waitSpinner = document.getElementById(arxivID + '_spinner');
	waitSpinner.style.display = 'block';
	askIcon = document.getElementById(arxivID + '_ask_icon');
	askIcon.style.display = 'none';

	submitQueryButton = document.getElementById(arxivID + '_submitButton');
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
		askIcon.style.display = 'block';
		submitQueryButton.classList.remove('disabled');


    }


}

	

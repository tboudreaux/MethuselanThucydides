
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
	if (! await logged_in()) {
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

	var responseTemplate = document.getElementById('response-template').content.cloneNode(true);
	console.log(responseTemplate);
	var responseDiv = responseTemplate.getElementById('responseMessage');
	console.log(responseDiv);
	var GPTResponseBTN = responseDiv.querySelector('.GPTResponseBTN');
	var paperTextBTN = responseDiv.querySelector('.paperTextBTN');

	GPTResponseBTN.setAttribute('data-mdb-target', '#' + arxivID + '_GPTResponseTXT');
	paperTextBTN.setAttribute('data-mdb-target', '#' + arxivID + '_paperTextTXT');

	var GPTResponseTextContainer = responseDiv.querySelector('.GPTResponseTXT');
	var paperTextContainer = responseDiv.querySelector('.paperTextTXT');

	GPTResponseTextContainer.setAttribute('id', arxivID + '_GPTResponseTXT');
	paperTextContainer.setAttribute('id', arxivID + '_paperTextTXT');

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
	
		let sourceData = document.createElement('div');
		sourceData.classList.add('sourceData');
		let chunkList = document.createElement('ul');
		chunkList.classList.add('chunkList');
		for (let i = 0; i < responseOBJ['chunks'].length; i++) {
			let chunk = document.createElement('li');
			chunk.classList.add('chunk');
			chunk.innerHTML = responseOBJ['chunks'][i];
			chunkList.appendChild(chunk);
		}
		sourceData.appendChild(chunkList);

		GPTResponseTextContainer.appendChild(responseMessage);
		paperTextContainer.appendChild(sourceData);
		chat.appendChild(responseDiv);

		// chat.appendChild(responseMessage);
		// let currentState = [[query, responseOBJ['answer']]];
		waitSpinner.style.display = 'none';
		askIcon.style.display = 'block';
		submitQueryButton.classList.remove('disabled');
    }


}

	

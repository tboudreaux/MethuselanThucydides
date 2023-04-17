async function getPaperList(category) {
	let response = await fetch('/api/papers/date/category/latest/' + category);
	let data = await response.json();
	return data;
}
async function getCategories() {
	let response = await fetch('/api/categories');
	let data = await response.json();
	return data;
}
async function getSummary(paper_id) {
	let response = await fetch('/api/summarize/' + paper_id);
	let data = await response.json();
	return data;
}

async function activateAdvancedMode(arxivID) {
	let advancedModeBtn = document.getElementById(arxivID + '_advancedMode');
	advancedModeBtn.classList.add('disabled');
	let response = await fetch('/api/fetch/ID/' + arxivID + '/long');
	let data = await response.json();

	advancedModeBtn.innerHTML = 'Full Text Mode!';
	advancedModeBtn.classList.add('fullTextMode')
	return data
}

async function checkMode(arxivID) {
	let response = await fetch('/api/fetch/ID/' + arxivID + '/hasFullText');
	let data = await response.json();
	return data;
}


async function format_paper(paper) {
	let paper_div = document.createElement('div');
	paper_div.classList.add('paper');
	paper_div.id = paper.arxiv_id;

	let paper_div_header = document.createElement('div');
	paper_div_header.classList.add('paper_header');
	paper_div.appendChild(paper_div_header);

	let waitSpinner = document.createElement('div');
	waitSpinner.classList.add('spinner');
	waitSpinner.id = paper.arxiv_id + '_waitSpinner';
	paper_div_header.appendChild(waitSpinner);
	waitSpinner.style.display = 'none';

	let advancedMode = document.createElement('button');
	advancedMode.id = paper.arxiv_id + '_advancedMode';
	advancedMode.classList.add('advancedMode-btn');

	mode = await checkMode(paper.arxiv_id);
	if (mode['hasFullText'] === true) {
		advancedMode.innerHTML = 'Full Text Mode!';
		advancedMode.classList.add('disabled');
		advancedMode.classList.add('fullTextMode')
	}
	else {
		advancedMode.innerHTML = 'Fetch Full Text';
		advancedMode.classList.add('fetchMode-btn');
	}
	// advancedMode.addEventListener('click', async function() {await activateAdvancedMode(paper.arxiv_id)});
	advancedMode.addEventListener('click', async () => {
		console.log("Activating advanced mode for " + paper.arxiv_id);
		await activateAdvancedMode(paper.arxiv_id);
		console.log("Advanced mode activated for " + paper.arxiv_id);
	});
	paper_div_header.appendChild(advancedMode);

	let title = document.createElement('h3');
	title.classList.add('ptitle');
	let title_link = document.createElement('a');
	title_link.href = paper.url;
	title_link.innerHTML = paper.title;
	title.appendChild(title_link);
	paper_div.appendChild(title);
	
	let author_list = document.createElement('h4');
	author_list.classList.add('author_list');
	author_list.innerHTML = paper.author_list;
	paper_div.appendChild(author_list);

	let hr = document.createElement('hr');
	paper_div.appendChild(hr);

	let summary = document.createElement('p');
	summary.classList.add('psummary');

	let summary_text = await getSummary(paper.arxiv_id);
	summary.innerHTML = summary_text['summary'];
	paper_div.appendChild(summary);

	let chatBox = document.createElement('div');
	chatBox.id = paper.arxiv_id + '_chatBox';
	chatBox.classList.add('chatBox');

	let chat = document.createElement('div');
	chat.id = paper.arxiv_id + '_chat';
	chat.classList.add('chat');
	chatBox.appendChild(chat);

	let inputLine = document.createElement('div');
	inputLine.id = paper.arxiv_id + '_inputLine';
	inputLine.classList.add('inputLine');

	let queryBoxWrapper = document.createElement('div');
	queryBoxWrapper.classList.add('queryBoxWrapper');
	inputLine.appendChild(queryBoxWrapper);

	let queryBox = document.createElement('input');
	queryBox.type = 'text';
	queryBox.id = paper.arxiv_id + '_queryBox';
	queryBox.placeholder = 'Ask a question about this paper';
	queryBox.classList.add('queryBox');
	queryBoxWrapper.appendChild(queryBox);



	chatBox.appendChild(inputLine);

	let submitButton = document.createElement('button');
	submitButton.type = 'submit';
	submitButton.value = 'Ask';
	submitButton.id = paper.arxiv_id + '_submitButton';
	submitButton.classList.add('submitChatButton');
	submitButton.onclick = await function() {submitQuery(paper.arxiv_id)};
	inputLine.appendChild(submitButton);

	let icon = document.createElement('i');
	icon.classList.add('fa');
	icon.classList.add('fa-paper-plane');
	submitButton.appendChild(icon);

	paper_div.appendChild(chatBox);



	return paper_div;
}


async function displayPapers(category, container) {
  const paperList = await getPaperList(category);

  for (const paper of paperList['papers']) {
    const formattedPaper = await format_paper(paper);
    container.appendChild(formattedPaper);

	let lineBreak = document.createElement('br');
	container.appendChild(lineBreak)
  }
}

async function formatTab(category){
	let container = document.getElementById("paperList");
	let tab = document.createElement('div');
	tab.id = category;
	tab.classList.add('tabcontent');
	tab.id = category + '-list';
	container.appendChild(tab);

	await displayPapers(category, tab);
}

async function formatAllTabs(){
	let categories = await getCategories();
	for (const category of categories['categories']){
		formatTab(category);
	}
}



async function submitQuery(arxivID) {
	modeCheck = await checkMode(arxivID);
	console.log(modeCheck);
	if (modeCheck['hasFullText'] === false) {
		console.log("Using simple mode");
		endpoint = '/api/query/simple/' + arxivID;
	}
	else{
		console.log("Using advanced mode");
		endpoint = '/api/query/complex/' + arxivID;
	}
	console.log(endpoint);
    var http = new XMLHttpRequest();
    http.open("POST", endpoint, true);
    http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	let query = document.getElementById(arxivID + '_queryBox').value;
	let fullQuery = ''
	if (qamap.has(arxivID)) {
		let fullState = qamap.get(arxivID);
		for (let i = 0; i < fullState.length; i++) {
			fullQuery += 'Question #' + i+1 + ': ' + fullState[i][0] + ', Answer #' + i+1 + ': ' + fullState[i][1] + '\n';
		}
	}
	fullQuery += 'Current Question: ' + query;
    var params = "query=" + fullQuery; 
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

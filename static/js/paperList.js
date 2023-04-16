async function getPaperList(category) {
	let response = await fetch('/api/papers/category/' + category);
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


async function format_paper(paper) {
	console.log(paper);
	let paper_div = document.createElement('div');
	paper_div.classList.add('paper');
	paper_div.id = paper.arxiv_id;

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

	// let advancedMode = document.createElement('input');
	// advancedMode.type = 'checkbox';
	// advancedMode.id = paper.arxiv_id + '_advancedMode';
	// advancedMode.classList.add('advancedMode');
	// inputLine.appendChild(advancedMode);

	let queryBox = document.createElement('input');
	queryBox.type = 'text';
	queryBox.id = paper.arxiv_id + '_queryBox';
	queryBox.placeholder = 'Ask a question about this paper';
	inputLine.appendChild(queryBox);

	let waitSpinner = document.createElement('div');
	waitSpinner.classList.add('spinner');
	waitSpinner.id = paper.arxiv_id + '_waitSpinner';
	inputLine.appendChild(waitSpinner);
	waitSpinner.style.display = 'none';


	chatBox.appendChild(inputLine);

	let submitButton = document.createElement('button');
	submitButton.type = 'submit';
	submitButton.value = 'Ask';
	submitButton.id = paper.arxiv_id + '_submitButton';
	submitButton.onclick = function() {submitQuery(paper.arxiv_id)};
	inputLine.appendChild(submitButton);

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
	container.appendChild(tab);

	await displayPapers(category, tab);
}

async function formatAllTabs(){
	let categories = await getCategories();
	for (const category of categories['categories']){
		formatTab(category);
	}
}



function submitQuery(arxivID) {
	// let advancedMode = document.getElementById(arxivID + '_advancedMode').checked;
	// console.log(advancedMode)
	var endpoint = '/api/query/simple/' + arxivID;
	// if (advancedMode === true) {
	// 	console.log("Using advanced mode")
	// 	endpoint = '/api/query/complex/' + arxivID;
	// }
	// else {
	// 	console.log("Using simple mode")
	// 	endpoint = '/api/query/simple/' + arxivID;
	// }
	console.log(endpoint)
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
	waitSpinner.style.display = 'block';
    // $('#' + arxivID + '_waitSpinner').show();
	$('#' + arxivID + '_queryBox').prop('disabled', true);
	$('#' + arxivID + '_submitButton').prop('disabled', true);

	let chat = document.getElementById(arxivID + '_chat');
	let queryMessage = document.createElement('p');
	queryMessage.classList.add('chatElement');

	queryMessage.innerHTML = '[User]: ' + query;
	chat.appendChild(queryMessage);
	document.getElementById(arxivID + '_queryBox').value = '';

    http.onload = function() {
		let responseOBJ = JSON.parse(http.responseText);
		let responseMessage = document.createElement('p');
		responseMessage.classList.add('chatElement');
		responseMessage.innerHTML = '[GPT]: ' + responseOBJ['answer'];
		chat.appendChild(responseMessage);
		let currentState = [[query, responseOBJ['answer']]];
		if (qamap.has(arxivID)) {
			let fullState = qamap.get(arxivID).push(currentState);
		}
		else {
			qamap.set(arxivID, currentState);
		}
		waitSpinner.style.display = 'none';
		$('#' + arxivID + '_queryBox').prop('disabled', false);
		$('#' + arxivID + '_submitButton').prop('disabled', false);


    }


}


async function getPaperList(category) {
	let response = await fetch('/api/papers/date/category/latest/' + category);
	let data = await response.json();
	return data;
}
async function getCategories() {
	let response = await fetch('/api/utils/categories');
	let data = await response.json();
	return data;
}
async function getSummary(paper_id) {
	let response = await fetch('/api/gpt/summarize/' + paper_id);
	let data = await response.json();
	return data;
}

async function getPaperAuthors(paper_id) {
	let response = await fetch('/api/authors/paper/' + paper_id);
	let data = await response.json();
	return data;
}

async function formatAuthorList(paper_id){
	let authors = await getPaperAuthors(paper_id);
	let fullAuthorNames = [];
	for (let i = 0; i < authors.length; i++) {
		fullAuthorNames.push(authors[i].fullname.join(' '));
	}
	return fullAuthorNames.join(', ');
}

async function formatSingleCatButton(key, name) {
	let navItem = document.createElement('li');
	navItem.classList.add('nav-item');
	navItem.id = "navItem_" + key;

	let button = document.createElement('button');
	button.classList.add('categoryButton');
	button.classList.add('px-0');
	button.classList.add('align-middle');
	button.id = "categoryButton_" + key;
	
	button.addEventListener('click', function(event) { openCat(event, key); });

	let icon = document.createElement('tt');
	icon.innerHTML = " " + key.split('.')[1];
	icon.classList.add('circleIcon');

	let navNameContainer = document.createElement('span');
	navNameContainer.innerHTML = key;
	navNameContainer.classList.add('ms-1');
	navNameContainer.classList.add('d-none');
	navNameContainer.classList.add('d-sm-inline');


	button.appendChild(icon);
	button.appendChild(navNameContainer);
	navItem.appendChild(button);

	return navItem;
}

async function formatCategoryButtonList() {
	console.log(paths);
	let categories = await getCategories();
	categoryMenu = document.getElementById('cat-menu');
	console.log(categoryMenu);
	for (var key in categories['categories']) {
		if (categories['categories'].hasOwnProperty(key)) {
			console.log(key + " -> " + categories['categories'][key]);
			navItem = await formatSingleCatButton(key, categories['categories'][key]);
			console.log("NAVITEM: " + navItem);
			categoryMenu.appendChild(navItem);
		}
	}
}

async function activateAdvancedMode(arxivID) {
	let advancedModeBtn = document.getElementById(arxivID + '_advancedMode');
	advancedModeBtn.classList.add('disabled');
	advancedModeBtn.innerHTML = 'Fetching...';

	token = localStorage.getItem('token');

	if (token == null) {
		alert ('Please login to view full text!');
		advancedModeBtn.innerHTML = 'Fetch Full Text';
		advancedModeBtn.classList.remove('disabled');
		return;
	}
	let response = await fetch('/api/fetch/ID/' + arxivID + '/long', {
		method: 'GET',
		headers: {
			'x-access-tokens': token,
		},
	});
	let data = await response.json();

	advancedModeBtn.innerHTML = 'Full Text Mode!';
	advancedModeBtn.classList.add('fullTextMode')
	return data
}

async function checkMode(arxivID) {
	let response = await fetch('/api/utils/hasFullText/' + arxivID);
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
	author_list.innerHTML = await formatAuthorList(paper.arxiv_id);
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
	tab.style.display = 'none';
	container.appendChild(tab);

	await displayPapers(category, tab);
}

async function formatAllTabs(){
	let categories = await getCategories();
	for (var key in categories['categories']){
		if (categories['categories'].hasOwnProperty(key)){
			formatTab(key);
		}
	}
}




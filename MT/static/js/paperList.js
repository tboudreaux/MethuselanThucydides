async function formatAuthorList(paper_id){
/**
 * Formates the author list for a paper.
 *
 * @param {string} paper_id - The arxiv id of the paper.
 *
 * @return {string} - A string of the author names.
 */
	let authors = await getPaperAuthors(paper_id);
	let fullAuthorNames = [];
	for (let i = 0; i < authors.authors.length; i++) {
		fullAuthorNames.push(authors.authors[i].fullname);
	}
	return fullAuthorNames.join(', ');
}

async function format_paper_new(paper, userQueries){
	let paper_template = document.getElementById('paper-template');
	let paper_div_container = await paper_template.content.cloneNode(true).querySelector('.paper-container');
	let paper_div = paper_div_container.querySelector('.paper');

	paper_div.id = paper.arxiv_id;

	let paperHeader = paper_div.getElementsByClassName('paper-header')[0];
	let bookmark = paperHeader.getElementsByClassName('bookmark')[0];
	bookmark.id = paper.arxiv_id + '_bookmark';

	let advancedModeBtn = paperHeader.getElementsByClassName('advancedMode-btn')[0];
	advancedModeBtn.id = paper.arxiv_id + '_advancedMode';

	advancedModeBtn.addEventListener('click', async () => {
		await activateAdvancedMode(paper.arxiv_id);
	});

	mode = await checkMode(paper.arxiv_id);
	if (mode['hasFullText']) {
		advancedModeBtn.innerHTML = 'Full Text Mode!';
		advancedModeBtn.classList.add('fullTextMode')
		advancedModeBtn.classList.add('disabled');
	} else {
		advancedModeBtn.innerHTML = 'Fetch Full Text';
		advancedModeBtn.classList.remove('fullTextMode')
	}

	let paperTitle = paper_div.getElementsByClassName('paper-title')[0];
	let pTitle = paperTitle.getElementsByClassName('ptitle')[0];
	let pTitleLink = pTitle.getElementsByTagName('a')[0];
	pTitleLink.href = paper.url;
	pTitleLink.innerHTML = paper.title;

	let pAuthors = paperTitle.getElementsByClassName('pauthors')[0];
	pAuthors.innerHTML = await formatAuthorList(paper.arxiv_id);

	let paperBody = paper_div.getElementsByClassName('paper-body')[0];
	let pSummary = paperBody.getElementsByClassName('psummary')[0];
	summaryText = await getSummary(paper.arxiv_id);

	if (summaryText == null) {
		pSummary.innerHTML = 'No summary available';
	} else {
		pSummary.innerHTML = summaryText['summary'];
	}

	let chatBox = paper_div.getElementsByClassName('chatBox')[0];
	chatBox.id = paper.arxiv_id + '_chatBox';

	let chat = paper_div.getElementsByClassName('chat')[0];
	chat.id = paper.arxiv_id + '_chat';
	if (userQueries.auth != false) {
		if (paper.arxiv_id in userQueries['queries']) {
			await format_single_paper_chat_log(chat, userQueries['queries'][paper.arxiv_id]);
		}
	}

	let inputLine = paper_div.getElementsByClassName('inputLine')[0];
	inputLine.id = paper.arxiv_id + '_inputLine';

	let queryBoxWrapper = paper_div.getElementsByClassName('queryBoxWrapper')[0];
	let queryBox = queryBoxWrapper.getElementsByClassName('queryBox')[0];
	queryBox.id = paper.arxiv_id + '_queryBox';

	let submitButton = inputLine.getElementsByClassName('submitChatButton')[0];
	submitButton.onclick = await function() {submitQuery(paper.arxiv_id)};

	let planeIcon = submitButton.getElementsByClassName('fa')[0];
	planeIcon.id = paper.arxiv_id + '_ask_icon';

	let spinner = inputLine.getElementsByClassName('spinner-grow')[0];
	spinner.id = paper.arxiv_id + '_spinner';

	return paper_div_container;
}


// async function displayPapers(category, container, userQueries) {
//   const paperList = await getPaperList(category);
//
//   for (const paper of paperList['papers']) {
//     const formattedPaper = await format_paper_new(paper, userQueries);
//     container.appendChild(formattedPaper);
//
// 	let lineBreak = document.createElement('br');
// 	container.appendChild(lineBreak)
//   }
// }
//
// async function formatTab(category, userQueries){
// 	let container = document.getElementById("paperList");
// 	let tab = document.createElement('div');
// 	tab.id = category;
// 	tab.classList.add('tabcontent');
// 	tab.id = category + '-list';
// 	tab.style.display = 'none';
//
// 	container.appendChild(tab);
//
// 	await displayPapers(category, tab, userQueries);
// }
//
// async function formatAllTabs(){
// 	var categories = await getCategories();
// 	console.log(userQueries);
// 	for (var key in categories['categories']){
// 		if (categories['categories'].hasOwnProperty(key)){
// 			formatTab(key, userQueries);
// 		}
// 	}
// }




async function resolve_category(category){
	let response = await fetch('/api/arxiv/resolve/category/' + category);
	let json = await response.json();
	return json;
}

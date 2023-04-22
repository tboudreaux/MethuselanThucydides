async function style_for_current_user(){
	await loadStateInfo();
	formatUserButton();
	format_stored_chat_log();
	format_all_bookmarks();
}

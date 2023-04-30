async function style_for_current_user(){
	formatUserButton();
	format_user_profile_settings();
	await loadStateInfo();
	format_stored_chat_log();
	format_all_bookmarks();
}

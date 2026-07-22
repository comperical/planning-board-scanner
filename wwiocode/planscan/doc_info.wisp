<html>
<head>
<title>DocInfo</title>

<!-- standard wisp include tag -->
<wisp/>

<script>

const MAIN_TABLE = 'doc_info';

let EDIT_STUDY_ITEM = -1;


function getStudyItem() {
	U.massert(EDIT_STUDY_ITEM != -1, "No study item has been selected");
	return W.lookupItem(MAIN_TABLE, EDIT_STUDY_ITEM);
}


// Auto-generated create new function
function createNew() {

	const newrec = {
		doc_link : '',
		location : '',
		extracted_text : '',
		file_name : '',
		day_code : ''
	};
	const newitem = W.buildItem(MAIN_TABLE, newrec);
	newitem.syncItem();
	redisplay();
}


// Auto-generated redisplay function
function editStudyItem(itemid) {
	EDIT_STUDY_ITEM = itemid;
	redisplay();
}

function back2Main() {
	EDIT_STUDY_ITEM = -1;
	redisplay();
}

function shorten4Display(ob) {
	const s = '' + ob;
	if(s.length < 40) { return s; }
	return s.substring(0, 37) + '...';
}
function deleteItem(itemid) {
	if(confirm('Are you sure you want to delete this item?')) {
		const item = W.lookupItem(MAIN_TABLE, itemid);
		item.deleteItem();
		redisplay();
	}
}

// Auto-generated redisplay function
function redisplay() {
	const pageinfo = EDIT_STUDY_ITEM == -1 ? getMainPageInfo() : getEditPageInfo();
	U.populateSpanData({"page_info" : pageinfo });
}

// Auto-generated getEditPageInfo function
function getEditPageInfo() {

	const item = W.lookupItem(MAIN_TABLE, EDIT_STUDY_ITEM);
	var pageinfo = `
	<h4>Edit Item</h4>
	<table class="basic-table" width="50%">
	<tr>
	<td>Back</td>
	<td></td>
	<td><a href="javascript:back2Main()"><img src="/u/shared/image/leftarrow.png" height="18"/></a></td>
	</tr>
	<tr><td>DocLink</td>
	<td>${item.getDocLink()}</td>
	<td><a href="javascript:U.genericEditTextField(MAIN_TABLE, 'doc_link', EDIT_STUDY_ITEM)"><img src="/u/shared/image/edit.png" height="18"></a></td>
	</tr>
	<tr><td>Location</td>
	<td>${item.getLocation()}</td>
	<td><a href="javascript:U.genericEditTextField(MAIN_TABLE, 'location', EDIT_STUDY_ITEM)"><img src="/u/shared/image/edit.png" height="18"></a></td>
	</tr>
	<tr><td>ExtractedText</td>
	<td>${item.getExtractedText()}</td>
	<td><a href="javascript:U.genericEditTextField(MAIN_TABLE, 'extracted_text', EDIT_STUDY_ITEM)"><img src="/u/shared/image/edit.png" height="18"></a></td>
	</tr>
	<tr><td>FileName</td>
	<td>${item.getFileName()}</td>
	<td><a href="javascript:U.genericEditTextField(MAIN_TABLE, 'file_name', EDIT_STUDY_ITEM)"><img src="/u/shared/image/edit.png" height="18"></a></td>
	</tr>
	<tr><td>DayCode</td>
	<td>${item.getDayCode()}</td>
	<td><a href="javascript:U.genericEditTextField(MAIN_TABLE, 'day_code', EDIT_STUDY_ITEM)"><img src="/u/shared/image/edit.png" height="18"></a></td>
	</tr>
	</table>
	`;
	return pageinfo;

}


// Auto-generated getMainPageInfo function
function getMainPageInfo() {

	var pageinfo = `<h3>Main Listing</h3>
		<table class="basic-table" width="80%">
		<tr>
		<th>doc_link</th>
		<th>location</th>
		<th>extracted_text</th>
		<th>file_name</th>
		<th>day_code</th>
		<th>..</th></tr>
	`;

	const itemlist = W.getItemList(MAIN_TABLE);

	itemlist.forEach(function(item) {
		const rowstr = `
			<tr>
			<td>${shorten4Display(item.getDocLink())}</td>
			<td>${shorten4Display(item.getLocation())}</td>
			<td>${shorten4Display(item.getExtractedText())}</td>
			<td>${shorten4Display(item.getFileName())}</td>
			<td>${shorten4Display(item.getDayCode())}</td>
			<td>
			<a href="javascript:editStudyItem(${item.getId()})"><img src="/u/shared/image/inspect.png" height="16"/></a>
			&nbsp;&nbsp;&nbsp;
			<a href="javascript:deleteItem(${item.getId()})"><img src="/u/shared/image/remove.png" height="16"/></a>
			</td>
			</tr>
		`;
		pageinfo += rowstr;
	});

	pageinfo += `</table>`;
	pageinfo += `<br/><br/><a href="javascript:createNew()"><button>new</button></a>`;
	return pageinfo;
}

</script>
<body onLoad="javascript:redisplay()">
<center>
<div id="page_info"></div>

</center>
</body>
</html>

<html>
<head>
<title>PlanScan Documents</title>

<!-- standard wisp include tag -->
<wisp/>

<style>
.doc-page-text {
	font-family: monospace;
	white-space: pre-wrap;
	overflow-wrap: anywhere;
	text-align: left;
	background: #f5f5f5;
	border: 1px solid #ddd;
	padding: 8px;
	max-width: 70%;
	margin: 0 auto 1em auto;
}
</style>

<script>

const MAIN_TABLE = 'documents';

let EDIT_STUDY_ITEM = -1;


function getStudyItem() {
	U.massert(EDIT_STUDY_ITEM != -1, "No study item has been selected");
	return W.lookupItem(MAIN_TABLE, EDIT_STUDY_ITEM);
}

function getTownName(townid) {
	if(townid == null) { return "?"; }
	const town = W.lookupItem('town', townid);
	if(town == null) { return "?"; }
	return `${town.getName()}, ${town.getState()}`;
}

function getKeywordHitsForDoc(docid) {
	return W.getItemList('keyword_hits').filter(hit => hit.getDocumentId() == docid);
}

function getPagesForDoc(docid) {
	return W.getItemList('doc_pages')
		.filter(page => page.getDocumentId() == docid)
		.sort(U.proxySort(page => [page.getPageNumber()]));
}

function shorten4Display(ob) {
	const s = '' + ob;
	if(s.length < 50) { return s; }
	return s.substring(0, 47) + '...';
}

function formatSize(bytes) {
	if(bytes == null) { return "?"; }
	return Math.round(bytes / 1024) + " KB";
}

function editStudyItem(itemid) {
	EDIT_STUDY_ITEM = itemid;
	redisplay();
}

function back2Main() {
	EDIT_STUDY_ITEM = -1;
	redisplay();
}

// Auto-generated redisplay function
function redisplay() {
	const pageinfo = EDIT_STUDY_ITEM == -1 ? getMainPageInfo() : getEditPageInfo();
	U.populateSpanData({"page_info" : pageinfo });
}

// Detail view: full keyword-hit snippet list for one document
function getEditPageInfo() {

	const item = getStudyItem();
	const hitlist = getKeywordHitsForDoc(item.getId())
		.sort(U.proxySort(hit => [hit.getPageNumber()]));

	var pageinfo = `
	<h4>Document Detail</h4>
	<table class="basic-table" width="70%">
	<tr>
	<td>Back</td>
	<td></td>
	<td><a href="javascript:back2Main()"><img src="/u/shared/image/leftarrow.png" height="18"/></a></td>
	</tr>
	<tr><td>Town</td><td colspan="2">${getTownName(item.getTownId())}</td></tr>
	<tr><td>File</td><td colspan="2">${item.getFilePath()}</td></tr>
	<tr><td>Date</td><td colspan="2">${item.getDocDate() || "?"}</td></tr>
	<tr><td>Pages</td><td colspan="2">${item.getPageCount() || "?"}</td></tr>
	<tr><td>Size</td><td colspan="2">${formatSize(item.getFileSizeBytes())}</td></tr>
	<tr><td>Source</td><td colspan="2">
		${item.getSourceUrl() ? `<a href="${item.getSourceUrl()}" target="_blank">${shorten4Display(item.getSourceUrl())}</a>` : "?"}
	</td></tr>
	</table>

	<br/>

	<h4>Keyword Hits (${hitlist.length})</h4>
	<table class="basic-table" width="90%">
	<tr>
	<th width="8%">Page</th>
	<th width="15%">Keyword</th>
	<th width="7%">Count</th>
	<th>Snippet</th>
	</tr>
	`;

	hitlist.forEach(function(hit) {
		pageinfo += `
		<tr>
		<td>${hit.getPageNumber()}</td>
		<td>${hit.getKeyword()}</td>
		<td>${hit.getCount()}</td>
		<td class="left-align">${hit.getSnippet() || ""}</td>
		</tr>
		`;
	});

	pageinfo += `</table>`;

	pageinfo += `<br/><h4>Extracted Text</h4>`;

	const pagelist = getPagesForDoc(item.getId());
	if(pagelist.length == 0) {
		pageinfo += `<i>No text recorded for this document.</i>`;
	} else {
		pagelist.forEach(function(page) {
			pageinfo += `
			<h5>Page ${page.getPageNumber()}</h5>
			<pre class="doc-page-text">${escapeHtml(page.getPageText() || "")}</pre>
			`;
		});
	}

	return pageinfo;
}

function escapeHtml(rawtext) {
	const div = document.createElement("div");
	div.textContent = rawtext;
	return div.innerHTML;
}

// Main listing: one row per scanned document
function getMainPageInfo() {

	var pageinfo = `<h3>PlanScan Documents</h3>
		<table class="basic-table" width="95%">
		<tr>
		<th>Town</th>
		<th>Date</th>
		<th>File</th>
		<th>Pages</th>
		<th>Size</th>
		<th>Keyword Hits</th>
		<th>..</th></tr>
	`;

	const itemlist = W.getItemList(MAIN_TABLE)
		.sort(U.proxySort(item => [item.getDocDate() || ""]))
		.reverse();

	itemlist.forEach(function(item) {

		const hitcount = getKeywordHitsForDoc(item.getId()).length;

		const rowstr = `
			<tr>
			<td>${getTownName(item.getTownId())}</td>
			<td>${item.getDocDate() || "?"}</td>
			<td>${shorten4Display(item.getFilePath())}</td>
			<td>${item.getPageCount() || "?"}</td>
			<td>${formatSize(item.getFileSizeBytes())}</td>
			<td>${hitcount}</td>
			<td>
			<a href="javascript:editStudyItem(${item.getId()})"><img src="/u/shared/image/inspect.png" height="16"/></a>
			</td>
			</tr>
		`;
		pageinfo += rowstr;
	});

	pageinfo += `</table>`;
	return pageinfo;
}

</script>
<body onLoad="javascript:redisplay()">
<center>
<div id="page_info"></div>

</center>
</body>
</html>

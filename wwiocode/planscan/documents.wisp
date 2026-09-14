<html>
<head>
<title>PlanScan Documents</title>

<!-- standard wisp include tag -->
<wisp/>

<script src="/u/shared/optjs/SimpleModal/v1.js"></script>

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

/* Modal - see /opt/userdata/external/widgetprivate/nuhminc/MyStandardModal.css */
.modal-top {
	position: fixed;
	z-index: 1000;
	left: 0;
	top: 0;
	width: 100%;
	height: 100%;
	background-color: rgba(0, 0, 0, 0.5);
	border-radius: 5px;

	display: flex;
	justify-content: center;
	align-items: center;
	flex-direction: column;
}

.modal-title {
	background-color: white;
	padding: 15px 20px;
	font-weight: bold;
	font-size: 18px;
	width: 800px;
	max-width: 90vw;

	display: flex;
	justify-content: space-between;
	align-items: center;
}

.modal-title button {
	background: none;
	border: none;
	font-size: 16px;
	cursor: pointer;
}

.modal-content {
	background-color: white;
	padding: 20px;
	width: 800px;
	max-width: 90vw;
	max-height: 70vh;
	overflow-y: auto;
	text-align: left;
}

.project-row {
	cursor: pointer;
}
</style>

<script>

const MAIN_TABLE = 'documents';

let EDIT_STUDY_ITEM = -1;

let SELECTED_PROJECT_ID = -1;

const TOWN_SEL_KEY = "TownSelKey";

GENERIC_OPT_SELECT_MAP.set(TOWN_SEL_KEY, -1);


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

function getTownNameMap() {
	return PSUTIL.buildGenericMap(W.getItemList('town'),
		town => town.getId(), town => `${town.getName()}, ${town.getState()}`);
}

function getSelectedTownId() {
	return parseInt(GENERIC_OPT_SELECT_MAP.get(TOWN_SEL_KEY));
}

function getPagesForDoc(docid) {
	return W.getItemList('doc_pages')
		.filter(page => page.getDocumentId() == docid)
		.sort(U.proxySort(page => [page.getPageNumber()]));
}

function getProjectsForDoc(docid) {
	const links = W.getItemList('project_documents').filter(link => link.getDocumentId() == docid);
	return links
		.map(link => W.lookupItem('projects', link.getProjectId()))
		.filter(project => project != null);
}

// Same as getProjectsForDoc, but keeps the project_documents link (for its page_number)
function getProjectLinksForDoc(docid) {
	return W.getItemList('project_documents')
		.filter(link => link.getDocumentId() == docid)
		.map(link => ({ project : W.lookupItem('projects', link.getProjectId()), link : link }))
		.filter(entry => entry.project != null);
}

function shorten4Display(ob) {
	const s = '' + ob;
	if(s.length < 50) { return s; }
	return s.substring(0, 47) + '...';
}

// Most PDF viewers honor a #page=N fragment to jump straight to that page
function getPageLinkHtml(docitem, pagenumber) {
	if(pagenumber == null) { return "?"; }
	if(!docitem.getSourceUrl()) { return pagenumber; }

	return `<a href="${docitem.getSourceUrl()}#page=${pagenumber}" target="_blank"
				onclick="event.stopPropagation()">${pagenumber}</a>`;
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

function showProjectModal(projectid) {
	SELECTED_PROJECT_ID = projectid;
	redisplay();
}

function closeProjectModal() {
	SELECTED_PROJECT_ID = -1;
	redisplay();
}

// Builds the project-detail modal (empty string when nothing is selected)
function getProjectModalHtml() {

	if(SELECTED_PROJECT_ID == -1) { return ""; }

	const project = W.lookupItem('projects', SELECTED_PROJECT_ID);
	if(project == null) { return ""; }

	const content = `
		<div><b>Town</b> : ${getTownName(project.getTownId())}</div>
		<div><b>Short Desc</b> : ${project.getShortDesc() || ""}</div>
		<br/>
		<pre class="doc-page-text">${escapeHtml(project.getFullMdText() || "")}</pre>
	`;

	return MODAL.build()
				.setModalTitleHtml(`Project #${project.getId()}`)
				.setUseButton(true)
				.setButtonOnClick("javascript:closeProjectModal()")
				.setModalContentHtml(content)
				.getHtmlString();
}

// Auto-generated redisplay function
function redisplay() {
	const pageinfo = EDIT_STUDY_ITEM == -1 ? getMainPageInfo() : getEditPageInfo();
	U.populateSpanData({"page_info" : PSUTIL.getSimpleHeader() + pageinfo + getProjectModalHtml() });
}

// Detail view: document metadata, linked projects, and extracted text
function getEditPageInfo() {

	const item = getStudyItem();
	const projectlinklist = getProjectLinksForDoc(item.getId())
		.sort(U.proxySort(entry => [entry.project.getId()]));

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

	<h4>Projects (${projectlinklist.length})</h4>
	<table class="basic-table" width="70%">
	<tr>
	<th width="10%">ID</th>
	<th>Short Description</th>
	<th width="10%">Page</th>
	</tr>
	${projectlinklist.map(entry => `
	<tr class="project-row" onclick="javascript:showProjectModal(${entry.project.getId()})">
	<td>${entry.project.getId()}</td>
	<td class="left-align">${entry.project.getShortDesc() || ""}</td>
	<td>${getPageLinkHtml(item, entry.link.getPageNumber())}</td>
	</tr>
	`).join("")}
	</table>

	<br/>

	<h4>Extracted Text</h4>`;

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

function getUiControlTable() {

	const townmap = getTownNameMap();
	const townsel = buildOptSelector()
						.configureFromMap(townmap)
						.sortByDisplay()
						.insertStartingPair(-1, "---")
						.setElementName(TOWN_SEL_KEY)
						.setSelectedKey(getSelectedTownId())
						.useGenericUpdater()
						.getHtmlString();

	return `
		<table class="basic-table" width="40%">
		<tr>
		<td>Town</td>
		<td colspan="2">${townsel}</td>
		</tr>
		</table>
	`;
}

// Auto-generated getMainPageInfo function
function getMainPageInfo() {

	var pageinfo = `<h3>PlanScan Documents</h3>

		${getUiControlTable()}

		<br/>

		<table class="basic-table" width="95%">
		<tr>
		<th>Town</th>
		<th>Date</th>
		<th>File</th>
		<th>Pages</th>
		<th>Size</th>
		<th>#Projects</th>
		<th>..</th></tr>
	`;

	const towntrg = getSelectedTownId();

	const itemlist = W.getItemList(MAIN_TABLE)
		.filter(item => towntrg == -1 || item.getTownId() == towntrg)
		.sort(U.proxySort(item => [item.getDocDate() || ""]))
		.reverse();

	itemlist.forEach(function(item) {

		const projectcount = getProjectsForDoc(item.getId()).length;

		const rowstr = `
			<tr>
			<td>${getTownName(item.getTownId())}</td>
			<td>${item.getDocDate() || "?"}</td>
			<td>${shorten4Display(item.getFilePath())}</td>
			<td>${item.getPageCount() || "?"}</td>
			<td>${formatSize(item.getFileSizeBytes())}</td>
			<td>${projectcount}</td>
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

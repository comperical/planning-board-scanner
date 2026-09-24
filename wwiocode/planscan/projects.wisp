<html>
<head>
<title>PlanScan Projects</title>

<!-- standard wisp include tag -->
<wisp/>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css"> </link>

<!-- Markdown -> HTML for the project write-ups (full_md_text) -->
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>


<style>
.doc-page-text {
	font-family: monospace;
	white-space: pre-wrap;
	overflow-wrap: anywhere;
	text-align: left;
	background: #f5f5f5;
	border: 1px solid #ddd;
	padding: 8px;
	margin: 0 auto 1em auto;
}

.project-md {
	text-align: left;
	padding: 8px 16px;
}

/* Rendered project write-up on the edit page */
.project-md h1 { font-size: 20px; margin-top: 0; }
.project-md h2 { font-size: 17px; }
.project-md ul { padding-left: 20px; }
.project-md li { margin-bottom: 4px; }

</style>

<script>

const MAIN_TABLE = 'projects';

let EDIT_STUDY_ITEM = -1;

const TOWN_SEL_KEY = "TownSelKey";
const TAG_SEL_KEY = "TagSelKey";
const SORT_SEL_KEY = "SortSelKey";

GENERIC_OPT_SELECT_MAP.set(TOWN_SEL_KEY, -1);
GENERIC_OPT_SELECT_MAP.set(TAG_SEL_KEY, "any");
GENERIC_OPT_SELECT_MAP.set(SORT_SEL_KEY, "latest_doc");

const SORT_OPTION_MAP = new Map([
	["latest_doc", "Latest Document"],
	["newest", "Newest Project"],
	["town_name", "Town Name"],
	["num_docs", "#Documents"]
]);


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

// tag_set is a comma-separated set of tags (vocabulary: PROJECT_TAGS.md)
function getTagList(item) {
	return (item.getTagSet() || "").split(",").map(t => t.trim()).filter(t => t != "");
}

// Tag filter options: every tag in use, labeled with its project count
function getTagOptionMap() {

	const counts = new Map();
	W.getItemList(MAIN_TABLE).forEach(function(item) {
		getTagList(item).forEach(tag => counts.set(tag, (counts.get(tag) || 0) + 1));
	});

	const tagmap = new Map([["any", "---"], ["untagged", "(untagged)"]]);
	[...counts.keys()].sort().forEach(tag => tagmap.set(tag, `${tag} (${counts.get(tag)})`));
	return tagmap;
}

function matchesTagFilter(item, tagtrg) {
	if(tagtrg == "any") { return true; }
	const taglist = getTagList(item);
	if(tagtrg == "untagged") { return taglist.length == 0; }
	return taglist.includes(tagtrg);
}

// project id -> list of linked documents, built once per redisplay
// rather than scanning project_documents for every row
function getProjectDocMap() {

	const docmap = new Map();

	W.getItemList('project_documents').forEach(function(link) {
		const doc = W.lookupItem('documents', link.getDocumentId());
		if(doc == null) { return; }

		if(!docmap.has(link.getProjectId())) {
			docmap.set(link.getProjectId(), []);
		}
		docmap.get(link.getProjectId()).push(doc);
	});

	return docmap;
}

// Most recent doc_date among a project's linked documents, or "" if none known
function getLatestDocDate(doclist) {
	const datelist = doclist.map(doc => doc.getDocDate()).filter(d => d != null);
	if(datelist.length == 0) { return ""; }
	return datelist.sort().reverse()[0];
}

function getSortComparator(sortkey, docmap) {

	const doclistfor = item => docmap.get(item.getId()) || [];

	if(sortkey == "newest") {
		return U.proxySort(item => [-item.getId()]);
	}

	if(sortkey == "town_name") {
		return U.proxySort(item => [getTownName(item.getTownId()), -item.getId()]);
	}

	if(sortkey == "num_docs") {
		return U.proxySort(item => [-doclistfor(item).length, -item.getId()]);
	}

	// Default: latest_doc, most recent first; projects with no dated
	// documents sink to the bottom
	return U.proxySort(item => {
		const latest = getLatestDocDate(doclistfor(item));
		return [latest == "" ? 1 : 0, latest == "" ? 0 : -Date.parse(latest), -item.getId()];
	});
}

function getStudyItem() {
	U.massert(EDIT_STUDY_ITEM != -1, "No study item has been selected");
	return W.lookupItem(MAIN_TABLE, EDIT_STUDY_ITEM);
}

function editStudyItem(itemid) {
	EDIT_STUDY_ITEM = itemid;
	redisplay();
}

function back2Main() {
	EDIT_STUDY_ITEM = -1;
	redisplay();
}

// This project's project_documents links, each paired with its document,
// newest document first
function getDocLinksForProject(projectid) {
	return W.getItemList('project_documents')
		.filter(link => link.getProjectId() == projectid)
		.map(link => ({ doc : W.lookupItem('documents', link.getDocumentId()), link : link }))
		.filter(entry => entry.doc != null)
		.sort(U.proxySort(entry => [entry.doc.getDocDate() || ""]))
		.reverse();
}

// project id -> number of linked contacts, built once per redisplay
function getProjectContactCountMap() {
	const countmap = new Map();
	W.getItemList('contact_project').forEach(function(link) {
		countmap.set(link.getProjectId(), (countmap.get(link.getProjectId()) || 0) + 1);
	});
	return countmap;
}

// Contacts linked to this project via contact_project, sorted by company then name
function getContactsForProject(projectid) {
	return W.getItemList('contact_project')
		.filter(link => link.getProjectId() == projectid)
		.map(link => W.lookupItem('contact_info', link.getContactId()))
		.filter(contact => contact != null)
		.sort(U.proxySort(contact => [contact.getCompany() || contact.getName() || "", contact.getName() || ""]));
}

function shorten4Display(ob) {
	const s = '' + ob;
	if(s.length < 60) { return s; }
	return s.substring(0, 57) + '...';
}

// The document's source URL, or "" if it has none. A missing value can
// come back from the getter as the string "null", so only real http(s)
// URLs count - anything else would become a broken relative link.
function getRealSourceUrl(docitem) {
	const url = (docitem.getSourceUrl() || "") + "";
	return /^https?:\/\//i.test(url.trim()) ? url.trim() : "";
}

// Most PDF viewers honor a #page=N fragment to jump straight to that page
function getPageLinkHtml(docitem, pagenumber) {
	if(pagenumber == null) { return "?"; }
	const url = getRealSourceUrl(docitem);
	if(!url) { return pagenumber; }

	return `<a href="${url}#page=${pagenumber}" target="_blank">${pagenumber}</a>`;
}

function escapeHtml(rawtext) {
	const div = document.createElement("div");
	div.textContent = rawtext;
	return div.innerHTML;
}

// Falls back to escaped plain text if the marked CDN script didn't load
function renderMarkdown(mdtext) {
	if(typeof marked === "undefined") {
		return `<pre class="doc-page-text">${escapeHtml(mdtext)}</pre>`;
	}
	return marked.parse(mdtext);
}

// Copies the rendered description to the clipboard as rich HTML (pastes
// formatted into email/docs), with the HTML source as the plain-text
// flavor (pastes as markup into plain-text editors)
async function copyDescription() {
	const html = renderMarkdown(getStudyItem().getFullMdText() || "");
	await copyToClipboard(html, html, "Description copied to clipboard");
}

// Writes rich HTML plus a plain-text flavor to the clipboard; the paste
// target picks whichever it understands
async function copyToClipboard(html, plaintext, donemsg) {
	try {
		if(typeof ClipboardItem !== "undefined") {
			await navigator.clipboard.write([new ClipboardItem({
				"text/html" : new Blob([html], {type : "text/html"}),
				"text/plain" : new Blob([plaintext], {type : "text/plain"})
			})]);
		} else {
			await navigator.clipboard.writeText(plaintext);
		}
		alert(donemsg);
	}
	catch(err) {
		alert("Could not copy to clipboard: " + (err.message || err));
	}
}

// One contact as a single line: "Company - Name | phone | email | web"
function getContactLine(contact) {
	const who = [contact.getCompany(), contact.getName()].filter(x => x).join(" - ") || "(no name)";
	return [who, contact.getPhone(), contact.getEmail(), contact.getWebSite()].filter(x => x).join(" | ");
}

// Linked documents that have a source URL (the only ones worth linking),
// as {label, url} with a #page=N jump when the mention's page is known
function getSourceDocLinks(projectid) {
	return getDocLinksForProject(projectid)
		.filter(entry => getRealSourceUrl(entry.doc))
		.map(entry => ({
			label : `${entry.doc.getDocDate() || "?"} - ${entry.doc.getFilePath().split("/").pop()}`,
			url : getRealSourceUrl(entry.doc) + (entry.link.getPageNumber() != null ? `#page=${entry.link.getPageNumber()}` : "")
		}));
}

// The write-up's own headings are demoted so they sit under the per-project
// heading instead of competing with it
function getProjectCopyHtml(item) {

	const mdhtml = renderMarkdown(item.getFullMdText() || "")
		.replace(/<(\/?)h[1-3]>/g, "<$1h4>");
	const contacts = getContactsForProject(item.getId());
	const doclinks = getSourceDocLinks(item.getId());

	return `
		<h3>${escapeHtml(getTownName(item.getTownId()))}: ${escapeHtml(item.getShortDesc() || "(no short_desc)")}</h3>
		${mdhtml}
		${contacts.length == 0 ? "" : `
		<p><b>Contacts</b></p>
		<ul>${contacts.map(c => `<li>${escapeHtml(getContactLine(c))}</li>`).join("")}</ul>`}
		${doclinks.length == 0 ? "" : `
		<p><b>Source documents</b></p>
		<ul>${doclinks.map(d => `<li><a href="${escapeHtml(d.url)}">${escapeHtml(d.label)}</a></li>`).join("")}</ul>`}
	`;
}

function getProjectCopyText(item) {

	const contacts = getContactsForProject(item.getId());
	const doclinks = getSourceDocLinks(item.getId());

	const lines = [
		`${getTownName(item.getTownId())}: ${item.getShortDesc() || "(no short_desc)"}`,
		"",
		(item.getFullMdText() || "").trim()
	];
	if(contacts.length > 0) {
		lines.push("", "Contacts:", ...contacts.map(c => "  - " + getContactLine(c)));
	}
	if(doclinks.length > 0) {
		lines.push("", "Source documents:", ...doclinks.map(d => `  - ${d.label}: ${d.url}`));
	}
	return lines.join("\n");
}

// Copies every project in the current (filtered, sorted) main listing
async function copySelection() {

	const itemlist = getSelectedProjects();
	if(itemlist.length == 0) {
		alert("No projects in the current selection");
		return;
	}

	const html = itemlist.map(getProjectCopyHtml).join("<hr/>");
	const plaintext = itemlist.map(getProjectCopyText).join("\n\n" + "-".repeat(60) + "\n\n");
	await copyToClipboard(html, plaintext, `Copied ${itemlist.length} project(s) to clipboard`);
}

// Detail view: project fields, rendered write-up, and linked documents
function getEditPageInfo() {

	const item = getStudyItem();
	const doclinklist = getDocLinksForProject(item.getId());
	const latest = getLatestDocDate(doclinklist.map(entry => entry.doc));
	const contactlist = getContactsForProject(item.getId());

	var pageinfo = `
	<h4>Project Detail</h4>
	<table class="basic-table" width="70%">
	<tr>
	<td>Back</td>
	<td></td>
	<td><a href="javascript:back2Main()"><img src="/u/shared/image/leftarrow.png" height="18"/></a></td>
	</tr>
	<tr><td>ID</td><td>${item.getId()}</td><td></td></tr>
	<tr><td>Town</td><td>${getTownName(item.getTownId())}</td><td></td></tr>
	<tr><td>Short Desc</td>
	<td class="left-align">${item.getShortDesc() || "(no short_desc)"}</td>
	<td><a href="javascript:U.genericEditTextField(MAIN_TABLE, 'short_desc', EDIT_STUDY_ITEM)"><img src="/u/shared/image/edit.png" height="18"></a></td>
	</tr>
	<tr><td>#Docs</td><td>${doclinklist.length}</td><td></td></tr>
	<tr><td>Latest Doc</td><td>${latest || "?"}</td><td></td></tr>
	<tr><td>Tags</td><td class="left-align">${getTagList(item).join(", ") || "(untagged)"}</td><td></td></tr>
	</table>

	<br/>

	<table class="basic-table" width="70%">
	<tr><th>
	Description
	&nbsp;&nbsp;
	<a href="javascript:copyDescription()" title="Copy description (with HTML formatting)"><i class="fa-regular fa-copy"></i></a>
	</th></tr>
	<tr><td class="left-align project-md">${renderMarkdown(item.getFullMdText() || "")}</td></tr>
	</table>

	<br/>

	<h4>Contacts (${contactlist.length})</h4>
	${contactlist.length == 0 ? `<div>No contacts linked yet</div>` : `
	<table class="basic-table" width="70%">
	<tr>
	<th width="22%">Company</th>
	<th>Name</th>
	<th width="16%">Phone</th>
	<th width="24%">Email</th>
	<th width="24%">Web Site</th>
	</tr>
	${contactlist.map(contact => `
	<tr>
	<td class="left-align">${escapeHtml(contact.getCompany() || "")}</td>
	<td class="left-align">${escapeHtml(contact.getName() || "")}</td>
	<td>${PSUTIL.getPhoneHtml(contact.getPhone())}</td>
	<td class="left-align">${PSUTIL.getEmailHtml(contact.getEmail())}</td>
	<td class="left-align">${PSUTIL.getWebSiteHtml(contact.getWebSite())}</td>
	</tr>
	`).join("")}
	</table>
	`}

	<br/>

	<h4>Documents (${doclinklist.length})</h4>
	<table class="basic-table" width="70%">
	<tr>
	<th width="12%">Date</th>
	<th>File</th>
	<th width="10%">Page</th>
	</tr>
	${doclinklist.map(entry => `
	<tr>
	<td>${entry.doc.getDocDate() || "?"}</td>
	<td class="left-align">${shorten4Display(entry.doc.getFilePath())}</td>
	<td>${getPageLinkHtml(entry.doc, entry.link.getPageNumber())}</td>
	</tr>
	`).join("")}
	</table>
	`;

	return pageinfo;
}

// Auto-generated redisplay function
function redisplay() {
	const pageinfo = EDIT_STUDY_ITEM == -1 ? getMainPageInfo() : getEditPageInfo();
	U.populateSpanData({"page_info" : PSUTIL.getSimpleHeader() + pageinfo });
}

function getUiControlTable() {

	const townsel = buildOptSelector()
						.configureFromMap(getTownNameMap())
						.sortByDisplay()
						.insertStartingPair(-1, "---")
						.setElementName(TOWN_SEL_KEY)
						.setSelectedKey(getSelectedTownId())
						.useGenericUpdater()
						.getHtmlString();

	const tagsel = buildOptSelector()
						.configureFromMap(getTagOptionMap())
						.setElementName(TAG_SEL_KEY)
						.setSelectedKey(GENERIC_OPT_SELECT_MAP.get(TAG_SEL_KEY))
						.useGenericUpdater()
						.getHtmlString();

	const sortsel = buildOptSelector()
						.configureFromMap(SORT_OPTION_MAP)
						.setElementName(SORT_SEL_KEY)
						.setSelectedKey(GENERIC_OPT_SELECT_MAP.get(SORT_SEL_KEY))
						.useGenericUpdater()
						.getHtmlString();

	return `
		<table class="basic-table" width="40%">
		<tr>
		<td>Town</td>
		<td colspan="2">${townsel}</td>
		</tr>
		<tr>
		<td>Tag</td>
		<td colspan="2">${tagsel}</td>
		</tr>
		<tr>
		<td>Sort By</td>
		<td colspan="2">${sortsel}</td>
		</tr>
		</table>
	`;
}

// Projects matching the current town/tag filters, in the current sort
// order - what the main listing shows, and what copySelection copies
function getSelectedProjects(docmap) {

	docmap = docmap || getProjectDocMap();
	const towntrg = getSelectedTownId();
	const tagtrg = GENERIC_OPT_SELECT_MAP.get(TAG_SEL_KEY);
	const sortkey = GENERIC_OPT_SELECT_MAP.get(SORT_SEL_KEY);

	return W.getItemList(MAIN_TABLE)
		.filter(item => towntrg == -1 || item.getTownId() == towntrg)
		.filter(item => matchesTagFilter(item, tagtrg))
		.sort(getSortComparator(sortkey, docmap));
}

// Main listing: one row per project
function getMainPageInfo() {

	const docmap = getProjectDocMap();
	const contactcountmap = getProjectContactCountMap();
	const itemlist = getSelectedProjects(docmap);

	var pageinfo = `<h3>PlanScan Projects</h3>

		${getUiControlTable()}

		<br/>

		<div>Showing ${itemlist.length} project(s)
		&nbsp;&nbsp;
		<button onclick="javascript:copySelection()" title="Copy these projects (town, descriptions, contacts, source links) with light formatting">
		<i class="fa-regular fa-copy"></i> Copy selection</button>
		</div>

		<br/>

		<table class="basic-table" width="95%">
		<tr>
		<th width="5%">ID</th>
		<th width="12%">Town</th>
		<th>Short Description</th>
		<th width="18%">Tags</th>
		<th width="6%">#Docs</th>
		<th width="8%">#Contacts</th>
		<th width="10%">Latest Doc</th>
		</tr>
	`;

	itemlist.forEach(function(item) {

		const doclist = docmap.get(item.getId()) || [];

		const rowstr = `
			<tr class="editable" onclick="javascript:editStudyItem(${item.getId()})">
			<td>${item.getId()}</td>
			<td>${getTownName(item.getTownId())}</td>
			<td class="left-align">${item.getShortDesc() || "(no short_desc)"}</td>
			<td class="left-align">${getTagList(item).join(", ")}</td>
			<td>${doclist.length}</td>
			<td>${contactcountmap.get(item.getId()) || ""}</td>
			<td>${getLatestDocDate(doclist) || "?"}</td>
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

<html>
<head>
<title>PlanScan Contacts</title>

<!-- standard wisp include tag -->
<wisp/>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css"> </link>

<script>

const MAIN_TABLE = 'contact_info';

let EDIT_STUDY_ITEM = -1;

const TOWN_SEL_KEY = "TownSelKey";

GENERIC_OPT_SELECT_MAP.set(TOWN_SEL_KEY, -1);


function getTownName(townid) {
	if(townid == null) { return "?"; }
	const town = W.lookupItem('town', townid);
	if(town == null) { return "?"; }
	return `${town.getName()}, ${town.getState()}`;
}

function getSelectedTownId() {
	return parseInt(GENERIC_OPT_SELECT_MAP.get(TOWN_SEL_KEY));
}

// contact id -> list of linked projects, built once per redisplay
// rather than scanning contact_project for every row
function getContactProjectMap() {

	const projmap = new Map();

	W.getItemList('contact_project').forEach(function(link) {
		const project = W.lookupItem('projects', link.getProjectId());
		if(project == null) { return; }

		if(!projmap.has(link.getContactId())) {
			projmap.set(link.getContactId(), []);
		}
		projmap.get(link.getContactId()).push(project);
	});

	return projmap;
}

// Distinct town ids among a contact's projects - contacts have no town of
// their own, only through the projects they're linked to
function getTownIdList(projlist) {
	return [...new Set(projlist.map(project => project.getTownId()).filter(tid => tid != null))];
}

// Town filter options: only towns that have at least one linked contact
function getTownOptionMap(projmap) {

	const townset = new Set();
	projmap.forEach(projlist => getTownIdList(projlist).forEach(tid => townset.add(tid)));

	return PSUTIL.buildGenericMap([...townset], tid => tid, tid => getTownName(tid));
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

// Auto-generated redisplay function
function redisplay() {
	const pageinfo = EDIT_STUDY_ITEM == -1 ? getMainPageInfo() : getEditPageInfo();
	U.populateSpanData({"page_info" : PSUTIL.getSimpleHeader() + pageinfo });
}

function getUiControlTable(projmap) {

	const townsel = buildOptSelector()
						.configureFromMap(getTownOptionMap(projmap))
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

// Sort key: company, falling back to the person's name for an individual
function getSortName(item) {
	return (item.getCompany() || item.getName() || "").toLowerCase();
}

// Company name plus a small link icon for the web site (if any). The icon
// stops the click from bubbling up, so it opens the site rather than the
// detail view.
function getCompanyHtml(item) {
	const company = PSUTIL.escapeHtml(item.getCompany() || "");
	const website = item.getWebSite();
	if(!website) { return company; }

	return `${company}
		&nbsp;<a href="${PSUTIL.escapeHtml(website)}" target="_blank" title="${PSUTIL.escapeHtml(website)}"
			onclick="event.stopPropagation()"><i class="fa-solid fa-arrow-up-right-from-square fa-xs"></i></a>`;
}

// Main listing: one row per contact, sorted by company. Only the
// Company/Name cells open the detail view, so the phone/email links stay clickable.
function getMainPageInfo() {

	const projmap = getContactProjectMap();
	const towntrg = getSelectedTownId();

	const itemlist = W.getItemList(MAIN_TABLE)
		.filter(item => towntrg == -1 || getTownIdList(projmap.get(item.getId()) || []).includes(towntrg))
		.sort(U.proxySort(item => [getSortName(item), (item.getName() || "").toLowerCase(), item.getId()]));

	var pageinfo = `<h3>PlanScan Contacts</h3>

		${getUiControlTable(projmap)}

		<br/>

		<div>Showing ${itemlist.length} contact(s)</div>

		<br/>

		<table class="basic-table" width="95%">
		<tr>
		<th width="24%">Company</th>
		<th>Name</th>
		<th width="13%">Phone</th>
		<th width="22%">Email</th>
		<th width="15%">Town(s)</th>
		</tr>
	`;

	itemlist.forEach(function(item) {

		const projlist = projmap.get(item.getId()) || [];
		const opendetail = `onclick="javascript:editStudyItem(${item.getId()})"`;

		const rowstr = `
			<tr class="editable">
			<td class="left-align" ${opendetail}>${getCompanyHtml(item)}</td>
			<td class="left-align" ${opendetail}>${PSUTIL.escapeHtml(item.getName() || "")}</td>
			<td>${PSUTIL.getPhoneHtml(item.getPhone())}</td>
			<td class="left-align">${PSUTIL.getEmailHtml(item.getEmail())}</td>
			<td class="left-align">${getTownIdList(projlist).map(getTownName).join("; ")}</td>
			</tr>
		`;
		pageinfo += rowstr;
	});

	pageinfo += `</table>`;
	return pageinfo;
}

// Detail view: contact fields plus the projects it's linked to
function getEditPageInfo() {

	const item = getStudyItem();
	const projlist = (getContactProjectMap().get(item.getId()) || [])
		.sort(U.proxySort(project => [-project.getId()]));

	var pageinfo = `
	<h4>Contact Detail</h4>
	<table class="basic-table" width="60%">
	<tr>
	<td>Back</td>
	<td><a href="javascript:back2Main()"><img src="/u/shared/image/leftarrow.png" height="18"/></a></td>
	</tr>
	<tr><td>ID</td><td>${item.getId()}</td></tr>
	<tr><td>Name</td><td class="left-align">${PSUTIL.escapeHtml(item.getName() || "")}</td></tr>
	<tr><td>Company</td><td class="left-align">${PSUTIL.escapeHtml(item.getCompany() || "")}</td></tr>
	<tr><td>Phone</td><td class="left-align">${PSUTIL.getPhoneHtml(item.getPhone())}</td></tr>
	<tr><td>Email</td><td class="left-align">${PSUTIL.getEmailHtml(item.getEmail())}</td></tr>
	<tr><td>Web Site</td><td class="left-align">${PSUTIL.getWebSiteHtml(item.getWebSite())}</td></tr>
	</table>

	<br/>

	<h4>Projects (${projlist.length})</h4>
	<table class="basic-table" width="70%">
	<tr>
	<th width="6%">ID</th>
	<th width="16%">Town</th>
	<th>Short Description</th>
	</tr>
	${projlist.map(project => `
	<tr>
	<td>${project.getId()}</td>
	<td>${getTownName(project.getTownId())}</td>
	<td class="left-align">${project.getShortDesc() || "(no short_desc)"}</td>
	</tr>
	`).join("")}
	</table>
	`;

	return pageinfo;
}

</script>
<body onLoad="javascript:redisplay()">
<center>
<div id="page_info"></div>

</center>
</body>
</html>

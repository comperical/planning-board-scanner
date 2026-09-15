<html>
<head>
<title>PlanScan Scan Log</title>

<!-- standard wisp include tag -->
<wisp/>

<script>

const MAIN_TABLE = 'scan_log';

let EDIT_STUDY_ITEM = -1;

function getStudyItem() {
	U.massert(EDIT_STUDY_ITEM != -1, "No study item has been selected");
	return W.lookupItem(MAIN_TABLE, EDIT_STUDY_ITEM);
}

function getTownName(townid) {
	if(townid == null) { return "?"; }
	const town = W.lookupItem('town', townid);
	if(town == null) { return "?"; }
	return town.getName() || "?";
}

// Documents whose first_scan_id points at this scan - i.e. files this
// scan pass uncovered (as opposed to files it merely re-touched).
function getFilesUncovered(scanid) {
	return W.getItemList('documents').filter(doc => doc.getFirstScanId() == scanid);
}

// scan_log's alpha_time_est/omega_time_est are SQLite datetime('now')
// strings ("YYYY-MM-DD HH:MM:SS", UTC, no timezone marker) - normalize to
// ISO-8601 (space -> "T", append "Z") so Date.parse is reliable.
function parseScanTime(timestr) {
	if(!timestr) { return null; }
	const ms = Date.parse(timestr.replace(" ", "T") + "Z");
	return isNaN(ms) ? null : ms;
}

function getDurationMinutes(item) {
	const startms = parseScanTime(item.getAlphaTimeEst());
	const endms = parseScanTime(item.getOmegaTimeEst());
	if(startms == null || endms == null) { return "(in progress)"; }
	return Math.round((endms - startms) / 60000) + " min";
}

// "YYYY-MM-DD HH:MM:SS" -> "MM-DD HH:MM" - we don't need year or seconds.
function formatStartTime(timestr) {
	if(!timestr) { return "?"; }
	const m = timestr.match(/^\d{4}-(\d{2}-\d{2}) (\d{2}:\d{2})/);
	return m ? `${m[1]} ${m[2]}` : timestr;
}

function shorten4Display(ob) {
	const s = '' + ob;
	if(s.length < 60) { return s; }
	return s.substring(0, 57) + '...';
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

// Main listing: one row per scan_log pass, most recent first
function getMainPageInfo() {

	var pageinfo = `<h3>PlanScan Scan Log</h3>
		<table class="basic-table" width="50%">
		<tr>
		<th>Town</th>
		<th>Start</th>
		<th>Time</th>
		<th>#Files</th>
		</tr>
	`;

	const itemlist = W.getItemList(MAIN_TABLE)
		.sort(U.proxySort(item => [item.getAlphaTimeEst() || ""]))
		.reverse();

	itemlist.forEach(function(item) {

		const filecount = getFilesUncovered(item.getId()).length;

		const rowstr = `
			<tr class="editable" onclick="javascript:editStudyItem(${item.getId()})">
			<td>${getTownName(item.getTownId())}</td>
			<td>${formatStartTime(item.getAlphaTimeEst())}</td>
			<td>${getDurationMinutes(item)}</td>
			<td>${filecount}</td>
			</tr>
		`;
		pageinfo += rowstr;
	});

	pageinfo += `</table>`;
	return pageinfo;
}

// Detail view: scan metadata plus the files it uncovered
function getEditPageInfo() {

	const item = getStudyItem();
	const filelist = getFilesUncovered(item.getId())
		.sort(U.proxySort(doc => [doc.getDocDate() || ""]))
		.reverse();

	var pageinfo = `
	<h4>Scan Detail</h4>
	<table class="basic-table" width="50%">
	<tr>
	<td>Back</td>
	<td></td>
	<td><a href="javascript:back2Main()"><img src="/u/shared/image/leftarrow.png" height="18"/></a></td>
	</tr>
	<tr><td>Town</td><td colspan="2">${getTownName(item.getTownId())}</td></tr>
	<tr><td>Start</td><td colspan="2">${item.getAlphaTimeEst() || "?"}</td></tr>
	<tr><td>Time</td><td colspan="2">${getDurationMinutes(item)}</td></tr>
	</table>

	<br/>

	<h4>Notes</h4>
	<table class="basic-table" width="50%">
	<tr><td>${(item.getNotes() || "").split("\n").join("<br/>")}</td></tr>
	</table>

	<br/>

	<h4>Files Uncovered (${filelist.length})</h4>
	<table class="basic-table" width="70%">
	<tr>
	<th>Date</th>
	<th>File</th>
	<th width="10%">Pages</th>
	</tr>
	${filelist.map(doc => `
	<tr>
	<td>${doc.getDocDate() || "?"}</td>
	<td class="left-align">${shorten4Display(doc.getFilePath())}</td>
	<td>${doc.getPageCount() || "?"}</td>
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

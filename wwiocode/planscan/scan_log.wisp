<html>
<head>
<title>PlanScan Scan Log</title>

<!-- standard wisp include tag -->
<wisp/>

<script>

const MAIN_TABLE = 'scan_log';

let EDIT_STUDY_ITEM = -1;

const SORT_SEL_KEY = "SortSelKey";

GENERIC_OPT_SELECT_MAP.set(SORT_SEL_KEY, "next_scan");

// Same cadence as the daily-update skill: NextToScan due_days=7
const SCAN_DUE_DAYS = 7;

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

// Number of documents in the whole DB that have never been through
// LogAnalysis - same definition NextToAnalyze (and towns.wisp) uses.
function getUnanalyzedCount() {
	const analyzedset = new Set(W.getItemList('analysis_log').map(log => log.getDocumentId()));
	return W.getItemList('documents').filter(doc => !analyzedset.has(doc.getId())).length;
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

// Most recent good scan_log alpha_time_est for this town, or null if never
// scanned. Same rule as NextToScan (and towns.wisp): unclosed passes and ones
// whose notes start with FAILED don't count.
function getLastGoodScanTime(townid) {
	const timelist = W.getItemList(MAIN_TABLE)
		.filter(scan => scan.getTownId() == townid)
		.filter(scan => scan.getOmegaTimeEst() != null)
		.filter(scan => !(scan.getNotes() || "").startsWith("FAILED"))
		.map(scan => scan.getAlphaTimeEst())
		.filter(t => t != null);
	if(timelist.length == 0) { return null; }
	return timelist.sort().reverse()[0];
}

// "YYYY-MM-DD" date the town is next due for a scan: last good scan plus
// SCAN_DUE_DAYS, or today if never successfully scanned.
function getNextScanDate(townid) {
	const lastms = parseScanTime(getLastGoodScanTime(townid));
	const duems = lastms == null ? Date.now() : lastms + SCAN_DUE_DAYS * 86400000;
	return new Date(duems).toISOString().substring(0, 10);
}

// One scan_log record per town: the one with the latest alpha_time_est
// (any pass, including failed or in-progress ones).
function getLatestScanPerTown() {
	const latestmap = new Map();
	W.getItemList(MAIN_TABLE).forEach(function(scan) {
		const prev = latestmap.get(scan.getTownId());
		if(prev == null || (scan.getAlphaTimeEst() || "") > (prev.getAlphaTimeEst() || "")) {
			latestmap.set(scan.getTownId(), scan);
		}
	});
	return [...latestmap.values()];
}

// Number of towns whose most recent scan pass failed: either never closed
// (no omega_time_est) or closed with notes starting with FAILED.
function getRecentFailedCount() {
	return getLatestScanPerTown()
		.filter(scan => scan.getOmegaTimeEst() == null || (scan.getNotes() || "").startsWith("FAILED"))
		.length;
}

// A daily-update run has no ID of its own, so the "last scan" run is every
// scan pass that started within LAST_RUN_WINDOW_HOURS of the most recent
// pass's start.
const LAST_RUN_WINDOW_HOURS = 12;

// Display string for the "Last Scan" control row: number of distinct towns
// scanned in the last run, and the number of documents those passes uncovered.
function getLastScanDisplay() {
	const scanlist = W.getItemList(MAIN_TABLE).filter(scan => parseScanTime(scan.getAlphaTimeEst()) != null);
	if(scanlist.length == 0) { return "(none)"; }

	const latestms = Math.max(...scanlist.map(scan => parseScanTime(scan.getAlphaTimeEst())));
	const runlist = scanlist.filter(scan => parseScanTime(scan.getAlphaTimeEst()) >= latestms - LAST_RUN_WINDOW_HOURS * 3600000);

	const townset = new Set(runlist.map(scan => scan.getTownId()));
	const scanidset = new Set(runlist.map(scan => scan.getId()));
	const doccount = W.getItemList('documents').filter(doc => scanidset.has(doc.getFirstScanId())).length;

	// "M/DD" of the most recent pass's start (UTC), no leading zero on the month
	const lastdate = new Date(latestms).toISOString().substring(5, 10).replace("-", "/").replace(/^0/, "");

	return `${lastdate}, ${townset.size}, ${doccount}`;
}

const SORT_OPTION_MAP = new Map([
	["most_recent", "Most Recent"],
	["next_scan", "Next Scan"],
	["town_name", "Town Name"],
	["num_files", "#Files"]
]);

function getSortComparator(sortkey) {

	const alphaof = item => item.getAlphaTimeEst() || "";

	if(sortkey == "next_scan") {
		return U.proxySort(item => [getNextScanDate(item.getTownId()), getTownName(item.getTownId()), alphaof(item)]);
	}

	if(sortkey == "town_name") {
		return U.proxySort(item => [getTownName(item.getTownId()), alphaof(item)]);
	}

	if(sortkey == "num_files") {
		return U.proxySort(item => [-getFilesUncovered(item.getId()).length, alphaof(item)]);
	}

	// Default: most_recent - latest start time first
	return U.proxySort(item => [-(parseScanTime(item.getAlphaTimeEst()) || 0)]);
}

function getUiControlTable() {

	const sortsel = buildOptSelector()
						.configureFromMap(SORT_OPTION_MAP)
						.setElementName(SORT_SEL_KEY)
						.setSelectedKey(GENERIC_OPT_SELECT_MAP.get(SORT_SEL_KEY))
						.useGenericUpdater()
						.getHtmlString();

	// Count rows are only shown when there's something to report
	const countrow = (label, count) => count == 0 ? "" : `
		<tr>
		<td>${label}</td>
		<td colspan="2">${count}</td>
		</tr>
	`;

	return `
		<table class="basic-table" width="40%">
		<tr>
		<td>Sort By</td>
		<td colspan="2">${sortsel}</td>
		</tr>
		${countrow("#Recent Failed", getRecentFailedCount())}
		${countrow("#Unanalyzed Docs", getUnanalyzedCount())}
		<tr>
		<td>Last Scan</td>
		<td colspan="2">${getLastScanDisplay()}</td>
		</tr>
		</table>
	`;
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

		${getUiControlTable()}

		<br/>

		<table class="basic-table" width="60%">
		<tr>
		<th>Town</th>
		<th>Start</th>
		<th>Time</th>
		<th>#Files</th>
		<th>Next Scan</th>
		</tr>
	`;

	const sortkey = GENERIC_OPT_SELECT_MAP.get(SORT_SEL_KEY);

	const itemlist = getLatestScanPerTown()
		.sort(getSortComparator(sortkey));

	// UTC "YYYY-MM-DD", same basis as getNextScanDate
	const todaystr = new Date().toISOString().substring(0, 10);

	itemlist.forEach(function(item) {

		const filecount = getFilesUncovered(item.getId()).length;
		const nextscan = getNextScanDate(item.getTownId());

		// Light pink when the town is due for a scan (next scan today or earlier)
		const duestyle = nextscan <= todaystr ? ` style="background-color: #ffe0e6"` : "";

		const rowstr = `
			<tr class="editable"${duestyle} onclick="javascript:editStudyItem(${item.getId()})">
			<td>${getTownName(item.getTownId())}</td>
			<td>${formatStartTime(item.getAlphaTimeEst())}</td>
			<td>${getDurationMinutes(item)}</td>
			<td>${filecount}</td>
			<td>${nextscan.substring(5)}</td>
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

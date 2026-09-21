<html>
<head>
<title>PlanScan Towns</title>

<!-- standard wisp include tag -->
<wisp/>

<script>

const MAIN_TABLE = 'town';

const SORT_SEL_KEY = "SortSelKey";

GENERIC_OPT_SELECT_MAP.set(SORT_SEL_KEY, "next_up");

function getDocsForTown(townid) {
	return W.getItemList('documents').filter(doc => doc.getTownId() == townid);
}

function getProjectsForTown(townid) {
	return W.getItemList('projects').filter(project => project.getTownId() == townid);
}

// Documents for this town that have never been through LogAnalysis - same
// definition NextToAnalyze uses.
function getUnanalyzedDocsForTown(townid) {
	const analyzedset = new Set(W.getItemList('analysis_log').map(log => log.getDocumentId()));
	return getDocsForTown(townid).filter(doc => !analyzedset.has(doc.getId()));
}

function formatSize(bytes) {
	if(bytes == null) { return "?"; }
	return Math.round(bytes / 1024) + " KB";
}

function getMostRecentDocDate(doclist) {
	const datelist = doclist.map(doc => doc.getDocDate()).filter(d => d != null);
	if(datelist.length == 0) { return "?"; }
	return datelist.sort().reverse()[0];
}

// Sort key for "next up in the analysis queue": mirrors NextToAnalyze's
// ordering (most recent doc_date first among unanalyzed documents), applied
// per-town. rank 0 = has an unanalyzed doc with a known date (sorted by that
// date, most recent first); rank 1 = has backlog but no known date; rank 2 =
// nothing left to analyze (sinks to the bottom).
function getNextUpSortKey(townid) {

	const unanalyzed = getUnanalyzedDocsForTown(townid);
	if(unanalyzed.length == 0) { return [2, 0]; }

	const dated = unanalyzed.filter(doc => doc.getDocDate() != null);
	if(dated.length == 0) { return [1, 0]; }

	const maxdate = dated.map(doc => doc.getDocDate()).sort().reverse()[0];
	return [0, -Date.parse(maxdate)];
}

// Display string for the "Next Up" column, matching getNextUpSortKey's ranks.
function getNextUpDisplay(townid) {

	const unanalyzed = getUnanalyzedDocsForTown(townid);
	if(unanalyzed.length == 0) { return "(done)"; }

	const dated = unanalyzed.filter(doc => doc.getDocDate() != null);
	if(dated.length == 0) { return "(no date)"; }

	return dated.map(doc => doc.getDocDate()).sort().reverse()[0];
}

// Most recent scan_log alpha_time_est for this town ("YYYY-MM-DD HH:MM:SS"
// UTC strings, so they sort lexically), or null if never scanned.
function getLastScanTime(townid) {
	const timelist = W.getItemList('scan_log')
		.filter(scan => scan.getTownId() == townid)
		.map(scan => scan.getAlphaTimeEst())
		.filter(t => t != null);
	if(timelist.length == 0) { return null; }
	return timelist.sort().reverse()[0];
}

// Display string for the "Last Scanned" column: date plus days ago.
function getLastScanDisplay(townid) {
	const lastscan = getLastScanTime(townid);
	if(lastscan == null) { return "(never)"; }
	const ms = Date.parse(lastscan.replace(" ", "T") + "Z");
	const daysago = Math.floor((Date.now() - ms) / 86400000);
	return `${lastscan.substring(0, 10)} (${daysago}d)`;
}

const SORT_OPTION_MAP = new Map([
	["next_up", "Next Up"],
	["next_scan", "Next To Scan"],
	["town_name", "Town Name"],
	["num_projects", "#Projects"]
]);

function getSortComparator(sortkey) {

	if(sortkey == "town_name") {
		return U.proxySort(item => [item.getName() || "", item.getState() || ""]);
	}

	// Mirrors NextToScan: never-scanned towns first, then oldest last scan
	if(sortkey == "next_scan") {
		return U.proxySort(item => {
			const lastscan = getLastScanTime(item.getId());
			return lastscan == null ? [0, "", item.getName() || ""] : [1, lastscan, item.getName() || ""];
		});
	}

	if(sortkey == "num_projects") {
		return U.proxySort(item => [-getProjectsForTown(item.getId()).length, item.getName() || ""]);
	}

	// Default: next_up
	return U.proxySort(item => getNextUpSortKey(item.getId()));
}

function getUiControlTable() {

	const sortsel = buildOptSelector()
						.configureFromMap(SORT_OPTION_MAP)
						.setElementName(SORT_SEL_KEY)
						.setSelectedKey(GENERIC_OPT_SELECT_MAP.get(SORT_SEL_KEY))
						.useGenericUpdater()
						.getHtmlString();

	return `
		<table class="basic-table" width="40%">
		<tr>
		<td>Sort By</td>
		<td colspan="2">${sortsel}</td>
		</tr>
		</table>
	`;
}

// Auto-generated redisplay function
function redisplay() {
	U.populateSpanData({"page_info" : PSUTIL.getSimpleHeader() + getMainPageInfo() });
}

// Main listing: one row per town
function getMainPageInfo() {

	var pageinfo = `<h3>PlanScan Towns</h3>

		${getUiControlTable()}

		<br/>

		<table class="basic-table" width="80%">
		<tr>
		<th>Town</th>
		<th>Next Up</th>
		<th>Last Scanned</th>
		<th>#Files</th>
		<th>Total Size</th>
		<th>Most Recent File</th>
		<th>#Projects</th>
		</tr>
	`;

	const sortkey = GENERIC_OPT_SELECT_MAP.get(SORT_SEL_KEY);

	const itemlist = W.getItemList(MAIN_TABLE)
		.sort(getSortComparator(sortkey));

	itemlist.forEach(function(item) {

		const doclist = getDocsForTown(item.getId());
		const projectlist = getProjectsForTown(item.getId());
		const totalsize = doclist.map(doc => doc.getFileSizeBytes() || 0).reduce((a,b) => a+b, 0);

		const rowstr = `
			<tr>
			<td>${item.getName() || "?"}, ${item.getState() || "?"}</td>
			<td>${getNextUpDisplay(item.getId())}</td>
			<td>${getLastScanDisplay(item.getId())}</td>
			<td>${doclist.length}</td>
			<td>${formatSize(totalsize)}</td>
			<td>${getMostRecentDocDate(doclist)}</td>
			<td>${projectlist.length}</td>
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

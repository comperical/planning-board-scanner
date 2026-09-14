<html>
<head>
<title>PlanScan Towns</title>

<!-- standard wisp include tag -->
<wisp/>

<script>

const MAIN_TABLE = 'town';

function getDocsForTown(townid) {
	return W.getItemList('documents').filter(doc => doc.getTownId() == townid);
}

function getProjectsForTown(townid) {
	return W.getItemList('projects').filter(project => project.getTownId() == townid);
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

// Auto-generated redisplay function
function redisplay() {
	U.populateSpanData({"page_info" : PSUTIL.getSimpleHeader() + getMainPageInfo() });
}

// Main listing: one row per town
function getMainPageInfo() {

	var pageinfo = `<h3>PlanScan Towns</h3>
		<table class="basic-table" width="80%">
		<tr>
		<th>Town</th>
		<th>#Files</th>
		<th>Total Size</th>
		<th>Most Recent File</th>
		<th>#Projects</th>
		</tr>
	`;

	const itemlist = W.getItemList(MAIN_TABLE)
		.sort(U.proxySort(item => [item.getName() || "", item.getState() || ""]));

	itemlist.forEach(function(item) {

		const doclist = getDocsForTown(item.getId());
		const projectlist = getProjectsForTown(item.getId());
		const totalsize = doclist.map(doc => doc.getFileSizeBytes() || 0).reduce((a,b) => a+b, 0);

		const rowstr = `
			<tr>
			<td>${item.getName() || "?"}, ${item.getState() || "?"}</td>
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

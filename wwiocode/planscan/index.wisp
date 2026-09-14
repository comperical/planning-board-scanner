<html>
<head>

<title>PlanScan</title>

<!-- standard wisp include tag -->
<wisp/>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css"> </link>

<style>

.link-button {
    display: flex;
    align-items: center;
    padding: 5px 15px;
    margin: 3px;
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 20px; /* This creates the rounded edges */
    text-decoration: none;
    color: #333;
}

.link-button a {
    text-decoration: none;
    color: #333;
    font-weight: bold;
}

.icon {
    margin-right: 10px;
    font-size: 20px;
}

/* Hover effect */
.link-button:hover {
    background-color: #e0e0e0; /* Slightly darker shade on hover */
}

.rightpad {
    margin-right: 8px;
}

</style>

<script>

function composeLinkDiv(linktup)
{
    return `
        <div class="link-button">
          <i class="${linktup[0]} rightpad"></i>
          <a href="${linktup[1]}">${linktup[2]}</a>
        </div>
    `;
}

function getNavSection()
{
    const linkdata = [
        ["fa-solid fa-file-lines", "documents", "Documents"],
        ["fa-solid fa-city", "towns", "Towns"]
    ];

    return linkdata.map(composeLinkDiv).join("\n");
}

// Documents with zero analysis_log rows - same definition NextToAnalyze uses
function getBacklogCount()
{
    const analyzedset = new Set(W.getItemList('analysis_log').map(log => log.getDocumentId()));
    return W.getItemList('documents').filter(doc => !analyzedset.has(doc.getId())).length;
}

function getDashBoardTable()
{
    const towncount = W.getItemList('town').length;
    const doccount = W.getItemList('documents').length;
    const projectcount = W.getItemList('projects').length;
    const backlogcount = getBacklogCount();

    return `
        <table class="basic-table" width="80%">
        <tr>
        <th colspan="2">PlanScan Stats</th>
        </tr>

        <tr>
        <td>Towns</td>
        <td>${towncount}</td>
        </tr>

        <tr>
        <td>Documents</td>
        <td>${doccount}</td>
        </tr>

        <tr>
        <td>Projects</td>
        <td>${projectcount}</td>
        </tr>

        <tr>
        <td>Unanalyzed Backlog</td>
        <td>${backlogcount}</td>
        </tr>

        </table>
    `;
}

function redisplay()
{
    U.populateSpanData({
        "header_info" : PSUTIL.getSimpleHeader(),
        "nav_section" : getNavSection(),
        "dash_table" : getDashBoardTable()
    });
}

</script>

</head>

<body onLoad="javascript:redisplay()">

<center>
<div id="header_info"></div>

<h3>PlanScan</h3>

<table width="70%" class="basic-table">

<tr>
<td width="40%" valign="top">

<center>
<h3>Navigation</h3>
</center>

<div id="nav_section"></div>

</td>
<td valign="top">

<center>
<h3>Dashboard</h3>
</center>

<div id="dash_table"></div>

</td>
</tr>

</table>

</center>
<br/>
</body>
</html>

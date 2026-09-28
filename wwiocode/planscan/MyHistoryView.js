
// GitHub-style meeting history for projects. A "meeting" is one town on
// one doc_date - an agenda, minutes and materials for the same meeting all
// share that date, so they collapse into a single entry.
HISTORY = {

    // How far back the history views look
    WINDOW_WEEKS : 20,

    // Meeting-date colors run along one blue ramp: a town's oldest date in
    // the window gets OLD_RGB, its newest NEW_RGB, the rest evenly between
    OLD_RGB : [158, 202, 225],
    NEW_RGB : [8, 48, 107],

    // A Date as ISO YYYY-MM-DD in local time (toISOString would give UTC)
    toIso : function(d)
    {
        const pad = n => ("" + n).padStart(2, "0");
        return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
    },

    // ISO date of the start of the history window
    getWindowStartIso : function()
    {
        const d = new Date();
        d.setDate(d.getDate() - 7 * HISTORY.WINDOW_WEEKS);
        return HISTORY.toIso(d);
    },

    // town id -> (doc_date -> list of that town's documents), for dates in
    // the window (future dates included - those are upcoming agendas).
    // One pass over documents, so the listing can build it once per redisplay.
    getAllTownDateMaps : function()
    {
        const startiso = HISTORY.getWindowStartIso();
        const townmap = new Map();

        W.getItemList('documents')
            .filter(doc => doc.getDocDate() != null && doc.getDocDate() >= startiso)
            .forEach(function(doc) {
                if(!townmap.has(doc.getTownId())) {
                    townmap.set(doc.getTownId(), new Map());
                }
                const datemap = townmap.get(doc.getTownId());
                if(!datemap.has(doc.getDocDate())) {
                    datemap.set(doc.getDocDate(), []);
                }
                datemap.get(doc.getDocDate()).push(doc);
            });

        return townmap;
    },

    getTownDateMap : function(townid)
    {
        return HISTORY.getAllTownDateMaps().get(townid) || new Map();
    },

    // doc_date -> color, for a town's dates in the window; a lone date
    // gets the newest color
    getDateColorMap : function(datemap)
    {
        const datelist = [...datemap.keys()].sort();
        const colormap = new Map();
        datelist.forEach(function(iso, idx) {
            const frac = datelist.length == 1 ? 1 : idx / (datelist.length - 1);
            const rgb = HISTORY.OLD_RGB.map((c, i) => Math.round(c + frac * (HISTORY.NEW_RGB[i] - c)));
            colormap.set(iso, `rgb(${rgb.join(",")})`);
        });
        return colormap;
    },

    // "2026-09-16" -> "09/16"
    getShortDate : function(iso)
    {
        return iso.substring(5, 7) + "/" + iso.substring(8, 10);
    },

    // Legend for one town: one colored box per meeting date in the window,
    // oldest to newest, MM/DD in small print after each box. Hover shows the
    // file names.
    getTownLegendHtml : function(townid)
    {
        const datemap = HISTORY.getTownDateMap(townid);
        const colormap = HISTORY.getDateColorMap(datemap);

        const boxes = [...datemap.keys()].sort().map(function(iso) {
            const doclist = datemap.get(iso);
            const tip = iso + "\n" + doclist.map(doc => doc.getFilePath().split("/").pop()).join("\n");
            return `<span class="hist-date" title="${PSUTIL.escapeHtml(tip)}">
                <span class="hist-box" style="background:${colormap.get(iso)}"></span>
                <span class="hist-date-label">${HISTORY.getShortDate(iso)}</span></span>`;
        }).join("");

        return `
            <div class="hist-legend">
            ${datemap.size == 0 ? `<span class="hist-date-label">no meetings in last ${HISTORY.WINDOW_WEEKS} weeks</span>` : boxes}
            </div>
        `;
    },

    // One project's meeting history, for the listing: a box per meeting
    // date of its town in the window, same order and colors as the town
    // legend. Filled = the project is in that meeting's documents; outline
    // only (in the date's color) = the town met without it. Hover shows the
    // date and the project's files.
    getProjectStripHtml : function(doclist, datemap)
    {
        if(doclist.length == 0) {
            return `<span class="hist-date-label">no docs</span>`;
        }

        const colormap = HISTORY.getDateColorMap(datemap);

        const boxes = [...datemap.keys()].sort().map(function(iso) {
            const hits = doclist.filter(doc => doc.getDocDate() == iso);

            if(hits.length == 0) {
                return `<span class="hist-box" style="border:1.5px solid ${colormap.get(iso)}" title="${iso}: not mentioned"></span>`;
            }

            const tip = iso + "\n" + hits.map(doc => doc.getFilePath().split("/").pop()).join("\n");
            return `<span class="hist-box" style="background:${colormap.get(iso)}" title="${PSUTIL.escapeHtml(tip)}"></span>`;
        }).join("");

        return `<span class="hist-strip">${boxes}</span>`;
    },

    // Styles for the history views; pages include this once via
    // ${HISTORY.getStyleHtml()} so the CSS lives alongside the code
    getStyleHtml : function()
    {
        return `
            <style>
            .hist-legend { text-align: center; white-space: nowrap; }
            .hist-date {
                display: inline-flex;
                align-items: center;
                gap: 2px;
                margin: 0 4px;
                vertical-align: middle;
                cursor: default;
            }
            .hist-box {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 2px;
                box-sizing: border-box;
            }
            .hist-strip {
                display: inline-flex;
                align-items: center;
                gap: 3px;
                white-space: nowrap;
            }
            .hist-date-label { font-size: 9px; color: #57606a; line-height: 1.1; }
            </style>
        `;
    }
}

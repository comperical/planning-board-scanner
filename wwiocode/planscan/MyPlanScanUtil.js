// Feb 2025: new clients use this check
W.setStrictBadFieldCheck(true);

PSUTIL = {

    WARNING_EMOJI : "&#9888;&#65039;",

    KEY_EMOJI : "&#128273;",

    CROSS_MARK_EMOJI : "&#10062;",

    TRASH_EMOJI : "&#128465;&#65039;",

    CHECKMARK_EMOJI : "&#9989;",

    LEFT_ARROW_EMOJI : "&#11013;&#65039;",

    LIGHTNING_EMOJI : "&#9889;",

    RIGHT_ARROW_EMOJI : "&#10145;&#65039;",

    // If you want to use the MODAL tech, you should include the SimpleModal JS package
    // in the page (see documents.wisp) and the modal CSS classes. If you don't do
    // that, this will have no effect.
    CURRENT_MODAL : null,

    getPageCode : function()
    {
        const path = window.location.pathname;
        return path.split("/").pop().replace(".wisp", "");
    },

    getSimpleHeader : function()
    {

        const modalhtml = PSUTIL.CURRENT_MODAL == null ? "" : PSUTIL.CURRENT_MODAL.getHtmlString();

        var header = `


            <a href="../planscan/index"><button>Home</button></a>


            &nbsp;
            &nbsp;
            &nbsp;

            <a href="../planscan/documents"><button>Documents</button></a>

            &nbsp;
            &nbsp;
            &nbsp;

            <a href="../planscan/towns"><button>Towns</button></a>

            </div>

            ${modalhtml}

        `;

        return header;

    },

    showWaitModal : function(message)
    {
        PSUTIL.CURRENT_MODAL = MODAL.build().setModalContentHtml(message);
        redisplay();
    },

    closeModal : function()
    {
        PSUTIL.CURRENT_MODAL = null;
        redisplay();
    },

    buildGenericMap : function(items, keyfunc, valfunc)
    {
        const mymap = new Map();

        items.forEach(function(itm){
            const k = keyfunc(itm);
            const v = valfunc(itm);
            mymap.set(k, v);
        });

        return mymap;
    }
}

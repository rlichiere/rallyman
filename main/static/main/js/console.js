

/* Console
*
* Replace and improve the standard console.log
*
* By default, Console is configured to act the same way as the standard console: messages given via Console.log are directed to the standard output.
* However, for reasons of flexibility and performance, messages are not produced by default.
* Message production can be activated via the `.useConsole` option.
*   Console.useConsole = true;
*
* In addition, it is possible to direct the messages to an UI console:
*   - Declare the HTML elements that should support the integration of the console via `.setElementContainer()` and `.setElementContent()`
*       Console.setElementContainer($('#some_container_element'));
*       Console.setElementContent($('#some_element_for_content'));
*   - Activate the UI output by calling `.useUIOutput()`
*       Console.useUIOutput(true)
* */
const Console = Object();


/* PRIVATE */

Console._useConsole = false;
Console._useStd = true;
Console._useUI = false;

Console._containerId = null;
Console._containerObj = null;
Console._contentId = null;
Console._contentObj = null;
Console._compensedId = null;
Console._compensedObj = null;


/* PUBLIC */


/* Configuration */

Console.useConsole = function(yes) {
    this._useConsole = (yes !== false);
};

Console.useStdOutput = function(show) {
    this._useStd = (show !== false);
    this._useConsole = this._useStd;
};

Console.useUIOutput = function(show) {
    this._useUI = (show !== false);
    this._useConsole = this._useUI;
};


/* Initialization */

Console.initialize = function(containerId, contentId, compensedId) {
    if (containerId) {
        this._containerId = containerId;
        this._containerObj = $('#' + this._containerId);
    }
    if (contentId) {
        this._contentId = contentId;
        this._contentObj = $('#' + this._contentId);
    }
    if (compensedId) {
        this._compensedId = compensedId;
        this._compensedObj = $('#' + this._compensedId);
    }

    let _this = this;
    $('#'+_this._containerId + ' div.float-right > ul.nav > li > button.close[role="close"]').click(function() {
        // hide console
        let _consoleHeight = _this._containerObj.height();
        _this._containerObj.hide();
        _this._compensedObj.css('margin-bottom', '-=' + _consoleHeight + 'px');
    });
    $('#'+_this._containerId + ' div.float-right > ul.nav > li > button.close[role="reduce"]').click(function() {
        // increase console height
        _this._containerObj.css('height', '100px');
        _this._compensedObj.css('margin-bottom', '100px');
        $(this).css('margin-bottom', '0');

    });
    $('#'+_this._containerId + ' div.float-right > ul.nav > li > button.close[role="increase"]').click(function() {
        // increase console height
        _this._containerObj.css('height', '+=30px');
        _this._compensedObj.css('margin-bottom', '+=30px');
        $('#'+_this._containerId + ' div.float-right > ul.nav > li > button.close[role="reduce"]').css('margin-bottom', '+=30px');
    });
    $('#'+this._containerId + ' div.float-right > ul.nav > li > button.close[role="decrease"]').click(function() {
        let _consoleHeight = _this._containerObj.height();
        // decrease console height
        if  (_consoleHeight > 100) {
            _this._containerObj.css('height', '-=30px');
            _this._compensedObj.css('margin-bottom', '-=30px');
            $('#'+_this._containerId + ' div.float-right > ul.nav > li > button.close[role="reduce"]').css('margin-bottom', '-=30px');
        }
    });

    if (this._useConsole) {
        if (this._useUI) {
            this.show();
        }
        this.log('Console is ready.');
    }
};

Console.show = function() {
    this._containerObj.show();
    let _consoleHeight = this._containerObj.height();
    this._compensedObj.css('margin-bottom', '+=' + _consoleHeight + 'px');
};

/* Exploitation */

Console.log = function(message) {
    if (this._useConsole) {

        if (this._useStd) {
            console.log(message);
        }

        if (this._useUI) {
            let _html;
            _html = this._contentObj.html();
            if (_html !== '') {
                _html += '<br />';
            }
            _html += message;
            console.log(_html);
            this._contentObj.html(_html);
        }

    }
};

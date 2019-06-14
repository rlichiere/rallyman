/* Console
*
* Replace and improve the standard console.log
*
* By default, Console is configured to act the same way as the standard console: messages given via Console.log are directed to the standard output.
* However, for reasons of flexibility and performance, messages are not produced by default.
* Message production can be activated via the `.useConsole` option.
*   Console.useConsole();
*
* In addition, it is possible to direct the messages to an UI console:
*   - Declare the HTML elements that should support the integration of the console via `.initialize`
*       Console.initialize($('#some_container_element'), $('#some_element_for_content'), $('#some_element_to_compensate'));
*   - Activate the UI output by calling `.useUIOutput()`
*       Console.useUIOutput()
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
Console._btnShowId = null;
Console._btnShowObj = null;
Console._btnHideId = null;
Console._btnHideObj = null;

Console._debug = null;

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

Console.initialize = function(containerId, contentId, compensedId, btnShowId, btnHideId, debug) {
    this._debug = debug;
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
    if (btnShowId) {
        this._btnShowId = btnShowId;
        this._btnShowObj = $('#' + this._btnShowId);
    }
    if (btnHideId) {
        this._btnHideId = btnHideId;
        this._btnHideObj = $('#' + this._btnHideId);
    }

    let _this = this;
    $('#'+_this._containerId + ' div.float-right > ul.nav > li > button.close[role="close"]').click(function() {
        // hide console
        _this.hide();
    });
    $('#'+_this._containerId + ' div.float-right > ul.nav > li > button.close[role="reduce"]').click(function() {
        // increase console height
        _this._containerObj.css('height', '100px');
        _this._compensedObj.css('margin-bottom', '100px');
        $('#docBtnScrollTop').css('bottom', '105px');

        $(this).css('margin-bottom', '0');

    });
    $('#'+_this._containerId + ' div.float-right > ul.nav > li > button.close[role="increase"]').click(function() {
        // increase console height
        _this._containerObj.css('height', '+=30px');
        _this._contentObj.css('height', '+=30px');
        _this._compensedObj.css('margin-bottom', '+=30px');
        $('#docBtnScrollTop').css('bottom', '+=30px');

        $('#'+_this._containerId + ' div.float-right > ul.nav > li > button.close[role="reduce"]').css('margin-bottom', '+=30px');
    });
    $('#'+this._containerId + ' div.float-right > ul.nav > li > button.close[role="decrease"]').click(function() {
        let _consoleHeight = _this._containerObj.height();
        // decrease console height
        if  (_consoleHeight > 100) {
            _this._containerObj.css('height', '-=30px');
            _this._contentObj.css('height', '-=30px');
            _this._compensedObj.css('margin-bottom', '-=30px');
            $('#docBtnScrollTop').css('bottom', '-=30px');

            $('#'+_this._containerId + ' div.float-right > ul.nav > li > button.close[role="reduce"]').css('margin-bottom', '-=30px');
        }
    });
    this._btnShowObj.click(function() {
        _this.show();
    });
    this._btnHideObj.click(function() {
        _this.hide();
    });

    if (this._useConsole) {
        if (this._useUI) {
            this.show();
        }
        this._debug.info('Console is ready.');
    }
};

Console.show = function() {
    this._containerObj.show();
    let _consoleHeight = this._containerObj.height();
    this._compensedObj.css('margin-bottom', '+=' + _consoleHeight + 'px');
    $('#docBtnScrollTop').css('bottom', '+=' + _consoleHeight + 'px');

    this._btnShowObj.hide();
    this._btnHideObj.show();
};

Console.hide = function() {
    this._containerObj.hide();
    let _consoleHeight = this._containerObj.height();
    this._compensedObj.css('margin-bottom', '-=' + _consoleHeight + 'px');
    $('#docBtnScrollTop').css('bottom', '-=' + _consoleHeight + 'px');

    this._btnShowObj.show();
    this._btnHideObj.hide();
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
            this._contentObj.html(_html);
        }

    }
};

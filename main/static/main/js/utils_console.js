

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


/* PUBLIC */


/* Configuration */
Console.useConsole = false;

Console._eContainer = null;
Console._eContent = null;

Console.setElementContainer = function(element) {
    this._eContainer = element;
};

Console.setElementContent = function(element) {
    this._eContent = element;
};

Console.useStdOutput = function(show) {
     this._useStd = (show !== false);
};

Console.useUIOutput = function(show) {
    this._useUI = (show !== false);
};


/* Exploitation */
Console.init = function() {
    if (this.useConsole) {

        if (this._useUI) {

            // todo : adapt css to the console height

            this._eContainer.show();
        }
        this.log('Console is ready.')
    }
};
Console.log = function(message) {
    if (this.useConsole) {
        if (this._useStd) {
            console.log(message);
        }

        if (this._useUI) {
            let _html;
            _html = this._eContent.html();
            if (_html !== '') {
                _html += '<br />';
            }
            _html += message;
            console.log(_html);
            this._eContent.html(_html);
        }
    }
};


/* PRIVATE */

Console._useStd = true;
Console._useUI = false;

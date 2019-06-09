/* Debug
*
* Exposes tools to manage debug features such as:
*   - easy storage of ajax calls (url and return parameters
*   - easy tool to store debug data
*   - easy access to stored data
*   - management of debugging level (debug/info/warning/error)
*   - capacity to export stored errors
*
* */
const Debug = Object();

const DebugLevels = Object();
DebugLevels.VERBOSE = 0;
DebugLevels.DEBUG = 1;
DebugLevels.INFO = 2;
DebugLevels.WARNING = 3;
DebugLevels.ERROR = 4;

class AjaxCall {
    constructor(url, postData) {
        this.url = url;
        this.postData = postData;
        this.xhr = null;
        this.status = null;
        this.data = null;
    }
    setResult(xhr, status, data) {
        this.xhr = xhr;
        this.status = status;
        this.data = data;
    }
    reprCall() {
        let _res = '';

        if (!this.postData) {
            _res += 'GET: ' + this.url;
        } else {
            _res += 'POST: ' + this.url + ' ';
            _res += this._repr_postData();
        }
        return _res;
    }
    reprResult() {
        let _url = this.url + ' : ' + this.status + ' (' + this.xhr.status + ')';
        if (!this.postData) {
            return 'GET ' + _url;
        } else {
            return 'POST ' + _url;
        }
    }
    repr() {
        let _url = this.url + ' : ' + this.status + ' (' + this.xhr.status + ')';
        let _res = '';
        if (!this.postData) {
            _res += 'GET ' + _url;
        } else {
            _res += 'POST ' + _url + ' ';
            _res += this._repr_postData();
        }

        return _res;
    }
    _repr_postData() {
        let _res = '';
        if (this.postData) {
            let _idx = 0;
            for (let _postDataKey of Object.keys(this.postData)) {
                if (_idx > 0) {
                    _res += ', ';
                }
                _res += _postDataKey + '=' + this.postData[_postDataKey];
                _idx += 1;
            }
        }
        return _res;
    }
}


/* PRIVATE */

Debug._useDebug = false;
Debug._console = null;
Debug._level = DebugLevels.DEBUG;
Debug._storage = {};

/* PUBLIC */

/* Configuration */


/* Initialization */

Debug.initialize = function(console, level) {
    this._console = console;
    this._level = level;
    this._storage['_ajax'] = [];
};


/* Exploitation */

/* Loggers */
Debug.verbose = function(message) {
    if (this._level <= DebugLevels.VERBOSE) {
        this._console.log('V: ' + message);
    }
};
Debug.debug = function(message) {
    if (this._level <= DebugLevels.DEBUG) {
        this._console.log('D: ' + message);
    }
};
Debug.info = function(message) {
    if (this._level <= DebugLevels.INFO) {
        this._console.log('I: ' + message);
    }
};
Debug.warning = function(message) {
    if (this._level <= DebugLevels.WARNING) {
        this._console.log('W: ' + message);
    }
};
Debug.error = function(message) {
    if (this._level <= DebugLevels.ERROR) {
        this._console.log('E: ' + message);
    }
};

/* Storage */
Debug.store = function(keyName, value) {
    this._storage[keyName] = value;
};

Debug.getStoredKeys = function() {
    let _keys = [];
    for (let _key of this._storage) {
        _keys.append(_key);
    }
    return _keys;
};

Debug.get = function(keyName) {
    return this._storage[keyName];
};

Debug.storeAjaxCall = function(url, postData) {
    let _ajaxCall = new AjaxCall(url, postData);
    this.debug('AjaxCall:' + _ajaxCall.reprCall() + ' ...');
    this._storage._ajax.push(_ajaxCall);

};

Debug.storeAjaxResult = function(url, xhr, status, data) {
    let _ajaxCall;
    for (_ajaxCall of this._storage._ajax) {
        if (_ajaxCall.url === url) {
            _ajaxCall.setResult(xhr, status, data);
            this.debug('AjaxCall:' + _ajaxCall.reprResult());
        }
    }
};

Debug.getAjaxErrors = function() {
    let _ajaxCalls = [];
    for (let _ajaxCall of this._storage._ajax) {
        if (_ajaxCall.status === 'error') {
            _ajaxCalls.append(_ajaxCall);
        }
    }
    return _ajaxCalls;
};

Debug.getLastAjaxCall = function() {
    return this._storage._ajax[this._storage._ajax.length - 1];
};

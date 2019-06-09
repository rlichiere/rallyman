
function loadElementContentFromUrl(elem_id, url) {
    let elem = $('#' + elem_id);
    elem.html('');
    Debug.storeAjaxCall(url);
    $.ajax({
        url: url,
        success: function(data, status, xhr) {
            Debug.storeAjaxResult(url, xhr, status, data);
            elem.html(data);
        },
        error: function(xhr, status, data) {
            Debug.storeAjaxResult(url, xhr, status, data);
            elem.html(data);
        }
    });
}

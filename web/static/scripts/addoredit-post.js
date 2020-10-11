
document.querySelector("textarea").addEventListener('keydown',function(e) {
    e = e||window.event // IE support
    var c = e.keyCode
    var ctrlDown = e.ctrlKey||e.metaKey // Mac support

    if(c === 9) { // tab was pressed
        // get caret position/selection
        var start = this.selectionStart;
        var end = this.selectionEnd;

        var target = e.target;
        var value = target.value;

        // set textarea value to: text before caret + tab + text after caret
        target.value = value.substring(0, start)
                    + "\t"
                    + value.substring(end);

        // put caret at right position again (add one for the tab)
        this.selectionStart = this.selectionEnd = start + 1;

        // prevent the focus lose
        e.preventDefault();
    }
    else if(c === 83 && ctrlDown) {
        document.forms["post"].submit();

        e.preventDefault();
    }
}, false);

key('⌘+s, ctrl+s', function(event, handler){
    console.log(handler.shortcut, handler.scope);

    document.forms["post"].submit();

    return false;
});

/* TopScroller
*
*   This class manages a scrolling to top with given button.
*
*   Constructor:
*       - `btn_scroller_id` <str> : Unique identifier of the button which should scroll to top when clicked.
*       - `configuration`   <dict>: configurtaion
* */
class TopScroller {

    constructor(btn_scroller_id, options) {
        this.btnScrollTopId = btn_scroller_id;
        this.btnScrollTop = $('#' + this.btnScrollTopId);
        this.animationIsRunning = false;

        this.scrollDuration = options.scrollDuration || 100;
        this.showBtnDuration = options.showBtnDuration || 100;
        this.hideBtnDuration = options.hideBtnDuration || 100;

        this._rootElements = options.root || $('html, body');
    }

    listenEvents() {
        let _this = this;

        this.btnScrollTop.click(function() {
            _this.scrollToTop();
        });

        window.onscroll = function() {
            _this.windowScrolls();
        };
    }

    /* Listens `window.onscroll`:
    *   Toggle the scrolling button visibility according to the document scroll information
    * */
    windowScrolls() {

        // skip when scroll animation is not finished
        if (this.animationIsRunning) {
            return;
        }

        // toggle scrolling button visibility according to scroll information
        if (document.body.scrollTop > 1 || document.documentElement.scrollTop > 1) {
            if (this.btnScrollTop.css('display') === 'none') {
                this.btnScrollTop.show(this.showBtnDuration);
            }
        } else {
            if (this.btnScrollTop.css('display') === 'block') {
                this.btnScrollTop.hide(this.hideBtnDuration);
            }
        }
    }

    /* Scroll window to top during the time allotted
    * */
    scrollToTop() {
        this.animationIsRunning = true;
        this.btnScrollTop.hide(this.hideBtnDuration);

        let _this = this;
        this._rootElements.animate({scrollTop : 0}, this.scrollDuration, function() {
            _this.animationIsRunning = false;
        });
    }

}


/* AnchorsScroller
*
*   This class adds an scroll animation on all anchored links in the page.
*
*   Constructor:
*       - `scroll_duration` <int>: Duration of the scroll. Milliseconds.
*
*   Example of anchored link:
*       <a href="#SomeAnchor">SomeLabel</a>
*
*   By contrast, below examples are not concerned:
*       <a href="#">SomeLabel</a>
*       <a href="https://domain.tld">SomeLabel</a>
*       <a href="https://domain.tld#SomeAnchor">SomeLabel</a>
* */
class AnchorsScroller {

    constructor(options) {
        this.scrollDuration = options.scrollDuration || 100;
        this.root = options.root || $('html, body');
    }

    /* Listens clicks on anchored links:
        Animate the scroll of a clicked anchored link with a duration
    * */
    listenEvents() {
        let _this = this;
        $('a[href^="#"]').click(function () {

            // skip links which have 'empty' (i.e '#') href
            let _href = $(this).attr('href');
            if (_href === '#') return true;

            if (!$(this).hasClass('.dropdown-toggle')) return true;

            // scroll to target with a duration
            _this.animateScroll(this);

            return true;
        });
    }

    /* Animate scroll during the time allotted
    * */
    animateScroll(obj) {
        this.root.animate({
            scrollTop: $('[name="' + $.attr(obj, 'href').substr(1) + '"]').offset().top
        }, this.scrollDuration);
    }
}

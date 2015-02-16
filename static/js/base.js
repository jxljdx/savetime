function isHomepage() {
    var url = location.href;
    var domain = location.origin;

    // Delete anchor at the end of url, and remove slashes for both url
    // and domain, check if the modified url is the same as modified
    // domain, if they are, current page is the homepage.
    url = url.substring(0, url.indexOf("#")).split("/").join("");
    domain = domain.split("/").join("");
    if (url == domain) {
        return true;
    }

    return false;
}

$(document).ready(function() {
    // Hack: align search button with search input box in Firefox
    if (navigator.userAgent.indexOf("Firefox") != -1 ) {
        $("div#search input[type=button]").css("top", "-2px");
    }

    $searchDiv = $("div#search");
    $(".header-menu-item.search-item").click(function() {
        $searchDiv.slideToggle();
    });

    // Only when the home page is requested, we show the search div by default
    if (!isHomepage()) {
        $searchDiv.css("display", "none");
    }
});

/*
 * [ Alternative entry UI for search and categorization ]
 *

var animated = false;

$(document).ready(function() {

    $(".header-menu-item#search").hover(function() {
        if (!animated) {
            animated = true;

            var container = this;
            var input = $(this).find("input");
            var categoriesDiv = $(this).find("div.categories");
            var widthToAddForContainer = 200;
            var widthToAddForInput = 200;

            if (navigator.userAgent.indexOf("Firefox") != -1 ) {
                var inputPaddingLeft = $(input).css("padding-left");
                widthToAddForInput -= inputPaddingLeft.substring(0, inputPaddingLeft.indexOf("px"));
            }

            $(container).css("height", "93px");

            $(container).animate({
                width: "+=" + widthToAddForContainer + "px",
                padding: "10px"
            });

            $(input).animate({
                width: "+=" + widthToAddForInput + "px"
            });

            $(categoriesDiv).animate({
                opacity: 1
            }, "easeOutBack", function() {
                $(container).css("box-shadow", "0 0 2px 2px #888");
                $(container).css("background-color", "#fff");

                // Focus input
                $(input).focus();
            });
        }
    });

    $(".header-menu-item#search").focusout(function() {
        if (animated) {
            animated = false;

            var container = this;
            var input = $(this).find("input");
            var categoriesDiv = $(this).find("div.categories");
            var widthToDecrementForContainer = 200;
            var widthToDecrementForInput = 200;

            if (navigator.userAgent.indexOf("Firefox") != -1 ) {
                var inputPaddingLeft = $(input).css("padding-left");
                widthToDecrementForInput -= inputPaddingLeft.substring(0, inputPaddingLeft.indexOf("px"));
            }

            $(container).css("box-shadow", "0 0 2px 2px #fff");

            $(categoriesDiv).animate({
                opacity: 0
            });

            $(input).animate({
                width: "-=" + widthToDecrementForInput + "px"
            });

            $(container).animate({
                width: "-=" + widthToDecrementForContainer + "px",
                padding: "0px"
            }, function() {
                $(container).css("height", "40px");
            });
        }
    });
});

*/
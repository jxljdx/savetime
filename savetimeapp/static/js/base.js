function isHomepage() {
    var url = location.href;
    var domain = location.origin;

    // Delete anchor at the end of url, and remove slashes for both url
    // and domain, check if the modified url is the same as modified
    // domain, if they are, current page is the homepage.
    if (url.indexOf("#") != -1) {
        url = url.substring(0, url.indexOf("#"));
    }
    url = url.split("/").join("");
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
function getRamdomDarkColor() {
    var r = Math.round(Math.random() * 128 + 32);
    var g = Math.round(Math.random() * 128 + 32);
    var b = Math.round(Math.random() * 128 + 32);
    return [r, g, b];
}

$(document).ready(function() {
    _hmt.push(['_trackPageview', "/categories"]);

    $("span.sub-category").each(function() {
        var rgb = getRamdomDarkColor();
        $(this).css("background", "rgb(" + rgb[0] + ", " + rgb[1] + ", " + rgb[2] + ")");
    });

    $("span.sub-category").click(function() {
        var keyword = $(this).text();
        isSearchingCategory = true;
        _hmt.push(['_trackPageview', '/search/category']);
        search(keyword);
    });
});
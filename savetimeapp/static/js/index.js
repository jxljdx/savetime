var MONTHS = ["一月", "二月", "三月", "四月", "五月", "六月",
              "七月", "八月", "九月", "十月", "十一月", "十二月"];
var WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"];
var TODAY = "今天";
var YESTERDAY = "昨天";
var DOMAIN = "http://127.0.0.1:8000";
var BUTTON_HTML = "<div class=\"button load-more-button\">更多</div>";

function loadMore() {
    // Number of items we want to load for each request
    var NUM_ITEMS = 100;
    // Number of items in page so far
    var num_items_so_far = $(".savetime-item").length;
    var request_url = DOMAIN + "/items/" + NUM_ITEMS + "/" + num_items_so_far;

    $.ajax({
        url: request_url,
        success: function( data ) {
            onLoadMoreSuccess(data);
        }
    });
}

function onLoadMoreSuccess(data) {
    // Get last posts section's date, it is save in the custom attribute "data-date-time"
    var last_posts_section_date_value = $(".posts").last().attr("data-date-time");
    var last_posts_section_date;
    if (last_posts_section_date_value !== undefined && last_posts_section_date_value !== null) {
        var date = last_posts_section_date_value.split("-");
        last_posts_section_date = new Date();
        last_posts_section_date.setFullYear(date[0], date[1], date[2]);
    }

    // Add save time item one onto page
    for (var i = 0; i < data.length; i++) {
        var item = data[i];
        var item_date = dateStrToDateObj(item["created_at"]);

        // Add a new posts section if there is none or if the new save time item has different date
        // than last posts section date.
        if (last_posts_section_date === undefined || last_posts_section_date === null ||
                item_date.getFullYear() != last_posts_section_date.getFullYear() ||
                item_date.getMonth() != last_posts_section_date.getMonth() ||
                item_date.getDate() != last_posts_section_date.getDate()) {

            appendSection(item_date);

            // Update last posts section's date
            last_posts_section_date = new Date();
            last_posts_section_date.setFullYear(
                    item_date.getFullYear(), item_date.getMonth(), item_date.getDate());
        }

        // Add a new save time item to the last posts section
        appendItemToSection(item);

        reappendLoadMoreButton();
    }
}

// Posts sections are always appended to the end of #content div, but we want to have have the
// load more button at the end of #content div, so after done appending posts sections, reappend
// the load more button.
function reappendLoadMoreButton() {
    // $(".button-wrapper").remove();
    $(".load-more-button").remove();
    $("#content").append(BUTTON_HTML);
}

// Appends a new posts section to content
function appendSection(date) {
    var weekday = WEEKDAYS[date.getDay()];
    if (isToday(date)) weekday = TODAY;
    else if (isYesterday(date)) weekday = YESTERDAY;

    // var datetime1 = MONTHS[date.getMonth()] + " " + date.getDate() + ", " + date.getFullYear();
    var datetime1 = date.getFullYear() + "/" + (date.getMonth() + 1) + "/" + date.getDate();
    var datetime2 = date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate();
    $("#content").append(
        "<section class=\"posts\" data-date-time=\"" + datetime2 + "\">" +
            "<div class=\"posts-date row\">" +
                "<h4 class=\"posts-date-weekday\">" + weekday + "</h4>" +
                "<span class=\"posts-date-time\">" + datetime1 + "</span>" +
            "</div><ul></ul>" +
        "</section>"
    );
}

// Appends a new save time item to the last posts section's <ul> portion
function appendItemToSection(item) {
    $("ul").last().append(
        "<li class=\"savetime-item\" data-item-id=\"" + item.id + "\">" +
            "<div class=\"upvote\">" +
                "<a href=\"#\" class=\"upvote-link\"></a>" +
                "<span class=\"upvote-count\">" + item["num_likes"] + "</span>" +
            "</div>" +
            "<div class=\"desc\">" +
                "<a class=\"item-url\" href=\"" + item["url"] + "\">" + item["title"] + "</a>" +
                "<span class=\"item-tagline\">" + item["desc"] + "</span>" +
            "</div>" +
        "</li>"
    );
}

// Retrieved date time string's format is Year-month-day-hour-minute-second-serverTimezone
function dateStrToDateObj(date_str) {
    if (date_str !== undefined && date_str !== null) {
        var date = date_str.split("-");
        // For Javascript's Date object, the month is in the range of 0 to 11 instead of 1 to 12,
        // we have to explictly decrement the month by 1 here.
        return new Date(Number(date[0]), Number(date[1]) - 1, Number(date[2]),
                        Number(date[3]), Number(date[4]), Number(date[5]), 0);
    }
}

// Checks if the given date is today
function isToday(date) {
    var today = new Date();
    return date.getFullYear() == today.getFullYear() &&
           date.getMonth() == today.getMonth() &&
           date.getDate() == today.getDate();
}

// Checks if the given date is yesterday
function isYesterday(date) {
    var today = new Date();
    var yesterday = new Date();
    yesterday.setDate(today.getDate() - 1);
    return date.getFullYear() == yesterday.getFullYear() &&
           date.getMonth() == yesterday.getMonth() &&
           date.getDate() == yesterday.getDate();
}

// Send a request to increment num_likes of a item, the given upvote_link is the <a> element
// belonging to the savetime item
function likeItem(upvote_link) {
    // Find the id of the savetime item from <li> element's data-item-id attribute
    var item_id = upvote_link.closest("li").attr("data-item-id");
    var request_url = DOMAIN + "/item/" + item_id + "/like";
    $.ajax({
        url: request_url,
        success: function (data) {
            if (data["msg"] == "success") {
                var item_num_likes_ele = upvote_link.closest("li").find(".upvote-count");
                item_num_likes_ele.text(Number(item_num_likes_ele.text()) + 1);
            }
        }
    });
}

$(document).ready(function(){
    // Load the first batch of save time items
    loadMore();

    $("#content").on("click", "a.upvote-link", function(event) {
        event.preventDefault();
        // Refer to the clicked element using $(this) instead of this, so jquery can understand
        // what that is.
        likeItem($(this));
    });

    $("#content").on("click", ".load-more-button", function() {
        alert("还没有测试呢");
        loadMore();
    });
});
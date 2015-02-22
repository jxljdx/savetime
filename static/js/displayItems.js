/*
 * Displays savetime items in div content
 */

var MONTHS = ["一月", "二月", "三月", "四月", "五月", "六月",
              "七月", "八月", "九月", "十月", "十一月", "十二月"];
var WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"];
var TODAY = "今天";
var YESTERDAY = "昨天";
var DOMAIN = location.origin;
var BUTTON_HTML = "<div class=\"button load-more-button\">更多</div>";

var OrderByEnum = {
    TimeDecrease: 0,
    // TimeIncrease: 1 not supported yet or never will
    LikesDecrease: 1
    // LikesIncrease: 2 not supported yet or never will
}

// What order by method is being used for save time items on current page
var curOrderBy = OrderByEnum.TimeDecrease;
var inSearchMode = false;

function onLoadMoreSuccess(data) {
    if (curOrderBy == OrderByEnum.TimeDecrease) {
        // Get last posts section's date, it is save in the custom attribute "data-date-time"
        var last_posts_section_date_value = $(".posts").last().attr("data-date-time");
        var last_posts_section_date;
        if (last_posts_section_date_value !== undefined && last_posts_section_date_value !== null) {
            var date = last_posts_section_date_value.split("-");
            last_posts_section_date = new Date();
            last_posts_section_date.setFullYear(date[0], date[1], date[2]);
        }

        // Add save time item one by one onto page
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
            appendItem(item);

            reappendLoadMoreButton();
        }
    } else if (curOrderBy == OrderByEnum.LikesDecrease) {
        // Add save time item one by one onto page
        for (var i = 0; i < data.length; i++) {
            appendItem(data[i]);
        };

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

// Used only in order by time UI
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

// Used in order by time UI and order by likes UI
// Appends a new save time item to the last posts section's <ul> portion
function appendItem(item) {
    $("ul").last().append(
        "<li class=\"savetime-item\" data-item-id=\"" + item.id + "\" data-item-date-time=\"" + item["created_at"] + "\">" +
            "<div class=\"upvote\">" +
                "<a href=\"#\" class=\"upvote-link\"></a>" +
                "<span class=\"upvote-count\">" + item["num_likes"] + "</span>" +
            "</div>" +
            "<div class=\"desc\">" +
                "<a class=\"item-url\" target=\"_blank\" href=\"" + item["url"] + "\">" +
                        item["title"] + "</a>" +
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

// Returns back oldest item time from among all save time items.
function findOldestItemTime() {
    var oldest_item_time_str = "2200-01-01-01-01-00-UTC";
    var oldest_item_time = dateStrToDateObj(oldest_item_time_str);
    $(".savetime-item").each(function() {
        var item_time_str = $(this).attr("data-item-date-time");
        var item_time = dateStrToDateObj(item_time_str);
        if (oldest_item_time > item_time) {
            oldest_item_time = item_time;
            oldest_item_time_str = item_time_str;
        }
    });
    return oldest_item_time_str;
}

// Load more save times from server using keyword,
// keyword is only needed when loadMore request comes from search, in which
// case, inSearchMode is set to true.
function loadMore(keyword) {
    // Number of items we want to load for each request
    var NUM_ITEMS = 50;

    if (!inSearchMode) {
        var request_url = DOMAIN + "/items/before/" + NUM_ITEMS + "/" + findOldestItemTime();
        $.ajax({
            url: request_url,
            success: function( data ) {
                onLoadMoreSuccess(data);
            }
        });
    } else {
        if (keyword.length > 0) {
            var request_url = DOMAIN + "/search/items/" + keyword + "/before/" + NUM_ITEMS + "/" + findOldestItemTime();
            $.ajax({
                url: request_url,
                success: function( data ) {
                    if (data["msg"] == "success") {
                        onLoadMoreSuccess(data["data"]);
                    }
                }
            });
        } else {
            // TODO: Display an error msg
        }
    }
}

function search(keyword) {
    inSearchMode = true;
    curOrderBy = OrderByEnum.LikesDecrease;

    // Remove all the content in content div
    $("#content").empty();

    // Add a <ul> section in content div so we can append <li> elements in <ul>
    $("#content").append("<ul></ul>");

    loadMore(keyword);
}

$(document).ready(function(){
    // Load the first batch of save time items if this is the home page
    if (isHomepage()) {
        loadMore("");
    }

    $("#content").on("click", ".load-more-button", function() {
        var keyword = $("div#search input[type=text]").val();
        loadMore(keyword);
    });

    $("#content").on("click", "a.upvote-link", function(event) {
        event.preventDefault();
        // Refer to the clicked element using $(this) instead of this, so jquery can understand
        // what that is.
        likeItem($(this));
    });

    $("#content").on("mouseover", ".upvote", function(event) {
        $(this).find("a.upvote-link").css("border-bottom", "12px solid #EB4A10");
    });

    $("#content").on("mouseout", ".upvote", function(event) {
        $(this).find("a.upvote-link").css("border-bottom", "12px solid #534540");
    });

    $("#content").on("click", ".upvote", function(event) {
        likeItem($(this).find("a.upvote-link"));
    });

    $("div#search input[type=button]").click(function(event) {
        event.preventDefault();
        var keyword = $("div#search input[type=text]").val();
        search(keyword);
    });

    // Make on input enter, it behaves correctly
    $("div#search input[type=text]").keypress(function(event) {
        if (event.keyCode == 13) {
            event.preventDefault();
            var keyword = $("div#search input[type=text]").val();
            search(keyword);
        }
    });

    $("#cssmenu a").click(function(event) {
        event.preventDefault();
        var keyword = $(this).find("span").text();
        search(keyword);
    });
});
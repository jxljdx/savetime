// var DOMAIN = location.origin;
var animated = false;

$(document).ready(function() {
    // $(".header-menu-item#search").hover(function() {
    //     var onHoverSearchImgPath = DOMAIN + "/static/img/search_hover.png"
    //     $(this).find("img").attr("src", onHoverSearchImgPath);
    // }, function() {
    //     var searchImgPath = DOMAIN + "/static/img/search.png"
    //     $(this).find("img").attr("src", searchImgPath);
    // });

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

            // $(input).animate({
            //     width: "+=" + widthToAddForInput + "px"
            // }, function() {
            //     $(container).css("box-shadow", "0 0 2px 2px #888");
            //     $(container).css("height", "93px");
            //     $(container).css("background-color", "#fff");
            //     // $(container).animate({
            //     //     boxShadow: "0 0 2px 2px #888",
            //     //     height: "93px",
            //     //     backgroundColor: "#fff"
            //     // });

            //     $(categoriesDiv).animate({
            //         opacity: 1
            //     });

            //     // Focus input
            //     $(input).focus();
            // });
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
$(function () {
    var body = $('body');

    var query_input = $("#id_query");
    query_input.bind("focus", function () {
        $(this).select();
    });
    query_input.bind("mouseup", function () {
        return false;
    });

    body.on('click', '.vote-link', function () {
        var button = $(this);
        var url = button.attr('href');

        var parts = url.split('=');
        var srpk = parts[parts.length - 1];

        $.ajax({
            'url': url,
            'success': function (html) {
                if (html.length > 5) {
                    $("#scores-" + srpk).html(html);
                    refreshFullView();
                }

                button.parents('.search-result-social').find('a.vote-link').each(function () {
                    $(this).attr('disabled', 'disabled');
                });

                refreshMessages();
                refreshExperienceProgress();
            }
        });

        return false;
    });

    body.on('click', '.comment-add', function () {
        var icon = $(this).find('i');
        if (icon.hasClass('glyphicon-plus')) {
            icon.removeClass('glyphicon-plus').addClass('glyphicon-minus');
        } else {
            icon.removeClass('glyphicon-minus').addClass('glyphicon-plus');
        }
    });

    body.on('click', '.purchase-btn', function () {
        var button = $(this);
        var url = button.attr('href');

        var parts = url.split('=');
        var srpk = parts[parts.length - 1];

        $.ajax({
            'url': url,
            'success': function (html) {
                if (html.length > 5) {
                    $("#" + srpk).replaceWith(html);
                    refreshFullView();
                }

                refreshMessages();
                refreshBalance();
                refreshExperienceProgress();
            }
        });

        return false;
    });

    body.on('click', '.remove-offer-btn, .offer-accept-btn, .offer-decline-btn', function () {
        var button = $(this);
        var url = button.attr('href');

        $.ajax({
            'url': url,
            'success': function () {
                window.location.reload();
            }
        });

        return false;
    });

    body.on('click', '.report-comment-btn', function () {
        var button = $(this);
        var url = button.attr('href');

        $.ajax({
            'url': url,
            'success': function () {
                refreshMessages();
            }
        });

        return false;
    });

    body.on('click', '.favourite-btn', function () {
        var button = $(this);
        var url = button.attr('href');

        $.ajax({
            'url': url,
            'success': function () {
                var i = button.find('i');

                if (i.hasClass('fa-heart-o')) {
                    button.find('i').removeClass('fa-heart-o').addClass('fa-heart');
                } else {
                    button.find('i').removeClass('fa-heart').addClass('fa-heart-o');
                }
            }
        });

        return false;
    });

    $("#dock-bar").hover(function () {
        $(this).stop().animate({
            'margin-right': 0
        }, 200);
    }, function () {
        $(this).stop().animate({
            'margin-right': -120
        }, 200);
    });
});

function setUpMinimizedIframes()
{
    var cookieData = $.cookie("minimized-iframe-list");
    if (typeof (cookieData) == 'undefined') {
        return;
    }
    var minimizedIframeList = JSON.parse(cookieData);
    if (typeof (minimizedIframeList) != 'undefined') {
        var executed = false;
        $.each(minimizedIframeList, function (index, value) {
            executed = true;
            var obj = $(value);
            if (obj.length > 0) {
                openLinkInIframe(obj);
                minimizeIframe($("#iframe-row"));
            }
        });

        if (executed) {
            unlockScroll();
        }
    }
}

function openLinkInIframe(anchor)
{
    var rowDiv = $('<div class="row" id="iframe-row"></div>');
    var colDiv = $('<div class="col-md-10 col-sm-10 col-md-offset-1 col-sm-offset-1"></div>');

    var calculatedHeight = $(window).height() - 55;

    colDiv.height(calculatedHeight);

    var iframe = $('<iframe id="'+anchor.data('href')+'" src="'+anchor.attr('href')+'" data-src="'+anchor.data('href')+'" class="link-iframe"></iframe>');

    resizeIframe(iframe);

    $(window).on('resize', function () {
        resizeIframe(iframe);
    });

    var body = $('body');

    colDiv.append(iframe);
    rowDiv.append(colDiv);
    body.prepend(rowDiv);

    var navigationRow = $('<div class="row" id="navigation-row"></div>');
    var navigationCol = $('<div class="col-md-12 col-sm-12"></div>');
    var navigationWrapper = $('<div class="navigation-wrapper"></div>');
    var buttonGroup = $('<div class="btn-group pull-right"></div>');
    var clearFix = $('<div class="clearfix"></div>');

    var newWindowButton = $('<a href="#" class="btn btn-default" data-toggle="tooltip" data-placement="top" title="Open in new window"><i class="fa fa-external-link"></i></a>');
    newWindowButton.bind('click', function () {
        removeIframeCookie(iframe.data('src'));

        window.open(anchor.data('href'), '_blank');

        $("#iframe-row").remove();
        unlockScroll();

        return false;
    });

    var minimizeButton = $('<a href="#" class="btn btn-default" data-toggle="tooltip" data-placement="top" title="Minimize"><i class="fa fa-toggle-right"></i></a>');
    minimizeButton.bind('click', function () {
        minimizeIframe(rowDiv);

        unlockScroll();

        return false;
    });

    var closeButton = $('<a href="#" class="btn btn-default" data-toggle="tooltip" data-placement="top" title="Close"><i class="fa fa-close"></i></a>');
    closeButton.bind('click', function () {
        removeIframeCookie(iframe.data('src'));

        $("#iframe-row").remove();

        unlockScroll();

        return false;
    });

    buttonGroup.append(newWindowButton);
    buttonGroup.append(minimizeButton);
    buttonGroup.append(closeButton);

    var title = anchor.text().trim();
    var iframeTitle = $('<div class="iframe-title pull-left"></div>').html("<h3 class='iframe-title'>" + title + "</h3>");

    navigationWrapper.append(iframeTitle);
    navigationWrapper.append(buttonGroup);
    navigationWrapper.append(clearFix);
    navigationCol.append(navigationWrapper);
    navigationRow.append(navigationCol);

    colDiv.prepend(navigationRow);

    iframeTitle.width(navigationWrapper.width() - buttonGroup.width());

    lockScroll();
    body.tooltip({ selector: '[data-toggle="tooltip"]' });

    return false;
}

function removeIframeCookie(key)
{
    var cookieData = $.cookie("minimized-iframe-list");
    if (typeof (cookieData) != 'undefined') {
        var minimizedIframeList = JSON.parse(cookieData);
        if (typeof (minimizedIframeList) != 'undefined') {
            delete minimizedIframeList[key];
            $.cookie("minimized-iframe-list", JSON.stringify(minimizedIframeList));
        }
    }
}

function minimizeIframe(iframeDiv)
{
    var cookieData = $.cookie("minimized-iframe-list");
    if (typeof (cookieData) == 'undefined') {
        minimizedIframeList = {};
    } else {
        var minimizedIframeList = JSON.parse(cookieData);
        if (typeof (minimizedIframeList) == 'undefined' || minimizedIframeList.length == 0) {
            minimizedIframeList = {};
        }
    }

    var iframeSource = iframeDiv.find('iframe').data('src');
    var anchor = $('a[data-href="' + iframeSource + '"]');
    var anchorHtml = anchor.wrap('<span/>').parent().html();
    if ($.inArray(anchorHtml, minimizedIframeList) < 0) {
        minimizedIframeList[anchor.data('href')] = anchorHtml;
    }
    anchor.unwrap();
    $.cookie("minimized-iframe-list", JSON.stringify(minimizedIframeList));

    iframeDiv.data('id', iframeDiv.attr('id')).removeAttr('id');
    iframeDiv.hide();

    var link = $('<a href="#" class="btn btn-default"></a>');
    link.text(iframeDiv.find('h3.iframe-title').text());

    link.bind('click', function () {
        if ($('#iframe-row').length > 0) {
            minimizeIframe($("#iframe-row"));
        }

        iframeDiv.attr('id', iframeDiv.data('id')).removeData('id');
        iframeDiv.show();

        link.remove();

        return false;
    });

    $("#dock-bar").find('.dock-item-group').append(link);
}

function resizeIframe(iframe)
{
    var calculatedHeight = $(window).height() - 55;
    iframe.height(calculatedHeight - 40);
}

var $html, $body;

function lockScroll(){
    $html = $('html');
    $body = $('body');
    var initWidth = $body.outerWidth();
    var initHeight = $body.outerHeight();

    var scrollPosition = [
        self.pageXOffset || document.documentElement.scrollLeft || document.body.scrollLeft,
        self.pageYOffset || document.documentElement.scrollTop  || document.body.scrollTop
    ];
    $html.data('scroll-position', scrollPosition);
    $html.data('previous-overflow', $html.css('overflow'));
    $html.css('overflow', 'hidden');
    window.scrollTo(scrollPosition[0], scrollPosition[1]);

    var marginR = $body.outerWidth()-initWidth;
    var marginB = $body.outerHeight()-initHeight;
    $body.css({'margin-right': marginR,'margin-bottom': marginB});
}

function unlockScroll(){
    $html = $('html');
    $body = $('body');
    $html.css('overflow', $html.data('previous-overflow'));
    var scrollPosition = $html.data('scroll-position');
    window.scrollTo(scrollPosition[0], scrollPosition[1]);

    $body.css({'margin-right': 0, 'margin-bottom': 0});
}

function refreshExperienceProgress()
{
    $.ajax({
        'url': '/user/get-experience/',
        'success': function (html) {
            if (html.length > 5) {
                $("#experience-progress").html(html);
            }
        }
    });
}

function refreshMessages()
{
    $.ajax({
        'url': '/flash-messages/',
        'success': function (html) {
            $("#message-affix").html(html);
        }
    });
}

function refreshBalance()
{
    $.ajax({
        'url': '/user/get-balance/',
        'success': function (balance) {
            $("#balance").text(balance);
        }
    });
}

function refreshFullView()
{
    var srpk = $("#item-full-view").data('srpk');
    $.ajax({
        'url': '/load-item/',
        'data': {
            'srpk': srpk
        },
        'success': function (html) {
            $("#item-full-view").replaceWith(html);
        }
    });
}

function commentFormSubmit(form) {
    $.ajax({
        'url': form.attr('action'),
        'type': 'post',
        'data': form.serialize(),
        'success': function (html) {
            if (html.length > 0) {
                var srpk = form.find('input[name="srpk"]').val();
                $("#comment-list-" + srpk).html(html);
                form.find('textarea[name="comment_text"]').val('');
            }

            refreshMessages();
            refreshFullView();
            refreshExperienceProgress();
        }
    });

    return false;
}

function makeOfferFormSubmit(form) {
    $.ajax({
        'url': form.attr('action'),
        'type': 'post',
        'data': form.serialize(),
        'success': function () {
            form.find('#amount').val('');

            refreshMessages();
        }
    });

    return false;
}

function makeHref(anchor) {
    anchor.attr('href', anchor.data('href'));
}
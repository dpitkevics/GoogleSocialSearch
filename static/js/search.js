$(function () {
    var body = $('body');

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
});

function openLinkInIframe(anchor)
{
    var rowDiv = $('<div class="row" id="iframe-row"></div>');
    var colDiv = $('<div class="col-md-10 col-sm-10 col-md-offset-1 col-sm-offset-1"></div>');

    var calculatedHeight = $(window).height() - 125;

    colDiv.height(calculatedHeight);

    var iframe = $('<iframe src="'+anchor.attr('href')+'" class="link-iframe"></iframe>');
    resizeIframe(iframe);

    $(window).on('resize', function () {
        resizeIframe(iframe);
    });

    var body = $('body');

    colDiv.append(iframe);
    rowDiv.append(colDiv);
    body.prepend(rowDiv);

    var navigationRow = $('<div class="row" id="navigation-row"></div>');
    var navigationCol = $('<div class="col-md-10 col-sm-10 col-md-offset-1 col-sm-offset-1"></div>');
    var buttonGroup = $('<div class="btn-group"></div>');
    var closeButton = $('<a href="#" class="btn btn-default">Close</a>');
    closeButton.bind('click', function () {
        $("#iframe-row").remove();

        unlockScroll();

        return false;
    });

    buttonGroup.append(closeButton);
    navigationCol.append(buttonGroup);
    navigationRow.append(navigationCol);

    colDiv.prepend(navigationRow);

    lockScroll();

    return false;
}

function resizeIframe(iframe)
{
    var calculatedHeight = $(window).height() - 125;
    iframe.height(calculatedHeight - 40);
}

function lockScroll(){
    var $html = $('html');
    var $body = $('body');
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
    var $html = $('html');
    var $body = $('body');
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
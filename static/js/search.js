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

function makeHref(anchor) {
    anchor.attr('href', anchor.data('href'));
}
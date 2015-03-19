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
                }

                button.parents('.search-result-social').find('a.vote-link').each(function () {
                    $(this).attr('disabled', 'disabled');
                });
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
});

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
        }
    });

    return false;
}

function makeHref(anchor) {
    anchor.attr('href', anchor.data('href'));
}
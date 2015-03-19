$(function () {
    $('body').on('click', '.vote-link', function () {
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
});
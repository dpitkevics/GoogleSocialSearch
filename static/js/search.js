$(function () {
    $('body').on('click', '.vote-link', function () {
        var button = $(this);
        var url = button.attr('href');

        $.ajax({
            'url': url,
            'success': function () {
                button.parents('.search-result-social').find('a.vote-link').each(function () {
                    $(this).attr('disabled', 'disabled');
                });
            }
        });

        return false;
    });
});
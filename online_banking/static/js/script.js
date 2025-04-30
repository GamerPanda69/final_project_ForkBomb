$(document).ready(function() {
    $('.tool-btn').click(function() {
        var toolId = $(this).data('tool');
        $('.tool-form').not('#' + toolId).slideUp();
        $('#' + toolId).slideToggle();
    });

    $('a.nav-link, a.btn').click(function(e) {
        e.preventDefault();
        var href = $(this).attr('href');
        $('.container').removeClass('slide-in').fadeOut(300, function() {
            window.location.href = href;
        });
    });
});
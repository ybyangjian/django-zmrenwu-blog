$(function () {
    // search
    $('#js-search-btn').on('click', function (e) {
        $('#js-search-musk').fadeIn(300);
        $('#search-form').removeClass('hide-on-mobile').addClass('show-on-mobile').find('input').focus();
        e.preventDefault();
    });

    $('#js-search-musk').on('click', function (e) {
        $(this).fadeOut(300);
        $('#search-form').removeClass('show-on-mobile').addClass('hide-on-mobile');
    });

    // sidebar
    $('#js-sidebar-btn').on('click', function (e) {
        $('.toc-sidebar').animate({'left': 0}, 300);
        $('#js-sidebar-musk').fadeIn(300);
        e.preventDefault();
    });

    $('#js-sidebar-musk').on('click', function (e) {
        $('.toc-sidebar').animate({'left': '-70%'}, 300);
        $(this).fadeOut(300);
    });

    // back top
    $('#js-back-top').on('click', function (e) {
        if ($(window).scrollTop() > 0 && !$('html,body').is(':animated')) {
            $('html,body').animate({scrollTop: 0}, 500);
        }
        e.preventDefault();
    });

    $(window).on('scroll', function (e) {
        var $pos = $(window).height() / 2;
        if ($(window).scrollTop() > $pos) {
            $('#js-back-top').fadeIn();
        } else {
            $('#js-back-top').fadeOut();
        }
    });

    // donate
    $('#js-weixin-btn').on('click', function (e) {
        $('#alipay').hide();
        $('#weixin').show();
        e.preventDefault();
    });

    $('#js-alipay-btn').on('click', function (e) {
        $('#weixin').hide();
        $('#alipay').show();
        e.preventDefault();
    });
});

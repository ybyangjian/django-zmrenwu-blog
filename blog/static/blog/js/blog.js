$(function () {
    // search form
    $('#js-search-btn').on('click', function (e) {
        var $musk = $('#search-musk');
        var $searchForm = $('#search-form');

        if ($musk.length === 0) {
            // Musk does not exist, create it.
            $musk = $('<div></div>')
                .addClass('musk')
                .attr('id', 'search-musk')
                .appendTo($searchForm)
                .click(function () {
                    $searchForm.slideUp();
                    $(this).fadeOut();
                });
        }

        $searchForm.removeClass('hide-on-mobile')
            .hide().slideDown()
            .find('input')
            .focus();
        $musk.fadeIn();

        return false;
    });

    // sidebar
    $('#js-sidebar-btn').on('click', function (e) {
        var $musk = $('#sidebar-musk');
        var $sideBar = $('.toc-sidebar');

        if ($musk.length === 0) {
            // Musk does not exist, create it.
            $musk = $('<div></div>')
                .addClass('musk')
                .attr('id', 'sidebar-musk')
                .css('z-index', 1)
                .appendTo('body')
                .click(function () {
                    $(this).fadeOut(500);
                    $sideBar.animate({'left': '-70%'}, 500);
                });
        }
        $sideBar.animate({'left': 0}, 500);
        $musk.fadeIn(500);
        return false;
    });

    // back top
    var $backTop = $('.back-top');

    if ($backTop.length === 0) {
        // Button back top does not exist, create it.
        $backTop = $('<a href="#" class="back-top"><i class="fa fa-arrow-up" aria-hidden="true"></i></a>')
            .appendTo('body')
            .click(function (e) {
                if ($(window).scrollTop() > 0 && !$('html,body').is(':animated')) {
                    $('html,body').animate({scrollTop: 0}, 500);
                }
                return false
            });
    }

    $(window).on('scroll', function (e) {
        var $pos = $(window).height() / 2;
        if ($(window).scrollTop() > $pos) {
            $backTop.fadeIn();
        } else {
            $backTop.fadeOut();
        }
    });

    // reward
    $('#js-reward').click(function () {
        var $this = $(this);
        $this.next().slideToggle()
    })
});

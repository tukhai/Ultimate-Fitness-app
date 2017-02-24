"use strict";


// Prealoder
function prealoader() {
    if ($('#loader').length) {
        $('#loader').fadeOut(); // will first fade out the loading animation
        $('#loader-wrapper').delay(350).fadeOut('slow'); // will fade out the white DIV that covers the website.
        $('body').delay(350).css({ 'overflow': 'visible' });
    };
}

// Banner rev Slider 
function mainBanner() {
    if ($("#banner").length) {
        $("#main_slider").revolution({
            sliderType: "standard",
            sliderLayout: "auto",
            loops: false,
            delay: 7500,
            navigation: {
                keyboardNavigation: "off",
                keyboard_direction: "horizontal",
                mouseScrollNavigation: "off",
                onHoverStop: "on",
                touch: {
                    touchenabled: "on",
                    swipe_threshold: 75,
                    swipe_min_touches: 1,
                    swipe_direction: "horizontal",
                    drag_block_vertical: false
                },
                arrows: {
                    style: "hephaistos",
                    enable: true,
                    hide_onmobile: false,
                    hide_onleave: false,
                    tmp: '<div class="arrow-holder"> </div>',
                    left: {
                        h_align: "left",
                        v_align: "center",
                        h_offset: 28,
                        v_offset: 32
                    },
                    right: {
                        h_align: "right",
                        v_align: "center",
                        h_offset: 43,
                        v_offset: 32
                    }
                },
                bullets: {
                    style: "hephaistos",
                    enable: true,
                    hide_onmobile: false,
                    hide_onleave: false,
                    h_align: "center",
                    v_align: "bottom",
                    space: 10,
                    v_offset: 30
                },
            },
            responsiveLevels: [2220, 1183, 975, 751],
            gridwidth: [1170, 970, 770, 480],
            gridheight: [700, 700, 700, 500],
            lazyType: "none",
            parallax: {
                type: "mouse",
                origo: "slidercenter",
                speed: 2000,
                levels: [2, 3, 4, 5, 6, 7, 12, 16, 10, 50],
            },
            shadow: 0,
            spinner: "off",
            stopLoop: "off",
            stopAfterLoops: -1,
            stopAtSlide: -1,
            shuffle: "off",
            autoHeight: "off",
            hideThumbsOnMobile: "off",
            hideSliderAtLimit: 0,
            hideCaptionAtLimit: 0,
            hideAllCaptionAtLilmit: 0,
            debugMode: false,
            fallbacks: {
                simplifyAll: "off",
                nextSlideOnWindowFocus: "off",
                disableFocusListener: false,
            }
        });
    };
}




function countryInfo() {
    if ($('.area_select').length) {
        $('.area_select').change(function() {
            var val = $(this).val();
            if (val) {
                $('.state:not(#value' + val + ')').slideUp();
                $('#value' + val).slideDown();
            } else {
                $('.state').slideDown();
            }
        });
    }
}



// Select menu 
function selectDropdown() {
    if ($(".selectmenu").length) {
        $(".selectmenu").selectmenu();

        var changeSelectMenu = function(event, item) {
            $(this).trigger('change', item);
        };
        $(".selectmenu").selectmenu({ change: changeSelectMenu });
    };
}


// placeholder remove
function removePlaceholder() {
    if ($("input,textarea").length) {
        $("input,textarea").each(
            function() {
                $(this).data('holder', $(this).attr('placeholder'));
                $(this).on('focusin', function() {
                    $(this).attr('placeholder', '');
                });
                $(this).on('focusout', function() {
                    $(this).attr('placeholder', $(this).data('holder'));
                });

            });
    }
}


// Main Menu Function 
function themeMenu() {
    if ($("#main_menu").length) {
        $("#main_menu").menuzord({
            animation: "zoom-out"
        });
    }
}



// cart item Dismiss
function cartItemDismiss() {
    if ($('.cart_option').length) {
        $('.cart_list>ul>li').append(function() {
            return '<i class="fa fa-times-circle" aria-hidden="true"></i>';
        });
        $('.cart_list>ul>li .fa-times-circle').on('click', function() {
            $(this).parent('li').fadeOut(300);
        });
    };
}

// Cart Open function 
function cartOpen() {
    if ($('#cartDropdown').length) {
        $("#cartDropdown").on('click', function() {
            $(".cart_list").slideToggle(300)
        })
    }
}



// Fancybox Video
function FancypopUpVideo() {
    if ($(".fancy_video").length) {
        $(".fancy_video").fancybox({
            maxWidth: 1080,
            maxHeight: 1080,
            fitToView: false,
            width: '85%',
            height: '85%',
            autoSize: false,
            closeClick: false,
            openEffect: 'none',
            closeEffect: 'none'
        });
    };
}

// Fancybox 
function FancypopUp() {
    if ($(".fancybox").length) {
        $(".fancybox").fancybox({
            openEffect: 'elastic',
            closeEffect: 'elastic',
            helpers: {
                overlay: {
                    css: {
                        'background': 'rgba(0, 0, 0, 0.6)'
                    }
                }
            }
        });
    };
}




// Counter function
function CounterNumberChanger() {
    var timer = $('.timer');
    if (timer.length) {
        timer.appear(function() {
            timer.countTo();
        })
    }
}

// Service Slider
function ServiceSlider() {
    if ($('.service_slider').length) {
        $('.service_slider').owlCarousel({
            loop: true,
            nav: false,
            navText: false,
            dots: false,
            autoplay: true,
            autoplayTimeout: 3500,
            autoplaySpeed: 1000,
            lazyLoad: true,
            responsive: {
                0: {
                    items: 1
                },
                600: {
                    items: 2
                },
                1000: {
                    items: 3
                },
                1001: {
                    items: 3
                }
            }
        })
    }
}



// testimonial Slider
function testimonialSlider() {
    if ($('.testimonials-carousel').length) {
        $('.testimonials-carousel').owlCarousel({
            loop:true,
            margin:30,
            nav:true,
            dots: true,
            autoplayHoverPause:false,
            autoplay: 6000,
            smartSpeed: 700,
            navText: [ '<span class="fa fa-angle-left"></span>', '<span class="fa fa-angle-right"></span>' ],
            responsive:{
                0: {
                    items: 1
                },
                600: {
                    items: 2
                },
                1000: {
                    items: 3
                },
                1001: {
                    items: 3
                }
            }
        })
    }
}




// Accordion
function accordion() {
    if ($('.accordion-box').length) {
        $('.accordion-box .acc-btn').on('click', function() {
            if ($(this).hasClass('active') !== true) {
                $('.accordion-box .acc-btn').removeClass('active');
            }

            if ($(this).next('.acc-content').is(':visible')) {
                $(this).removeClass('active');
                $(this).next('.acc-content').slideUp(500);
            } else {
                $(this).addClass('active');
                $('.accordion-box .acc-content').slideUp(500);
                $(this).next('.acc-content').slideDown(500);
            }
        });
    }
}


// Partner Logo Footer 
function partnersLogo() {
    if ($('#partner_logo').length) {
        $('#partner_logo').owlCarousel({
            loop: true,
            nav: false,
            margin: 30,
            dots: true,
            autoplay: true,
            autoplayTimeout: 1500,
            autoplaySpeed: 1000,
            lazyLoad: true,
            responsive: {
                0: {
                    items: 1
                },
                400: {
                    items: 2
                },
                550: {
                    items: 3
                },
                1001: {
                    items: 4
                }
            }
        })
    }
}



// Scroll to top
function scrollToTop() {
    if ($('.scroll-top').length) {

        //Check to see if the window is top if not then display button
        $(window).on('scroll', function() {
            if ($(this).scrollTop() > 200) {
                $('.scroll-top').fadeIn();
            } else {
                $('.scroll-top').fadeOut();
            }
        });

        //Click event to scroll to top
        $('.scroll-top').on('click', function() {
            $('html, body').animate({ scrollTop: 0 }, 1500);
            return false;
        });
    }
}






//Contact Form Validation
function contactFormValidation() {
    if ($('.form-validation').length) {
        $('.form-validation').validate({ // initialize the plugin
            rules: {
                category: {
                    required: true
                },
                name: {
                    required: true
                },
                email: {
                    required: true,
                    email: true
                },
                phone: {
                    required: true
                },
                message: {
                    required: true
                }
            },
            submitHandler: function(form) {
                $(form).ajaxSubmit({
                    success: function() {
                        $('.form-validation :input').attr('disabled', 'disabled');
                        $('.form-validation').fadeTo("slow", 1, function() {
                            $(this).find(':input').attr('disabled', 'disabled');
                            $(this).find('label').css('cursor', 'default');
                            $('#alert_success').fadeIn();
                        });
                    },
                    error: function() {
                        $('.form-validation').fadeTo("slow", 1, function() {
                            $('#alert_error').fadeIn();
                        });
                    }
                });
            }
        });
    }
}

// Close suddess Alret
function closeSuccessAlert() {
    if ($('.closeAlert').length) {
        $(".closeAlert").on('click', function() {
            $(".alert_wrapper").fadeOut();
        });
        $(".closeAlert").on('click', function() {
            $(".alert_wrapper").fadeOut();
        })
    }
}


// Share item Show
function blogShareSlide() {
    if ($('.share-content').length) {
        $('.share_box button').on('click', function() {
            $(this).parent().find('.share-content').toggleClass('share-show');
        });
    };
}



// Mixitup gallery
function mixitupGallery() {
    if ($(".filter-list").length) {
        $(".filter-list").mixItUp()
    };
}
 
//Sortable Masonary with Filters
function enableMasonry() {
    if($('.sortable-masonry').length){

        var winDow = $(window);
        // Needed variables
        var $container=$('.sortable-masonry .items-container');
        var $filter=$('.filter-btns');

        $container.isotope({
            filter:'*',
             masonry: {
                columnWidth : 0 
             },
            animationOptions:{
                duration:500,
                easing:'linear'
            }
        });
        

        // Isotope Filter 
        $filter.find('li').on('click', function(){
            var selector = $(this).attr('data-filter');

            try {
                $container.isotope({ 
                    filter  : selector,
                    animationOptions: {
                        duration: 500,
                        easing  : 'linear',
                        queue   : false
                    }
                });
            } catch(err) {

            }
            return false;
        });


        winDow.bind('resize', function(){
            var selector = $filter.find('li.active').attr('data-filter');

            $container.isotope({ 
                filter  : selector,
                animationOptions: {
                    duration: 500,
                    easing  : 'linear',
                    queue   : false
                }
            });
        });


        var filterItemA = $('.filter-btns li');

        filterItemA.on('click', function(){
            var $this = $(this);
            if ( !$this.hasClass('active')) {
                filterItemA.removeClass('active');
                $this.addClass('active');
            }
        });
    }
}

enableMasonry();



// Price Ranger 
function priceRange() {
    if ($('.price-ranger').length) {
        $('.price-ranger #slider-range').slider({
            range: true,
            min: 5,
            max: 100,
            values: [11, 49],
            slide: function(event, ui) {
                $('.price-ranger .ranger-min-max-block .min').val('$' + ui.values[0]);
                $('.price-ranger .ranger-min-max-block .max').val('$' + ui.values[1]);
            }
        });
        $('.price-ranger .ranger-min-max-block .min').val('$' + $('.price-ranger #slider-range').slider('values', 0));
        $('.price-ranger .ranger-min-max-block .max').val('$' + $('.price-ranger #slider-range').slider('values', 1));
    };
}



    //tab Hide Show Function
    if($('.about-gallery .tab-links').length){
        
        //Links Nav SLide Toggle
        $('.about-gallery .tab-links .tab-btn').on('click', function(e) {
            e.preventDefault();
            var target = $($(this).next('.tab-list'));
            $(target).slideToggle(300);
        });
        
        
        //tab Images Hide Show
        $('.about-gallery .tab-links .tab-list li a').on('click', function(e) {
            e.preventDefault();
            var target = $($(this).attr('href'));
            $('.about-gallery .tab-links .tab-list li a').removeClass('active');
            $(this).addClass('active');
            $('.about-gallery .tab-content .item').removeClass('collapsed');
            $('.about-gallery .tab-content .item').fadeOut(0);
            $(target).fadeIn(500);
        });
        
    }

// WOW animation 
function wowAnimation() {
    if ($('.wow').length) {
        var wow = new WOW({
            boxClass: 'wow', // animated element css class (default is wow)
            animateClass: 'animated', // animation css class (default is animated)
            offset: 80, // distance to the element when triggering the animation (default is 0)
            mobile: true, // trigger animations on mobile devices (default is true)
            live: true, // act on asynchronously loaded content (default is true)
            callback: function(box) {
                // the callback is fired every time an animation is started
                // the argument that is passed in is the DOM node being animated
            },
            scrollContainer: null // optional scroll container selector, otherwise use window
        });
        wow.init();
    }
}

// Language switcher
function languageSwitcher() {
    if ($("#polyglot-language-options").length) {
        $('#polyglotLanguageSwitcher').polyglotLanguageSwitcher({
            effect: 'fade',
            testMode: true,
            onChange: function(evt) {
                    alert("The selected language is: " + evt.selectedItem);
                }
                //                ,afterLoad: function(evt){
                //                    alert("The selected language has been loaded");
                //                },
                //                beforeOpen: function(evt){
                //                    alert("before open");
                //                },
                //                afterOpen: function(evt){
                //                    alert("after open");
                //                },
                //                beforeClose: function(evt){
                //                    alert("before close");
                //                },
                //                afterClose: function(evt){
                //                    alert("after close");
                //                }
        });
    };
}

// function for style switcher
function swithcerMenu() {
    if ($('.switch_menu').length) {

        $('.switch_btn button').on('click', function() {
            $('.switcher').toggleClass('switcher-show')
        });

        $("#myonoffswitch").on('click', function() {
            $(".fixed").toggleClass("static");
        });

        $("#boxed").on('click', function() {
            $(".main_page").addClass("active_boxlayout");
            $('body').addClass('bg')
        });
        $("#full_width").on('click', function() {
            $(".main_page").removeClass("active_boxlayout");
            $('body').removeClass('bg')
        });

        $('#styleOptions').styleSwitcher({
            hasPreview: false,
            fullPath: 'css/',
            cookie: {
                expires: 999,
                isManagingLoad: true
            }
        });

        // chnage the theme related img/logo
        $('#styleOptions .color1').on('click', function() {
            $('.logo img,.sticky_logo img,.footer_logo a>img').attr('src', 'images/logo/logo.png');

            Cookies.remove('logo-img');
            Cookies.remove('logo-img-footer');
            Cookies.remove('map-skin');


            Cookies.set('logo-img', 'images/logo/logo.png', { expires: 365, path: '/' });
            Cookies.set('logo-img-footer', 'images/logo/logo.png', { expires: 365, path: '/' });
            Cookies.set('map-skin', 'skin-1', { expires: 365, path: '/' });



        });

        $('#styleOptions .color2').on('click', function() {
            $('.logo img,.sticky_logo img,.footer_logo a>img').attr('src', 'images/logo/logo2.png');

            Cookies.remove('logo-img');
            Cookies.remove('logo-img-footer');
            Cookies.remove('map-skin');


            Cookies.set('logo-img', 'images/logo/logo2.png', { expires: 365, path: '/' });
            Cookies.set('logo-img-footer', 'images/logo/logo2.png', { expires: 365, path: '/' });
            Cookies.set('map-skin', 'skin-2', { expires: 365, path: '/' });

        });

        $('#styleOptions .color3').on('click', function() {
            $('.logo img,.sticky_logo img,.footer_logo a>img').attr('src', 'images/logo/logo3.png');

            Cookies.remove('logo-img');
            Cookies.remove('logo-img-footer');
            Cookies.remove('map-skin');


            Cookies.set('logo-img', 'images/logo/logo3.png', { expires: 365, path: '/' });
            Cookies.set('logo-img-footer', 'images/logo/logo3.png', { expires: 365, path: '/' });
            Cookies.set('map-skin', 'skin-3', { expires: 365, path: '/' });

        });

        $('#styleOptions .color4').on('click', function() {
            $('.logo img,.sticky_logo img,.footer_logo a>img').attr('src', 'images/logo/logo4.png');
            Cookies.remove('logo-img');
            Cookies.remove('logo-img-footer');
            Cookies.remove('map-skin');


            Cookies.set('logo-img', 'images/logo/logo4.png', { expires: 365, path: '/' });
            Cookies.set('logo-img-footer', 'images/logo/logo4.png', { expires: 365, path: '/' });
            Cookies.set('map-skin', 'skin-4', { expires: 365, path: '/' });

        });

        $('.logo img').attr('src', Cookies.get('logo-img'));
        $('.sticky_logo img').attr('src', Cookies.get('logo-img'));
        $('.footer_logo a>img').attr('src', Cookies.get('logo-img-footer'));

        $('.google-map-home').addClass(Cookies.get('map-skin'));
        console.log(Cookies.get('logo-img'));

    };
}



// DOM ready function
jQuery(document).on('ready', function() {
    (function($) {
        mainBanner();
        countryInfo();
        selectDropdown();
        removePlaceholder();
        themeMenu();
        cartItemDismiss();
        cartOpen();
        FancypopUpVideo();
        CounterNumberChanger();
        ServiceSlider();
        testimonialSlider();
        accordion();
        partnersLogo();
        scrollToTop();
        contactFormValidation();
        closeSuccessAlert();
        blogShareSlide();
        FancypopUp();
        mixitupGallery();
        enableMasonry();
        priceRange();
        wowAnimation();
        languageSwitcher();
        swithcerMenu();
    })(jQuery);
});



// Window scroll function
jQuery(window).on('scroll', function() {
    (function($) {

    })(jQuery);
});




// Window load function
jQuery(window).on('load', function() {
    (function($) {
        prealoader();
    })(jQuery);
});

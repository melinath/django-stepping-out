;jQuery(function($){
    var popovers = $('.popover-trigger').popover();
    popovers.popover('show').popover('hide');

    $('[title]').tooltip();
});
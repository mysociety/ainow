$(function(){
    $('.js-schedule-accordion').each(function(){

        var $schedule = $(this);
        var $trigger = $('<button>');

        var fold = function() {
            $schedule.children().eq(2).nextAll().addClass('visible-print-block');
        };

        var unfold = function() {
            $schedule.children().removeClass('visible-print-block');
            $trigger.remove();
        };

        fold();

        $trigger.addClass('hidden-print');
        $trigger.html('<span class="btn btn-primary">Show full agenda</span>');
        $trigger.on('click', unfold);
        $trigger.prependTo($schedule);

    });
});

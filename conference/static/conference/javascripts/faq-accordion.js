$(function(){
    $(".js-faq-accordion").on("click", ".js-faq-accordion--header", function() {
        $(this).toggleClass("active").next().slideToggle();
    });
});

$(function () {
    $(".star").on("click", function () { //RATING PROCESS
        var rate = $(this).attr("id");
        var user = $("#user-data").attr("value");
        var movie = $("#movie-data").attr("value");
        console.log(rate)
        $.ajax({
            type: "POST",
            url: "/rate",
            data: {'rating':rate, 'user':user, 'movie':movie}
        })
    });
})
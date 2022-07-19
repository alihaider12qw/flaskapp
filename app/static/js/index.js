$(document).ready(function () {
    console.log("ready!");

    const ELS_pinEntry = document.querySelectorAll(".pinEntry");
    const selectAllIfFull = (evt) => {
        const EL_input = evt.currentTarget;
        if (EL_input.value.length >= 4) EL_input.select();
    };
    ELS_pinEntry.forEach(el => {
        el.addEventListener("focusin", selectAllIfFull);
    });


    $("#login_with_phone").on("click", function (e) {
        $(".show1").toggleClass('d-none')
        $(".show2").toggleClass('d-none')
    });
    $("#login_with_email").on("click", function (e) {
        $(".show1").toggleClass('d-none')
        $(".show2").toggleClass('d-none')
    });
    $("#mobile_next").on("click", function (e) {
        $(".show2").toggleClass('d-none')
        $(".show3").toggleClass('d-none')
    });
    console.log("$('.input-group.date')");
    console.log($('.input-group.date'));
    var ind = $('.input-group.date');
    if (ind.length > 0) {
        ind.on("click", function () {
            console.log("clicked");
        })
        ind.datepicker({
            clearBtn: true,
            daysOfWeekDisabled: "0,6",
            autoclose: true,
            todayHighlight: true
        });
    }
});


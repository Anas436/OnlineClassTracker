// const meterials_btn = document.querySelectorAll('.btn-meterials')

// meterials_btn.forEach(btn => {
//     btn.addEventListener('click', () => {
//         btn.classList.add("btn-meterials-active");
//         document.querySelector('.btn-meterials-active').classList.remove('btn-meterials-active');
//     });
// });

$(document).ready(function () {
    // Add click event to all neumorphic buttons
    $('.btn-meterials').click(function () {
        // Remove active class from all buttons
        $('.btn-meterials').removeClass('active');
        // Add active class to the clicked button
        $(this).addClass('active');
    });
});
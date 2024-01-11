// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

// owl carousel 

$('.owl-carousel').owlCarousel({
    loop: true,
    margin: 10,
    nav: true,
    autoplay: true,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 3
        },
        1000: {
            items: 6
        }
    }
})

function togglePasswordVisibility() {
    const passwordInput = document.querySelector("input[name='pwd']");
    const eyeIcon = document.querySelector(".show-password");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        eyeIcon.classList.remove("fa-eye");
        eyeIcon.classList.add("fa-eye-slash");
    } else {
        passwordInput.type = "password";
        eyeIcon.classList.remove("fa-eye-slash");
        eyeIcon.classList.add("fa-eye");
    }
}

function checkPasswordMatch() {
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirmPassword");
    const matchIcon = document.getElementById("matchIcon");

    if (confirmPasswordInput.value === '') {
        matchIcon.style.display = 'none';
    } else if (passwordInput.value === confirmPasswordInput.value) {
        matchIcon.classList.remove("fa-times");
        matchIcon.classList.add("fa-check");
        matchIcon.style.color = "white";
        matchIcon.style.display = 'inline';
    } else {
        matchIcon.classList.remove("fa-check");
        matchIcon.classList.add("fa-times");
        matchIcon.style.color = "white";
        matchIcon.style.display = 'inline';
    }
}
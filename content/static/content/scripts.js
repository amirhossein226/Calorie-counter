$(document).ready(function () {
    $('nav').slideDown(400);

    document.querySelectorAll('.btn-nav').forEach(btn => {
        btn.addEventListener("click", () => {
            if (btn.value == "home") {
                showHome();
            } else if (btn.value == "counter") {
                showCounter();
            } else if (btn.value == 'bmi') {
                showBmi();
            }
        });
    });

    checkNav();


});

function showHome() {
    $("#counter")[0].style.display = "none";
    $("#bmi")[0].style.display = "none";
    $("#single-art")[0].style.display = "none";
    $("#first-image")[0].style.display = "block";
    $("#home")[0].style.display = "block";

    document.body.style.backgroundColor = "rgba(83, 86, 83, 0.721)";
};

function showCounter() {
    $("#bmi")[0].style.display = "none";
    $("#single-art")[0].style.display = "none";
    $("#first-image")[0].style.display = "none";
    $("#home")[0].style.display = "none";
    $("#counter")[0].style.display = "flex";

    const counterContainer = document.getElementById('counter');
    document.body.style.backgroundColor = "white";

    // counterContainer.querySelector("div.bmi-f-container").innerHTML = `

    // `;
    // const formInputs = counterContainer.querySelectorAll("").forEach(input => {
    //     input.classList += "cen-el";
    // })

};


function showBmi() {
    $("#counter")[0].style.display = "none";
    $("#single-art")[0].style.display = "none";
    $("#first-image")[0].style.display = "none";
    $("#home")[0].style.display = "none";
    $("#bmi")[0].style.display = "block";


};

/* this function will fetch the single 
 article content and then give it to pushArticle function.*/
function fetchArticle(element) {

    let div = element.parentNode;
    let input = div.querySelector("input[type=hidden]")
    const id = input.value;
    fetch(`/articles/${id}`)
        .then(response => response.json())
        .then(content => {
            const bodyStyle = document.body.style;
            bodyStyle.color = 'white';
            bodyStyle.backgroundColor = "rgba( 0, 0, 0, 0.81)";
            pushArticle(content);
        });
};


// this function will push the content received from server into the page 
function pushArticle(content) {

    $('#home')[0].style.display = "none";
    $('#first-image')[0].style.display = "none";
    let singleArt = $('#single-art')[0];
    console.log(content)
    singleArt.style.display = "flex";
    singleArt.style.flexDirection = "column";
    console.log(content)
    singleArt.querySelector("#food-image img").src = content.picture;
    singleArt.querySelector("#art-name").innerHTML = content.headline;
    singleArt.querySelector("#l-date").innerHTML = "&ensp;" + content.last_update;
    singleArt.querySelector("#author").innerHTML = "&ensp;" + content.author_name;
    singleArt.querySelector("#text").innerHTML = content.content;




}

/* this function checks if the user scrolled down(to hide the navbar)
  or up(to show the navbar again)*/
function checkNav() {
    var oldPosition = window.scrollY;

    window.onscroll = function () {
        var newPosition = window.scrollY;

        let different = newPosition - oldPosition;

        if (oldPosition < newPosition & different > 50) {
            oldPosition = newPosition;
            $("nav").slideUp(400);
        }

        if (oldPosition > newPosition & different < -3) {
            oldPosition = newPosition;
            $("nav").slideDown(400);
        }
    }

}
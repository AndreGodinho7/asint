import QrScanner from "/static/js/qr-scanner.min.js";
QrScanner.WORKER_PATH = "/static/js/qr-scanner-worker.min.js";

const apiDomain = "127.0.0.1"
const apiUrl = "http://" + apiDomain + ":8089/";

var scanner;
var waitingForSecret = false;

function hideEverything() {
    jQuery("div#codeScanner,div#content,div#secretForm,div#showSecret,div#userInfo").hide();
    jQuery("div#content").html("");
    jQuery("#secretInput").val("");
    jQuery("#secretText").html("");
    jQuery("#userName").text("");
    jQuery("#userPhoto").attr("src", "");
    jQuery("#mestrado").text("");
    waitingForSecret = false;
    scanner.stop();
}

function showUserInfo(userInfo) {
    jQuery("#userName").text(userInfo.name);
    jQuery("#userPhoto").attr("src", "data:" + userInfo.photo.type + ";base64," + userInfo.photo.data);
    jQuery("#userInfo").show();
    jQuery("#mestrado").text(userInfo.roles[0].registrations[0].name)
}

function codeScanner() {
    hideEverything();
    jQuery("#codeScanner").show();
    scanner.start();
}

function secretForm() {
    hideEverything();
    jQuery("#secretForm").show();
}

function submitSecret() {
    var secret = jQuery("#secretInput").val();
    hideEverything();
    jQuery.get(apiUrl + "info/" + secret, result => {
        showUserInfo(result);
    }, "json");
}

function showSecret() {
    hideEverything();
    jQuery.get(apiUrl + "secret", secret => {
        jQuery("span#secretText").text(secret);
        jQuery("#showSecret").show();

        waitingForSecret = true;

        var timerId = setInterval(function () {
            if (waitingForSecret) {
                jQuery.get(apiUrl + "secretUsed", result => {
                    hideEverything();
                    waitingForSecret = false;

                    showUserInfo(result);
                }, "json");
            } else {
                clearInterval(timerId);
            }
        }, 500);
    }, "text");
}

jQuery(document).ready(function () {
    const video = document.getElementById('qr-video');
    scanner = new QrScanner(video, result => {
        const urlExpr = new RegExp("http:\/\/" + apiDomain + ":8089/([A-Za-z0-9]+)/([A-Za-z0-9]+)");
        var results = urlExpr.exec(result);

        if (results && results.length == 3) {
            var microservice = results[1];
            var identifier = results[2];

            var fetchURL = apiUrl + "api/" + microservice + "/" + identifier;

            scanner.stop();
            hideEverything();

            jQuery.get(fetchURL, data => {
                jQuery("div#content").text(data).show();
            }, "text");
        }
    });

    jQuery("#qrButton").click(codeScanner);
    jQuery("#showSecretBtn").click(showSecret);
    jQuery("#enterSecret").click(secretForm);
    jQuery("#submitSecretBtn").click(submitSecret);
});
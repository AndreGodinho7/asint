import QrScanner from "/static/js/qr-scanner.min.js";
QrScanner.WORKER_PATH = "/static/js/qr-scanner-worker.min.js";

jQuery(document).ready(function () {
    const video = document.getElementById('qr-video');
    const urlExpr = new RegExp("http:\/\/127.0.0.1:8089/([A-Za-z0-9]+)/([A-Za-z0-9]+)");
    const scanner = new QrScanner(video, result => {

        var results = urlExpr.exec(result);

        if (results.length == 3) {
            var microservice = results[1];
            var identifier = results[2];

            var fetchURL = "http://127.0.0.1:8089/api/" + microservice + "/" + identifier;

            jQuery.get(fetchURL, data => {
                jQuery("div#res").text(data);
            }, "text");
        }
    });

    scanner.start();
});
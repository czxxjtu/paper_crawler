var fs = require('fs');
var array = fs.read('input.txt').toString().split("\n");

var links;
var noHTMLQuery = "";
var casper = require('casper').create({
    verbose: true,
    logLevel: 'error'
});
var hasResult;
var hasHTML;


casper.start('http://ieeexplore.ieee.org/Xplore/home.jsp', function() {
    console.log("===== in - start =====");
});

function doEach(query, inde) {
    
    casper.thenOpen('http://ieeexplore.ieee.org/Xplore/home.jsp', function() {
        console.log("[ " + inde.toString() + ": " + query + " ]")
        console.log("===== in - start =====");
        hasResult = true;
        hasHTML = true;
    });

    casper.waitUntilVisible("#search_form button", function() {
        console.log("===== in - then - 1 =====");
        this.fill('form[action="/search/searchresult.jsp"]', { queryText: query, newsearch: 'true' }, false);
        this.click('button.js-search.Search-submit.Button.btn-search');
    });

    casper.waitUntilVisible("#search_results_form", function() {
        console.log("===== in - then - 2 =====");
        if (this.exists("div.page-tools")) {
            // exist search result
            this.capture("capture/" + inde.toString() + "_1.png");
            this.thenClick('div.detail h3 a', function() {
                casper.wait(3000, function() {
                    console.log("===== in - then - 3 =====");
                    if (this.exists("#full-text-html")){
                        // exist html paper
                        this.capture("capture/" + inde.toString() + "_2.png");
                        this.thenClick('a#full-text-html', function() {
                            casper.wait(3000, function() {
                                console.log("===== in - then - 4 =====");
                                if (hasHTML) {
                                    this.capture("capture/" + inde.toString() + "_3.png");
                                    var fs = require('fs');
                                    fs.write("html/" + inde.toString() + ".html", this.getHTML(), 'w');
                                    this.captureSelector("img/" + inde.toString() + ".png", "div.img-wrap");
                                } 
                            });
                        });
                    } else {
                        console.log("===== No HTML =====");
                        noHTMLQuery = noHTMLQuery + query + "\r\n";
                        hasHTML = false;
                    }
                });
            }, 20000);
        } else {
            console.log("===== No Result =====");
            hasResult = false;
        }
    }, 20000);    
}

for(i in array) {
    console.log(i.toString() + ": " + array[i]);
    doEach(array[i], i);
}

function makeNoHTMLText() {
    var fs = require('fs');
    fs.write("output/no_html_list.txt", noHTMLQuery, 'w');
}

casper.run(function() {
    console.log("===== in - run =====");
    makeNoHTMLText()
    this.exit();
});
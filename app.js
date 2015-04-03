var fs = require('fs');
var array = fs.read('input.txt').toString().split("\n");

var links;
var casper = require('casper').create({
    // verbose: true,
    // logLevel: 'debug'
});

casper.start('http://ieeexplore.ieee.org/Xplore/home.jsp', function() {
    // search for 'casperjs' from google form
    console.log("===== in - start =====");
});

function doEach(query, inde) {
    
    casper.thenOpen('http://ieeexplore.ieee.org/Xplore/home.jsp', function() {
        // search for 'casperjs' from google form
        console.log("[ " + inde.toString() + ": " + query + " ]")
        console.log("===== in - start =====");
    });

    casper.wait(2000, function() {
        console.log("===== in - then - 1 =====");
        this.capture("capture/" + inde.toString() + "_1.png");
        this.fill('form[action="/search/searchresult.jsp"]', { queryText: query, newsearch: 'true' }, false);
        this.click('button.js-search.Search-submit.Button.btn-search');
    });

    casper.wait(5000, function() {
        // aggregate results for the 'casperjs' search
        console.log("===== in - then - 2 =====");
        this.capture("capture/" + inde.toString() + "_2.png");
        // this.capture("capture.png");
        this.click('div.detail h3 a');
    });

    casper.wait(2000, function() {
        console.log("===== in - then - 3 =====");
        this.capture("capture/" + inde.toString() + "_3.png");
        this.click('a#full-text-html');
    });

    casper.wait(2000, function() {
        console.log("===== in - then - 4 =====");
        this.capture("capture/" + inde.toString() + "_4.png");
        var fs = require('fs');
        fs.write("html/" + inde.toString() + ".html", this.getHTML(), 'w');
        // links = links.concat(this.evaluate(getLinks));
    });

    
}

for(i in array) {
    console.log(i.toString() + ": " + array[i]);
    doEach(array[i], i);
}

casper.run(function() {
    console.log("===== in - run =====");
    this.exit();
});
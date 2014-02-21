window.onload = function () {

    var r = Raphael("holder", 3000, 3000);

    var visibleObjects = r.set();

    var application = function(){
        this.body = r.circle(100, 100, 20);
        this.body.attr({fill: "#FF3399", stroke: "#111", "fill-opacity": 1/6});
        visibleObjects.push(this.body);

        this.move = function(x, y){
            this.body.animate({cx:x, cy:y});
        };

        this.interfaces = [];

        this.packages = [];
        for(var i = 0 ; i < 5 ; i++){
            this.packages.push(new package());
        }

        this.runPackages = function(){
            for(var i = 0 ; i < packages.length ; i++){
                this.packages[i].run(
                    this.body.attr('cx'),
                    this.body.attr('cy'),
                    this.interfaces[0].body.attr('cx'),
                    this.interfaces[0].body.attr('cy')
                );
            }
        }
    };

    var package = function(){
        this.body = r.circle(0,0,5);
        this.body.attr({fill: "#FF3399", stroke: "#111", "fill-opacity": 1/6});
        visibleObjects.push(this.body);

        this.run = function(xStart, yStart, xEnd, yEnd){
            this.body.attr("cx", xStart);
            this.body.attr("cy", yStart);
            this.body.animate({cx: xEnd, cy:yEnd}, 1000, "<>");
        };
    };

    var packages = [];
    for(var i = 0 ; i < 3 ; i++){
        packages.push(new package());
    }
    for(var i = 0 ; i < packages.length ; i++){
        packages[i].run(1,1,100,100);
    }

    var interface = function(){
        this.body = r.circle(100, 100, 10);
        this.body.attr({fill: "#0000FF", stroke: "#111", "fill-opacity": 1/6});
        visibleObjects.push(this.body);

        this.move = function(x, y){
            this.body.animate({cx:x, cy:y});
        };
    };

    var framework = function(){

        this.body = r.circle(100, 100, 100);
        this.body.attr({fill: "#00CC00", stroke: "#111", "fill-opacity": 1/6});
        visibleObjects.push(this.body);

        this.move = function(x, y){
            this.body.animate({cx:x, cy:y});
            this.moveApplications(x, y);
            this.moveInterfaces(x, y);
        };

        this.applications = [];
        for(var i = 0 ; i < 3 ; i++){
            this.applications.push(new application());
        }
        this.moveApplications = function(x, y){
            for(var i = 0 ; i < this.applications.length ; i++){
                var radius = 100;
                var centerX = x + i*radius/(this.applications.length-1) - radius/2;
                var centerY = y - 20;
                var angle = (360 * i) / this.applications.length;
                this.applications[i].move(centerX,centerY);
            }
        };

        this.interfaces = [];
        for(var i = 0 ; i < 3 ; i++){
            this.interfaces.push(new interface());
        }
        this.moveInterfaces = function(x, y){
            for(var i = 0 ; i < this.interfaces.length ; i++){
                var radius = 100;
                var centerX = x + i*radius/(this.interfaces.length-1) - radius/2;
                var centerY = y + 50;
                var angle = (360 * i) / this.interfaces.length;
                this.interfaces[i].move(centerX,centerY);
            }
        };

        for(var i = 0 ; i < this.applications.length; i++){
            for(var j =  0 ; j < this.interfaces.length ; j++){
                this.applications[i].interfaces.push(this.interfaces[j]);
            }
        }
    };

    var frameworks = [];
    for(var i = 0; i < 10  ; i++){
        frameworks.push(new framework());
    }

    for(var i = 0; i < frameworks.length ; i++){
        var radius = 400;
        var centerX = radius + 110;
        var centerY = radius + 110;
        var angle = (360 * i) / frameworks.length;
        frameworks[i].move(centerX + Math.cos((angle * Math.PI) / 180) * radius , centerY + Math.sin((angle * Math.PI) / 180) * radius);
    }

    for(var i = 0; i < frameworks.length ; i++){
        for(var j = 0 ; j < frameworks[i].applications.length ; j++){
            frameworks[i].applications[j].runPackages();
        }
    }
};
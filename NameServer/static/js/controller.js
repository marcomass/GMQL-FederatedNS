/* ##########################################################
   Main Controller - Always active independently on the view
   ########################################################## */
app.controller('ns_ctrl', function($scope, $http, $location, $rootScope) {

    view = $location.path(); // gets the name of the current view

    // Check if the user is logged-in - if it is not redirect to the login page
    $rootScope.checkLogin = function() {

        console.log("Checking user login.")

        if( $.cookie('token')!= undefined && $.cookie('instancename')!= undefined ) {

            console.log("Found session cookies.")

            // If both cookies are set, try to retrieve user's information

            $rootScope.logged_user = {token: $.cookie('token'), instancename: $.cookie('instancename')}

            $http({
                method: 'GET',
                url:   API.instance+$rootScope.logged_user.instancename+"/",
                headers: {'Authorization': 'Token '+$rootScope.logged_user.token}

            }).then(
                // SUCCESS
                function(response) {

                    console.log("The user is logged in.");
                    $scope.logged = true;

                    // If the current view is login or signup redirect to the home page
                    if (view=="/login" || view=="/signup") {
                        setTimeout(function(){ window.location = "./index.html#!/home";}, 100)
                    }

                    // Retrieve instance location and set it on the rootScope
                    $http({
                        method: 'GET',
                        url:   API.location+$rootScope.logged_user.instancename+"/",
                        headers: {'Authorization': 'Token '+$rootScope.logged_user.token}

                    }).then(
                        // SUCCESS
                        function(response) {
                            $rootScope.logged_user.location = response.data.URI;
                        },
                        // ERROR
                        function(response){
                            console.error("Cannot retrieve instance location.");
                        }
                    );
                },

                // ERROR
                function(response){
                    // Found cookies were rejected by the API -> Delete them
                    $.removeCookie("token",{ path: '/static/' });
                    $.removeCookie("instancename",{ path: '/static/' });

                    // Redirect to the login page if necessary
                    if (view!="/login" && view!="/signup") {
                        setTimeout(function(){ window.location = "./index.html#!/login";}, 100);
                    }
                }
            );
        } else {

            // At least one of the cookies was not found -> clean all cookies
            $.removeCookie("token",{ path: '/static/' });
            $.removeCookie("instancename",{ path: '/static/' });

            // If the current page is not login or signup -> redirect to the login page
            if (view!="/login" && view!="/signup") {
                setTimeout(function(){ window.location = "./index.html#!/login";}, 100);
            }
        }
    }

    // Logout function
    $scope.logout = function() {
        $scope.logged = false;
        $.removeCookie("token",{ path: '/static/' });
        $.removeCookie("instancename",{ path: '/static/' });
        setTimeout(function(){ window.location = "./index.html#!/login";}, 100);
    }

    /* # Initialization # */
    $rootScope.checkLogin();

});

/* ####################
   Home Controller
   #################### */
app.controller('home_ctrl', function($scope, $http, $rootScope) {

    // Set the repository.xml string depending on the visibility of the token
    function setConf(hide) {

        tk = hide? "...." : $rootScope.logged_user.token;

        confString = '<property name="GF_ENABLED">true<property>\n'+
            '<property name="GF_NAMESERVER_ADDRESS">http://'+window.location.host+'/</property>\n'+
            '<property name="GF_INSTANCENAME">'+$rootScope.logged_user.instancename+'<property>\n'+
            '<property name="GF_TOKEN">'+tk+'</property>'

        $("#repoxml code").text(confString);

        Prism.highlightAll();

    }

    // Save changes to the instance URL
    $scope.saveLocation = function(location) {

        loc = {
            name:  $rootScope.logged_user.instancename,
            details: $rootScope.logged_user.instancename+"'s location",
            URI:  location
        }

        $http({
            method: 'PUT',
            url:   API.location+$scope.logged_user.instancename+"/",
            data:  $.param(loc),
            headers: {'Content-Type': 'application/x-www-form-urlencoded',
                      'Authorization': 'Token '+$rootScope.logged_user.token}
        }).then( 
            // SUCCESS
            function(response) {
                $("#alert-text").text("Successfully updated.");
                $("#alert").removeClass("alert-danger");
                $("#alert").addClass("alert-success");
                $("#alert").fadeIn('medium');
            }, 
            //ERROR
            function(response) {
                $("#alert-text").text("Error updating.");
                $("#alert").removeClass("alert-success");
                $("#alert").addClass("alert-danger");
                $("#alert").fadeIn('medium');
            });

    }


    /* # Graphic-support functions # */

    // Hide/Show token
    $scope.toggleHideToken = function(){
        $scope.hideToken=!$scope.hideToken;
        if($scope.hideToken) {
            $("#show_hide_token input").attr("type","password");
            setConf(true);

        } else {
            $("#show_hide_token input").attr("type","text");
            setConf(false);
        }


    }

    // Close an open alert
    $scope.closeAlert = function() {
        $('#alert').fadeOut('medium');
    }


    /* # Initialization # */
    $scope.hideToken = true;
    setConf(true);
    $("#alert").hide();
    $scope.active_menu = "home";


});


/* ####################
   Login Controller
   #################### */
app.controller('login_ctrl', function($scope, $rootScope, $http) {

    // Login function
    $scope.login = function(user) {

        data = {
            username:  user.instancename,
            password:  user.password,
            csrfmiddlewaretoken: getCookie('csrftoken')
        }

        // Send a post request with login info
        $http({
            method: 'POST',
            url:   API.token,
            data:  $.param(data),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}

        }).then(
            // SUCCESS
            function(response) {
                setAlert("Success.", true);
                $.cookie('token', response.data.token);
                $.cookie('instancename', response.data.instancename);

                $rootScope.checkLogin();

                setTimeout(function(){ window.location = "./index.html#!/home";}, 100);
            },
            // ERROR
            function(response){
                if(response.status==400) {
                    setAlert("Wrong credentials.", false);
                } else {
                    setAlert("Error.", false);
                }
            }
        );

        /* # Initialization # */
        //
    }

});

/* ####################
   Signup Controller
   #################### */
app.controller('signup_ctrl', function($scope, $http) {

    // Generate random user data for testing
    function generateRandomUser() {
        $scope.instance = {
            instancename: "c"+(new Date()).getTime(), 
            email: (new Date()).getTime()+"@gmail.com", 
            description:"c",
            password: "ciao", 
            repeatPassword:"ciao",
            location: "c"
        };
        $scope.locationURL = "http://www.google.com";
    }

    // Signup function
    $scope.register = function(instance) {


        if( /\s/.test(instance.instancename) ){
            setAlert("Error: Blank spaces not allowed.", false); 
            return;
        }

        // Check if provided passwords are the same
        if(instance.password!=instance.repeatPassword) {
            $("#repeat-password").addClass("is-invalid");
            setAlert("Passwords don't match.", false);
            return;
        } else {
            resetAlert();
        }

        // Set csrftoken
        $scope.instance.csrfmiddlewaretoken = getCookie('csrftoken');

        // Call Registration API
        $http({
            method: 'POST',
            url:   API.instance,
            data:  $.param($scope.instance),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}

        }).then(

            // SUCCESS (Registration)
            function(response) {

                console.log("User created. Adding location.");

                // Get token and then set the instance location
                data = {
                    username:  $scope.instance.instancename,
                    password:  $scope.instance.password,
                    csrfmiddlewaretoken: getCookie('csrftoken')
                }

                $http({
                    method: 'POST',
                    url:   API.token,
                    data:  $.param(data),
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}

                }).then(
                    // SUCCESS (Retrieving token)
                    function(response) {

                        token = response.data.token;

                        // Use the token to set the location

                        data = {
                            name:  $scope.instance.instancename,
                            details: $scope.instance.instancename+"'s location",
                            URI:  $scope.locationURL
                        }


                        $http({
                            method: 'POST',
                            url:   API.location,
                            data:  $.param(data),
                            headers: {'Content-Type': 'application/x-www-form-urlencoded', 
                                      'csrfmiddlewaretoken': getCookie('csrftoken'), 
                                      'Authorization': "Token "+token}

                        }).then(
                            // SUCCESS (Creating location)
                            function (response) {
                                setAlert("You are now registered.", true);

                                // Redirect to the login page
                                setTimeout(function(){ window.location = "./index.html#!/login";}, 1000);

                            },
                            // ERROR (Creating location)
                            function (response) {
                                setAlert("Failed creating location.", false);
                                console.error(response);
                            }

                        );

                    }, 

                    // ERROR (Retrieving token)
                    function(response) {
                        setAlert("Failed retrieving token.", false);
                        console.error(response);
                    }
                );
            },

            // ERROR (Registration)
            function(response) {

                if(response.status == 400 && response.data.email != undefined){
                    setAlert("Email already exists.", false);
                } else if (response.status == 500 && response.data.includes("UNIQUE")){
                    // TODO: improve server-side
                    setAlert("User already exists.", false);
                } else {
                    setAlert("Error "+response.status+".", false);
                }
                console.error(response);
            }
        );
    }

    /* # Initialization # */
    //generateRandomUser();

});

/* ####################
   Datasets Controller
   #################### */
app.controller('datasets_ctrl', function($scope, $location, $http, $rootScope, $routeParams) {

    // List datasets
    function getDatasets() {

        console.log("Getting datasets.");

        $http({
            method: 'GET',
            url:   API.dataset,
            headers: {'Authorization': 'Token '+$rootScope.logged_user.token}

        }).then(
            // SUCCESS
            function(response) {
                $scope.datasets = response.data;
            }, 

            // ERROR 
            function(response) {
                console.error("Error retrieving datasets.");
            }
        );
    }

    // List groups
    function getGroups() {

        console.log("Getting groups.");

        $http({
            method: 'GET',
            url:   API.group,
            headers: {'Authorization': 'Token '+$rootScope.logged_user.token}

        }).then(
            // SUCCESS
            function(response) {
                $scope.groups = response.data;
            }, 

            // ERROR 
            function(response) {
                console.error("Error retrieving groups.");
            }
        );
    }

    // List instances
    function getInstances() {

        console.log("Getting instances.");

        $http({
            method: 'GET',
            url:   API.instance,
            headers: {'Authorization': 'Token '+$rootScope.logged_user.token}

        }).then(
            // SUCCESS
            function(response) {
                $scope.instances = response.data;
            }, 

            // ERROR 
            function(response) {
                console.error("Error retrieving instances.");
            }
        );
    }

    // Create a new dataset
    $scope.create = function(dataset) {

        console.log("Creating dataset");

        if( /\s/.test(dataset.name) ){
            setAlert("Error: Blank spaces not allowed.", false); 
            return;
        }

        // Generate FormData
        fd =  new FormData();
        fd.append('name', dataset.name);
        fd.append('author',dataset.author);
        fd.append('description', dataset.description);

        for(var i=0; i<dataset.allowed_to.length; i++)  
            fd.append('allowed_to', dataset.allowed_to[i]);
        for(var i=0; i<dataset.copies.length; i++)  
            fd.append('copies', dataset.copies[i]);

        // Send a POST request
        $http({
            method: 'POST',
            url:   API.dataset,
            data:  fd,
            headers: {'Content-Type': undefined,
                      'Authorization': 'Token '+$rootScope.logged_user.token}
        }).then(
            // SUCCESS
            function(response) {
                setAlert("Dataset created.", true);
                getDatasets();

                setTimeout(function(){ window.location = "./index.html#!/datasets";}, 500);
            },
            // ERROR
            function(response){
                if (response.status == 500 && response.data.includes("UNIQUE")){
                    // TODO: improve server-side
                    setAlert("Dataset "+dataset.name+" already exists.", false);
                } else {
                    setAlert("Error.", false);
                }
            }
        );
    }

    // Update a dataset
    $scope.save_changes = function(dataset) {

        console.log("Updating dataset");

        if( /\s/.test(dataset.name) ){
            setAlert("Error: Blank spaces not allowed.", false); 
            return;
        }

        // Generate FormData
        fd =  new FormData();
        fd.append('name', dataset.name);
        fd.append('author',dataset.author);
        fd.append('description', dataset.description);

        for(var i=0; i<dataset.allowed_to.length; i++)  
            fd.append('allowed_to', dataset.allowed_to[i]);
        for(var i=0; i<dataset.copies.length; i++)  
            fd.append('copies', dataset.copies[i]);

        // Send a PUT request
        $http({
            method: 'PUT',
            url:   API.dataset+$scope.dataset_id+"/",
            data:  fd,
            headers: {'Content-Type': undefined,
                      'Authorization': 'Token '+$rootScope.logged_user.token}

        }).then(
            // SUCCESS
            function(response) {
                setAlert("Saved.", true);

                // Redirect to the list of datasets
                setTimeout(function(){window.location = "./index.html#!/datasets/";}, 1000);
            },
            // ERROR
            function(response){

                if (response.status == 500 && response.data.includes("UNIQUE")){
                    // TODO: improve server-side
                    setAlert("Dataset "+dataset.name+" already exists.", false);
                } else {
                    setAlert("Error.", false);
                }

            }
        );
    }

    // Delete a dataset
    $scope.delete = function(dataset_id) {

        console.log("Deleting dataset");

        if( confirm("You are going to delete this dataset ..") ) {

            $http({
                method: 'DELETE',
                url:   API.dataset+dataset_id+"/",
                headers: {'Content-Type': undefined,
                          'Authorization': 'Token '+$rootScope.logged_user.token}

            }).then(
                // SUCCESS
                function(response) {
                    setAlert("Deleted.", true);

                    // Redirect to the list of datasets
                    setTimeout(function(){window.location = "./index.html#!/datasets/";}, 1000);
                },
                // ERROR
                function(response){
                    setAlert("Error deleting.", false);
                }
            );
        }

    }


    /* # Multi-selection support functions # */
    $scope.moveItems = function(items, destination) {

        if(items!=undefined) {
            for(var i=0; i<items.length; i++) {
                if(!destination.includes(items[i].trim()))
                    destination.push(items[i].trim());
            }
        }
    }

    $scope.deleteItem = function(item, from) {
        return from.filter(function(el){return el!=item});
    }

    /* # Initialization # */

    $scope.active_menu = "datasets";

    $scope.datasets = [];

    if("datasetId" in $routeParams)
        $scope.dataset_id =$routeParams.datasetId

    view = $location.path();

    // Initialization based on the current view
    if (view == "/datasets") 
        getDatasets();

    if (view == "/datasets/create" || view.startsWith("/datasets/edit")) {
        getGroups();
        getInstances();

        $('#datasetName').tooltip({'trigger':'focus', 'title': 'The exact name of a dataset in your public repository.'});


        if (view == "/datasets/create") {
            // Set default privacy and location
            $scope.dataset = { allowed_to:[$rootScope.logged_user.instancename], copies:[$rootScope.logged_user.instancename]};
        } else if(view.startsWith("/datasets/edit")) {

            $http({
                method: 'GET',
                url:   API.dataset+$scope.dataset_id+"/",
                headers: {'Authorization': 'Token '+$rootScope.logged_user.token}

            }).then(
                // SUCCESS
                function(response) {
                    $scope.dataset = response.data;
                },
                // ERROR
                function(response){
                    console.error("Unable to retrieve dataset "+$scope.dataset_i);
                }
            );

        }
    }

});

/* ####################
   Instances Controller
   #################### */
app.controller('instances_ctrl', function($scope, $location, $rootScope, $http, $routeParams) {

    // List all instances
    function getInstances() {

        console.log("Getting instances.");

        $http({
            method: 'GET',
            url:   API.instance,
            headers: {'Authorization': 'Token '+$rootScope.logged_user.token}

        }).then(
            // SUCCESS
            function(response) {
                $scope.instances = response.data;
            }, 

            // ERROR 
            function(response) {
                console.error("Error retrieving instances.");
            }
        );
    }

    /* # Initialization # */
    $scope.active_menu = "instances";
    getInstances();

});

/* ####################
   Groups Controller
   #################### */
app.controller('groups_ctrl', function($scope, $location, $rootScope, $http, $routeParams) {

    // List all groups
    function getGroups() {

        console.log("Getting groups.");

        $http({
            method: 'GET',
            url:   API.group,
            headers: {'Authorization': 'Token '+$rootScope.logged_user.token}

        }).then(
            // SUCCESS
            function(response) {
                $scope.groups = response.data;
            }, 

            // ERROR 
            function(response) {
                console.error("Error retrieving groups.");
            }
        );
    }

    // List all instances
    function getInstances() {

        console.log("Getting instances.");

        $http({
            method: 'GET',
            url:   API.instance,
            headers: {'Authorization': 'Token '+$rootScope.logged_user.token}

        }).then(
            // SUCCESS
            function(response) {
                $scope.instances = response.data;
            }, 

            // ERROR 
            function(response) {
                console.error("Error retrieving instances.");
            }
        );
    }

    // Create a group
    $scope.create = function(group) {

        console.log("Creating group");

        if( /\s/.test(group.name) ){
            setAlert("Error: Blank spaces not allowed.", false); 
            return;
        }

        if(group.instances.length<2){
            setAlert("Error: Single instance group not allowed.", false); 
            return;
        }

        // Creating form data
        fd =  new FormData();
        fd.append('name', group.name)

        for(var i=0; i<group.instances.length; i++)  
            fd.append('instances', group.instances[i]);

        // Sending a POST request
        $http({
            method: 'POST',
            url:   API.group,
            data:  fd,
            headers: {'Content-Type': undefined,
                      'Authorization': 'Token '+$rootScope.logged_user.token}

        }).then(
            // SUCCESS
            function(response) {
                setAlert("Group created.", true);
                getGroups();
                setTimeout(function(){ window.location = "./index.html#!/groups";}, 500);
            },
            // ERROR
            function(response){
                if (response.status == 400 && response.data.name!=undefined){
                    // TODO: improve server-side
                    setAlert("Group "+group.name+" already exists.", false);
                } else {
                    setAlert("Error.", false);
                }
            }
        );
    }

    // Edit a group
    $scope.save_changes = function(group) {

        console.log("Updating group");

        if( /\s/.test(group.name) ){
            setAlert("Error: Blank spaces not allowed.", false); 
            return;
        }

        if(group.instances.length<2){
            setAlert("Error: Single instance group not allowed.", false); 
            return;
        }

        // Creating FormData
        fd =  new FormData();
        fd.append('name', group.name)

        for(var i=0; i<group.instances.length; i++)  
            fd.append('instances', group.instances[i]);

        // Send a PUT request
        $http({
            method: 'PUT',
            url:   API.group+$scope.group_id+"/",
            data:  fd,
            headers: {'Content-Type': undefined,
                      'Authorization': 'Token '+$rootScope.logged_user.token}

        }).then(
            // SUCCESS
            function(response) {
                setAlert("Saved.", true);
                setTimeout(
                    function(){
                        window.location = "./index.html#!/groups/edit/"+group.name;
                    }, 1000)
                ;
            },
            // ERROR
            function(response){
                if (response.status == 400 && response.data.name!=undefined){
                    // TODO: improve server-side
                    setAlert("Group "+group.name+" already exists.", false);
                } else {
                    setAlert("Error.", false);
                }
            }
        );
    }

    // Delete a group
    $scope.delete = function(group_id) {

        console.log("Deleting group");

        if( confirm("You are going to delete this group.") ) {

            $http({
                method: 'DELETE',
                url:   API.group+group_id+"/",
                headers: {'Content-Type': undefined,
                          'Authorization': 'Token '+$rootScope.logged_user.token}

            }).then(
                // SUCCESS
                function(response) {
                    setAlert("Deleted.", true);

                    setTimeout(function(){window.location = "./index.html#!/groups/";}, 1000);
                },
                // ERROR
                function(response){
                    setAlert("Error deleting.", false);
                }
            );
        }

    }

    /* # Multi-selection support functions # */
    $scope.moveItems = function(items, destination) {

        if(items!=undefined) {
            for(var i=0; i<items.length; i++) {
                if(!destination.includes(items[i].trim()))
                    destination.push(items[i].trim());
            }
        }
    }

    $scope.deleteItem = function(item, from) {
        return from.filter(function(el){return el!=item});
    }

    /* # Initialization # */

    $scope.active_menu = "groups";

    view = $location.path();

    if("groupId" in $routeParams)
        $scope.group_id =$routeParams.groupId

    $scope.groups = [];

    // Initialization based on the current view
    if (view == "/groups")
        getGroups();

    if (view == "/groups/create" || view.startsWith("/groups/edit")) {
        getInstances();

        if (view == "/groups/create") {
            $scope.group = { instances:[$rootScope.logged_user.instancename]};
        } else if( view.startsWith("/groups/edit") ) {

            $http({
                method: 'GET',
                url:   API.group+$scope.group_id+"/",
                headers: {'Authorization': 'Token '+$rootScope.logged_user.token}

            }).then(
                // SUCCESS
                function(response) {
                    $scope.group = response.data;
                },
                // ERROR
                function(response){
                    console.error("Error retrieving group "+$scope.group_id);
                }
            );

        }
    }



});
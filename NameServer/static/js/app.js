var app = angular.module('app',['ngRoute']);
app.config(['$routeProvider', '$locationProvider',
  function($routeProvider, $locationProvider) {

    $routeProvider
      .when('/login', {
        templateUrl: 'views/login.html',
        controller: 'login_ctrl',
        controllerAs: 'lg'
      })
      .when('/signup', {
        templateUrl: 'views/signup.html',
        controller: 'signup_ctrl',
        controllerAs: 'signup'
      })
      .when('/home', {
        templateUrl: 'views/home.html',
        controller: 'home_ctrl',
        controllerAs: 'home'
      })
      .when('/datasets', {
        templateUrl: 'views/datasets.html',
        controller: 'datasets_ctrl',
        controllerAs: 'dsc'
      })
      .when('/datasets/create', {
        templateUrl: 'views/createDataset.html',
        controller: 'datasets_ctrl',
        controllerAs: 'dsc'
      })
      .when('/datasets/edit/:datasetId', {
        templateUrl: 'views/editDataset.html',
        controller: 'datasets_ctrl',
        controllerAs: 'dsc'
      })
      .when('/instances', {
        templateUrl: 'views/instances.html',
        controller: 'instances_ctrl',
        controllerAs: 'isc'
      })
      .when('/groups', {
        templateUrl: 'views/groups.html',
        controller: 'groups_ctrl',
        controllerAs: 'gpc'
      })
      .when('/groups/create', {
        templateUrl: 'views/createGroup.html',
        controller: 'groups_ctrl',
        controllerAs: 'gpc'
      })
      .when('/groups/edit/:groupId', {
        templateUrl: 'views/editGroup.html',
        controller: 'groups_ctrl',
        controllerAs: 'gpc'
      }).otherwise({redirectTo : '/home'});
   

    //$locationProvider.html5Mode(true);
}]);
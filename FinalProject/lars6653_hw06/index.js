// YOU CAN USE THIS FILE AS REFERENCE FOR SERVER DEVELOPMENT

// include the express modules
var express = require("express");

// create an express application
var app = express();
const url = require('url');

// helps in extracting the body portion of an incoming request stream
var bodyparser = require('body-parser'); // this has been depricated, is now part of express...

// got this from the internet to make post request work without using fetch
app.use(bodyparser.urlencoded({ 
  extended: true 
})); 

// fs module - provides an API for interacting with the file system
var fs = require("fs");

// helps in managing user sessions
var session = require('express-session');

// include the mysql module
var mysql = require("mysql");

// Bcrypt library for comparing password hashes
const bcrypt = require('bcrypt');

// Pug library
var pug = require('pug');

// A possible library to help reading uploaded file.
// var formidable = require('formidable')


// apply the body-parser middleware to all incoming requests
app.use(bodyparser.json());

// use express-session
// in mremory session is sufficient for this assignment
app.use(session({
  secret: "csci4131secretkey",
  saveUninitialized: true,
  resave: false
}
));

// server listens on port 9007 for incoming connections
app.listen(9007, () => console.log('Listening on port 9007!'));



// sql connection setup
var dbConn = mysql.createConnection({
  host: "cse-mysql-classes-01.cse.umn.edu",
  user: "C4131S24DU57",
  password: "3299",
  database: "C4131S24DU57",
  port: 3306
});

dbConn.connect(function(err) {
  if (err) {
    throw err;
  };
  console.log("Connected to MYSQL database!");
});



// Functions to return pages
app.get('/', function(req, res) {
  // res.sendFile(__dirname + '/static/html/welcome.html');
  renderPugFile('welcome', res);
});

app.get('/addEvent', function(req, res) {
  if (!req.session.value) {
    res.redirect('/login');
  } else {
    // res.sendFile(__dirname + '/static/html/addEvent.html');
    renderPugFile('addEvent', res);
  }
})

app.get('/login', function(req, res) {
  // res.sendFile(__dirname + '/static/html/login.html');
  renderPugFile('login', res);
});

app.get('/schedule', function(req, res) {
  if (!req.session.value) {
    res.redirect('/login');
  } else {
    // res.sendFile(__dirname + '/static/html/schedule.html');
    renderPugFile('schedule', res);
  }
})



// Verify login credentials
app.post('/verifyLogin', function(req, res) {
  // Get the username and password
  var username = req.body.username;
  var password = req.body.password;
  console.log("credentials: " + username + " " + password);

  // Query the DB to verify the password
  dbConn.query('SELECT * FROM tbl_accounts WHERE acc_login=?', username, (err, results) => {
    console.log(results);

    var passwordHash;
    if (results.length != 0) {
      passwordHash = results[0].acc_password;
      console.log(passwordHash);
    } else {
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ status: false }));
      return;
    }

    // Compare the given password hashed to the hash from the DB
    bcrypt.compare(password, passwordHash, function(err, result) {
      var status = { status: result };
      console.log(status);

      res.setHeader('Content-Type', 'application/json');
      if (result) {
        req.session.value = 1;
        res.end(JSON.stringify(status));
      } else {
        res.end(JSON.stringify(status));
      }
    });
  });
});



// Get schedule events
app.post('/getSchedule', function(req, res) {
  console.log(req.body);
  var day = req.body.day;
  
  // Do nothing if not logged in
  if (!req.session.value) { return; }

  dbConn.query('SELECT * FROM tbl_events WHERE event_day=?', day, (err, results) => {
    if (results.length == 0) { return; }

    // Create a JSON object with an empty list for the day
    var eventsJSON = {};
    eventsJSON[day] = [];

    // Add all the events to the day's list
    results.forEach(event => {
      // Create a new JSON object for the event
      var eventJSON = {
        event: event.event_event,
        day: event.event_day,
        start: event.event_start,
        end: event.event_end,
        phone: event.event_phone,
        location: event.event_location,
        info: event.event_info,
        url: event.event_url
      }
      
      // Find where to place the new event in the day's event list
      var i = 0;
      for (const existingEvent of eventsJSON[day]) {
        if (existingEvent.start < event.start) {
          i++;
        } else {
          break;
        }
      }

      // Place the new event in the day's event list
      eventsJSON[day].splice(i, 0, eventJSON);
    });
    console.log(eventsJSON);

    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(eventsJSON));
  });
})



// Add a new event to the user's events DB
app.post('/postEventEntry', function(req, res) {
  console.log(req.body);

  var rowToBeInserted = {
    event_day: req.body.day,
    event_event: req.body.event,
    event_start: req.body.start,
    event_end: req.body.end,
    event_location: req.body.location,
    event_phone: req.body.phone,
    event_info: req.body.info,
    event_url: req.body.url
  };

  dbConn.query('INSERT tbl_events SET ?', rowToBeInserted, function(err, result) {
    console.log(result);
  });
})



// Logout functionality
app.post('/logout', function(req, res) {
  req.session.destroy();
  res.redirect('/login');
})



// middle ware to serve static files
app.use('/static', express.static(__dirname + '/static'));

// function to return the 404 message and error to client
app.get('*', function(req, res) {
  // add details
  res.sendStatus(404);
});



// Render a pug file
function renderPugFile(file, res) {
  var filePath = 'static/html/' + file + '.pug';
  pug.renderFile(filePath, function(err, result) {
    if (err) { console.error(err) }
    res.send(result);
  });
}

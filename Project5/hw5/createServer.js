const http = require('http');
const url = require('url');
const fs = require('fs');
const qs = require('querystring');

const port = 4131;
http.createServer(function(req, res) {
  var q = url.parse(req.url, true);
  if (q.pathname === '/') {
    indexPage(req, res);
  }
  else if (q.pathname === '/index.html') {
    indexPage(req, res);
  }
  else if (q.pathname === '/schedule.html') {
    schedulePage(req, res);
  }
  else if (q.pathname === '/addEvent.html') {
    addEventPage(req, res);
  }
  else if (q.pathname === '/postEventEntry') {
    addNewEvent(req, res);
  }
  else if (q.pathname === '/getSchedule') {
    getSchedule(req, res, q.query);
  }
  else {
    res.writeHead(404, { 'Content-Type': 'text/html' });
    return res.end("404 Not Found");
  }
}).listen(port);


function getSchedule(req, res, query) {
  var reqBody = '';
  
  req.on('data', function(data) {
    reqBody += data;
  }); 
  
  req.on('end', function() {
    const day = query.day;
    console.log(day);

    fs.readFile('schedule.json', (err, data) => {
      if (err) { throw err; }
      const schedule = JSON.parse(data);
      const eventsList = schedule[day];
    
      // Send the eventsList to the client
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify(eventsList));
    });
    
  });
}


function addNewEvent(req, res) {
  var reqBody = '';
  
  req.on('data', function(data) {
    reqBody += data;
  }); 
  
  req.on('end', function() {
    const params = new URLSearchParams(reqBody);

    // Convert the form input into JSON
    var paramsJSON = {}
    for (const [key, value] of params) {
      paramsJSON[key] = value;
    }

    fs.readFile("schedule.json", (err, data) => {
      if (err) { throw err; }
      const schedule = JSON.parse(data);
  
      // Find where to place the new event in the day's event list
      var i = 0;
      for (const event of schedule[paramsJSON.day.toLowerCase()]) {
        if (event.start < paramsJSON.start) {
          i++;
        } else {
          break;
        }
      }

      // Place the new event in the day's event list
      schedule[paramsJSON.day.toLowerCase()].splice(i, 0, paramsJSON);

      // Write the updated JSON to the file
      fs.writeFile("schedule.json", JSON.stringify(schedule, null, 2), (err) => {
        if (err) { throw err; }
        schedulePage(req, res);
      });
    });
  });
}


function indexPage(req, res) {
  fs.readFile('static/html/index.html', (err, html) => {
    if (err) {
      throw err;
    }
    res.statusCode = 200;
    res.setHeader('Content-type', 'text/html');
    res.write(html);
    res.end();
  });
}


function schedulePage(req, res) {
  fs.readFile('static/html/schedule.html', (err, html) => {
    if (err) {
      throw err;
    }
    res.statusCode = 200;
    res.setHeader('Content-type', 'text/html');
    res.write(html);
    res.end();
  });
}


function addEventPage(req, res) {
  fs.readFile('static/html/addEvent.html', (err, html) => {
    if (err) {
      throw err;
    }
    res.statusCode = 200;
    res.setHeader('Content-type', 'text/html');
    res.write(html);
    res.end();
  });
}

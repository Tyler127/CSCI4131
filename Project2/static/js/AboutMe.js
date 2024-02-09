function updateClock() {
    console.log('updating clock');
    var date = new Date();
    document.getElementById('hours').innerHTML = date.getHours() % 12;
    document.getElementById('minutes').innerHTML = date.getMinutes();
    document.getElementById('seconds').innerHTML = date.getSeconds();
    document.getElementById('ampm').innerHTML = (date.getHours() % 12 > 0) ? "AM" : "PM";
}

window.onload = function() {
    console.log('window loaded');
    var intervalClock = setInterval(updateClock, 1000);
};

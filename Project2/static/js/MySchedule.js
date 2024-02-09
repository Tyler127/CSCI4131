/* MY SCHEDULE */
function updateImage(imageName) {
    console.log('image hovered: ' + imageName);

    image = document.getElementById('myScheduleImg');

    switch (imageName) {
        case 'anderson':
            image.setAttribute('src', '/img/anderson.jpg');
            break;
        
        // TODO:
        case 'akerman':
            image.setAttribute('src', '/img/akerman.jpg');
            break;

        case 'rec':
            image.setAttribute('src', '/img/rec.jpg');
            break;

        // TODO:
        case 'smith':
            image.setAttribute('src', '/img/smith.jpg');
            break;

        case 'tate':
            image.setAttribute('src', '/img/Tate.png');
            break;
        
        case 'walter':
            image.setAttribute('src', '/img/walter.jpg');
            break;

        case 'zoom':
            image.setAttribute('src', '/img/zoom.jpg');
            break;
    }

    image.setAttribute('height', '500px');
    image.setAttribute('width', '500px');
}

/* ABOUT ME */
document.addEventListener("DOMContentLoaded", function() {
    // Your JavaScript code here
    console.log("DOM content loaded");
});
$('#search').click(getEvents);

function getEvents() {
    let eventName = $('#eventGiven').val();
    let cityName = $('#cityGiven').val();
    const sortOrder = 'date,desc';

    if (eventName === '') {
        $('#alert').show().text('Search term cannot be empty. Please enter a search term.');
    } else if (cityName === '') {
        $('#alert').show().text('City cannot be empty. Please enter a city.');
    } else {
        $('#alert').css('display', 'none');
        $('#alertBottom').css('display', 'none');
    }
}

function getCookie(c_name){
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start !== -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end === -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

$('a').click(saveEvent);

function saveEvent(){
    const username = $('#username').text();
    const id = $(this).attr('id');
    const eventName = $('#event' + id).text();
    const eventUrl = $('#find' + id).attr('href');
    const imageUrl = $('#image' + id).attr('src');
    const date = $('#date' + id).text();
    const time = $('#time' + id).text();
    const venue = $('#location' + id).text();
    const address = $('#address' + id).text();
    const cityState = $('#state' + id).text().split(', ');
    const state = cityState[1]
    const city = cityState[0];
    const urlUsed = 'http://127.0.0.1:8000/add'
    
    const body = {
        user: username,
        event_name: eventName,
        event_url: eventUrl,
        image_url: imageUrl,
        event_date: date,
        event_time: time,
        event_venue: venue,
        event_address: address,
        event_state: state,
        event_city: city,
    };

    $.ajax({
        type: "POST",
        url: urlUsed,
        data: body,
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        success: function (data) {
            console.log(body);
            console.log(urlUsed);
        }
    })
}

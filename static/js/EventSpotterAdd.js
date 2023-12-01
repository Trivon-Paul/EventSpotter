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
    const eventName = $('#section_add_event' + id).text();
    const eventUrl = $('#section_add_find' + id).attr('href');
    const imageUrl = $('#section_add_image' + id).attr('src');
    const date = $('#section_add_date' + id).text();
    const time = $('#section_add_time' + id).text();
    const venue = $('#section_add_location' + id).text();
    const address = $('#section_add_address' + id).text();
    const cityState = $('#section_add_state' + id).text().split(', ');
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

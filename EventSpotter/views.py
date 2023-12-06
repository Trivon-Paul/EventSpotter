from random import randint

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from requests import get

from EventSpotter.forms import SearchForm, EventsSavedForm, LocationForm
from EventSpotter.models import EventsSaved, Location


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'EventSpotter/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            location = Location(user=form.cleaned_data['username'], location='blank')
            location.save()
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'EventSpotter/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'EventSpotter/logout.html')


def event_search(keyword, city):
    try:
        url = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=KslWGouXriRWRSAPuh4pA43xDblNVF1f"
        parameters = {"keyword": keyword,
                      "city": city,
                      "sort": "date,asc"}
        data = get(url, params=parameters)
        return data.json()
    except:
        url = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=KslWGouXriRWRSAPuh4pA43xDblNVF1f"
        parameters = {"keyword": keyword,
                      "city": city,
                      "sort": "date,asc"}
        data = get(url, params=parameters)
        return data.json()


def parse_data(data):
    events_array = data["_embedded"]["events"]
    number_of_events = len(events_array)
    events = []
    urls = []
    image_urls = []
    dates = []
    times = []
    venues = []
    addresses = []
    states = []
    cities = []

    for i in range(1, number_of_events):
        try:
            events.append(events_array[i]["name"])
            urls.append(events_array[i]["url"])
            image_urls.append(events_array[i]["images"][1]["url"])
            dates.append(events_array[i]["dates"]["start"]["localDate"])
            times.append(time_convert(events_array[i]["dates"]["start"]["localTime"]))
            venues.append(events_array[i]["_embedded"]["venues"][0]["name"])
            addresses.append(events_array[i]["_embedded"]["venues"][0]["address"]["line1"])
            states.append(events_array[i]["_embedded"]["venues"][0]["state"]["stateCode"])
            cities.append(events_array[i]["_embedded"]["venues"][0]["city"]["name"])
        except:
            return events, urls, image_urls, dates, times, venues, addresses, states, cities

    return events, urls, image_urls, dates, times, venues, addresses, states, cities


def time_convert(time_in):
    hour = int(str(time_in[0]) + str(time_in[1]))
    minutes = time_in[3] + time_in[4]

    if hour == 24:
        return str(hour - 12) + ':' + minutes + ' AM'
    elif hour > 11:
        return str(hour - 12) + ':' + minutes + ' PM'
    else:
        return str(hour) + ':' + minutes + ' AM'


@login_required(login_url='/EventSpotter/login')
def index(request):
    username = str(request.user).capitalize()
    events_saved = EventsSaved.objects.filter(user=request.user).values()
    locations = ['New York City', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio',
                 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'San Francisco', 'Indianapolis',
                 'Columbus', 'Charlotte', 'Seattle', 'Washington', 'Boston']
    keywords = ['dance', 'music', 'art', 'comedy', 'concert']
    location_get = locations[randint(0, len(locations) - 1)]
    keyword_get = keywords[randint(0, len(keywords) - 1)]
    location_saved = Location.objects.filter(user=request.user)
    if location_saved.exists() and location_saved.values().first().get('location') != 'blank':
        try:
            events, urls, image_urls, dates, times, venues, addresses, states, cities = (
                parse_data(event_search(keyword_get, location_saved.values().first().get('location'))))
            number_of_events = range(0, len(events))
            content = {'eventName': events, 'urls': urls, 'image_urls': image_urls, 'dates': dates,
                       'times': times, 'venues': venues, 'addresses': addresses, 'states': states,
                       'cities': cities, 'length': number_of_events, 'user': username, 'events': events_saved,
                       'username': request.user}
            return render(request, 'EventSpotter/index.html', content)
        except:
            events, urls, image_urls, dates, times, venues, addresses, states, cities = (
                parse_data(event_search(keyword_get, location_get)))
            number_of_events = range(0, len(events))
            content = {'eventName': events, 'urls': urls, 'image_urls': image_urls, 'dates': dates,
                       'times': times, 'venues': venues, 'addresses': addresses, 'states': states,
                       'cities': cities, 'length': number_of_events, 'user': username, 'events': events_saved,
                       'username': request.user}
            return render(request, 'EventSpotter/index.html', content)

    events, urls, image_urls, dates, times, venues, addresses, states, cities = (
        parse_data(event_search(keyword_get, location_get)))
    number_of_events = range(0, len(events))
    content = {'eventName': events, 'urls': urls, 'image_urls': image_urls, 'dates': dates,
               'times': times, 'venues': venues, 'addresses': addresses, 'states': states,
               'cities': cities, 'length': number_of_events, 'user': username, 'events': events_saved,
               'username': request.user}
    return render(request, 'EventSpotter/index.html', content)


@login_required(login_url='/EventSpotter/login')
def search_view(request):
    form = SearchForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            location_get = form.cleaned_data["location"]
            keyword_get = form.cleaned_data["keyword"]
            try:
                events, urls, image_urls, dates, times, venues, addresses, states, cities = (
                    parse_data(event_search(keyword_get, location_get)))
                number_of_events = range(0, len(events))
                content = {'events': events, 'urls': urls, 'image_urls': image_urls, 'dates': dates,
                           'times': times, 'venues': venues, 'addresses': addresses, 'states': states,
                           'cities': cities, 'length': number_of_events, 'username': request.user}
                return render(request, 'EventSpotter/results.html', context=content)
            except:
                return render(request, 'EventSpotter/results.html', {'found': "false"})
    return render(request, 'EventSpotter/search.html', {'form': form})


def results_view(request):
    return render(request, 'EventSpotter/results.html', {'username': request.user})


def location_view(request):
    form = LocationForm(request.POST or None)
    if request.method == 'POST':
        form = LocationForm(request.POST)

        if form.is_valid():
            location_used = Location.objects.filter(user=request.user).first()
            location_used.location = form.cleaned_data['location']
            location_used.save()
            return redirect('index')
    return render(request, 'EventSpotter/location.html', {'form': form})


def about_view(request):
    return render(request, 'EventSpotter/about.html')


@login_required(login_url='/EventSpotter/login')
def add_view(request):
    content = EventsSavedForm(request.POST or None)
    if content.is_valid():
        content.save()
        redirect('saved')
    events_saved = EventsSaved.objects.all()
    content = {'events': events_saved}
    return render(request, 'EventSpotter/saved.html', content)


@login_required(login_url='/EventSpotter/login')
def events_saved_view(request):
    events_saved = EventsSaved.objects.filter(user=request.user).values()
    content = {'events': events_saved}
    return render(request, 'EventSpotter/saved.html', content)


@login_required(login_url='/EventSpotter/login')
def delete_view(request, event_id):
    event = EventsSaved.objects.get(id=event_id)
    event.delete()
    events_saved = EventsSaved.objects.all()
    content = {'events': events_saved}
    return render(request, 'EventSpotter/saved.html', content)

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
import requests

from EventSpotter.forms import SearchForm, EventsSavedForm
from EventSpotter.models import EventsSaved


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
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'EventSpotter/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'EventSpotter/logout.html')


def event_search(keyword, city):
    url = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=KslWGouXriRWRSAPuh4pA43xDblNVF1f"
    parameters = {"keyword": keyword,
                  "city": city,
                  "sort": "date,asc"}
    data = requests.get(url, params=parameters)
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
        events.append(events_array[i]["name"])
        urls.append(events_array[i]["url"])
        image_urls.append(events_array[i]["images"][1]["url"])
        dates.append(events_array[i]["dates"]["start"]["localDate"])
        times.append(time_convert(events_array[i]["dates"]["start"]["localTime"]))
        venues.append(events_array[i]["_embedded"]["venues"][0]["name"])
        addresses.append(events_array[i]["_embedded"]["venues"][0]["address"]["line1"])
        states.append(events_array[i]["_embedded"]["venues"][0]["state"]["stateCode"])
        cities.append(events_array[i]["_embedded"]["venues"][0]["city"]["name"])

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
    return render(request, 'EventSpotter/index.html')


@login_required(login_url='/EventSpotter/login')
def search_view(request):
    form = SearchForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            location_get = form.cleaned_data["location"]
            keyword_get = form.cleaned_data["keyword"]
            events, urls, image_urls, dates, times, venues, addresses, states, cities = (
                parse_data(event_search(keyword_get, location_get)))
            number_of_events = range(0, len(events))
            content = {'events': events, 'urls': urls, 'image_urls': image_urls, 'dates': dates,
                       'times': times, 'venues': venues, 'addresses': addresses, 'states': states,
                       'cities': cities, 'length': number_of_events}
            return render(request, 'EventSpotter/Results.html', context=content)
    return render(request, 'EventSpotter/search.html', {'form': form})


def results_view(request):
    return render(request, 'EventSpotter/results.html', {'user': request.user})


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

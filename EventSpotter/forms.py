from django import forms
from .models import Search
from .models import EventsSaved


class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ['keyword', 'location']
        labels = {
            "keyword": "",
            "location": ""
        }
        widgets = {
            'keyword': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by genre, artist, or '
                                                                                      'event'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a city e.g., Hartford'})
        }


class EventsSavedForm(forms.ModelForm):
    class Meta:
        model = EventsSaved
        fields = ['user', 'event_name', 'event_url', 'image_url', 'event_date', 'event_time', 'event_venue',
                  'event_address', 'event_state', 'event_city']

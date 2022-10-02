from django import forms

class IndexForm(forms.Form):
    from_place = forms.CharField(label='From', max_length=100)
    # from_place = forms.ModelChoiceField(label='From', queryset=Airport.objects.all())
    to_place = forms.CharField(label='To', max_length=100)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),label="Date")
    flight_class = forms.CharField(label="Class", max_length=10)
    # no_adults = forms.IntegerField(label="Adult")
    # no_children = forms.IntegerField(label="Children")

class BookingForm(forms.Form):
    no_adults = forms.IntegerField(label="Adult")
    no_children = forms.IntegerField(label="Children")


from django.forms import ModelForm
from models import Tournament

class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
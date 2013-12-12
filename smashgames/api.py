# myapp/api.py
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.validation import FormValidation
from models import Tournament
from forms import TournamentForm

class TournamentResource(ModelResource):
    class Meta:
        queryset = Tournament.objects.all()
        resource_name = 'tournament'
        authorization = Authorization()
        validation = FormValidation(form_class=TournamentForm)
        filtering = {'name': ['icontains']}
from django.views import generic
from django.db.models import Count

from .models import DTC, Phrase

class IndexView(generic.TemplateView):
    template_name = 'nd/index.html'

class PhraseView(generic.ListView):
    template_name = 'nd/phrase.html'
    def get_queryset(self):
        return Phrase.objects.raw('SELECT *, COUNT(*) AS count FROM nd_phrase GROUP BY text, file, page ORDER BY count DESC')

class DtcList(generic.ListView):
    template_name = 'nd/dtc_list.html'
    def get_queryset(self):
        return DTC.objects.annotate(count=Count('causes'))

class DtcDetail(generic.DetailView):
    model = DTC
    template_name = 'nd/dtc_detail.html'

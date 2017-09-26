from django.views import generic
from django.db.models import Count

from .models import Phrase

class IndexView(generic.ListView):
    template_name = 'nd/index.html'

    def get_queryset(self):
        return Phrase.objects.raw('SELECT *, COUNT(*) AS count FROM nd_phrase GROUP BY text, file, page ORDER BY count DESC')

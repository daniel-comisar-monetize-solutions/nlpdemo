from .models import Cause, DTC, Fix, Part, Phrase
from django import forms
from django.db.models import Count, Q
from django.shortcuts import redirect, reverse
from django.views import generic

class CauseDetail(generic.DetailView):
    model = Cause
    template_name = 'nd/cause_detail.html'

class CauseList(generic.ListView):
    model = Cause
    template_name = 'nd/cause_list.html'

class DtcDetail(generic.DetailView):
    model = DTC
    template_name = 'nd/dtc_detail.html'

class DtcList(generic.ListView):
    template_name = 'nd/dtc_list.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return DTC.objects.filter(Q(code__icontains=query) | Q(bmw_code__icontains=query))
        else:
            return DTC.objects.all()

class DtcSearchView(generic.edit.FormView):
    class DtcSearchForm(forms.Form):
        query = forms.CharField()
    form_class = DtcSearchForm
    template_name = 'nd/dtc_search.html'
    def form_valid(self, form):
        return redirect('{}?q={}'.format(reverse('nd:dtc_list'), form.cleaned_data['query']))

class FixDetail(generic.DetailView):
    model = Fix
    template_name = 'nd/fix_detail.html'

class FixList(generic.ListView):
    model = Fix
    template_name = 'nd/fix_list.html'

class PartDetail(generic.DetailView):
    model = Part
    template_name = 'nd/part_detail.html'

class PartList(generic.ListView):
    model = Part
    template_name = 'nd/part_list.html'

class IndexView(generic.TemplateView):
    template_name = 'nd/index.html'

class PhraseView(generic.ListView):
    template_name = 'nd/phrase.html'
    def get_queryset(self):
        return Phrase.objects.raw('SELECT *, COUNT(*) AS count FROM nd_phrase GROUP BY text, file, page ORDER BY count DESC')

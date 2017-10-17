from django.conf.urls import url

from . import views

app_name = 'nd'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^cause$', views.CauseList.as_view(), name='cause_list'),
    url(r'^cause/(?P<pk>\d+)$', views.CauseDetail.as_view(), name='cause_detail'),
    url(r'^dtc$', views.DtcList.as_view(), name='dtc_list'),
    url(r'^dtc/(?P<pk>\w{5})$', views.DtcDetail.as_view(), name='dtc_detail'),
    url(r'^dtc/search$', views.DtcSearchView.as_view(), name='dtc_search'),
    url(r'^fix$', views.FixList.as_view(), name='fix_list'),
    url(r'^fix/(?P<pk>\d+)$', views.FixDetail.as_view(), name='fix_detail'),
    url(r'^part$', views.PartList.as_view(), name='part_list'),
    url(r'^part/(?P<pk>\d+)$', views.PartDetail.as_view(), name='part_detail'),
    url(r'^phrase$', views.PhraseList.as_view(), name='phrase_list'),
    url(r'^phrase/(?P<pk>\d+)$', views.PhraseDetail.as_view(), name='phrase_detail'),
]

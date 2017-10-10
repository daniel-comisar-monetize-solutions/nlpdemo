from django.conf.urls import url

from . import views

app_name = 'nd'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^cause$', views.CauseList.as_view(), name='cause_list'),
    url(r'^cause/(?P<pk>\d+)$', views.CauseDetail.as_view(), name='cause_detail'),
    url(r'^dtc$', views.DtcList.as_view(), name='dtc_list'),
    url(r'^dtc/search$', views.DtcSearchView.as_view(), name='dtc_search'),
    url(r'^dtc/(?P<pk>[A-Za-z]\d{4,5})$', views.DtcDetail.as_view(), name='dtc_detail'),
    url(r'^fix$', views.FixList.as_view(), name='fix_list'),
    url(r'^fix/(?P<pk>\d+)$', views.FixDetail.as_view(), name='fix_detail'),
    url(r'^phrases$', views.PhraseView.as_view(), name='phrases'),
]

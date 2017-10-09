from django.conf.urls import url

from . import views

app_name = 'nd'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^causes$', views.CauseView.as_view(), name='causes'),
    url(r'^dtc$', views.DtcList.as_view(), name='dtc_list'),
    url(r'^dtc/search$', views.DtcSearchView.as_view(), name='dtc_search'),
    url(r'^dtc/(?P<pk>[A-Za-z][0-9]{4,5})$', views.DtcDetail.as_view(), name='dtc_detail'),
    url(r'^fixes$', views.FixView.as_view(), name='fixes'),
    url(r'^phrases$', views.PhraseView.as_view(), name='phrases'),
]

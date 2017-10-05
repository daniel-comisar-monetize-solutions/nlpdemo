from django.conf.urls import url

from . import views

app_name = 'nd'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^phrases$', views.PhraseView.as_view(), name='phrases'),
    url(r'^dtc$', views.DtcList.as_view(), name='dtc_list'),
    url(r'^dtc/(?P<pk>[A-Za-z][0-9]{4})$', views.DtcDetail.as_view(), name='dtc_detail'),
]

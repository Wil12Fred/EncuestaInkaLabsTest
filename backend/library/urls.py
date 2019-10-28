from django.conf.urls import url
from . import views
urlpatterns = [
    url('api/publisher/', views.PublisherListCreate.as_view() ),
    url('api/author/', views.AuthorListCreate.as_view() ),
    url('api/book/', views.BookListCreate.as_view() ),
    url(r'^api/author=(?P<pk>\d+)/detail/$',
        views.AuthorDetailView.as_view(), name = "author_detail"),
    url(r'^api/author=(?P<pk>\d+)/update/$',
        views.AuthorUpdateView.as_view(), name = "author_update"),
    url(r'^api/author=(?P<pk>\d+)/delete/$', 
        views.AuthorDeleteView.as_view(), name="delete_author"), 
    url(r'^api/authorpage$', 
        views.AuthorPageView.as_view(), name="page_author"), 
    url(r'^api/authorfilter$', 
        views.AuthorFilterView.as_view(), name="filter_author"), 
    url(r'^api/book=(?P<pk>\d+)/detail/$',
        views.BookDetailView.as_view(), name = "book_detail"),
    url(r'^api/book=(?P<pk>\d+)/update/$',
        views.BookUpdateView.as_view(), name = "book_update"),
    url(r'^api/book=(?P<pk>\d+)/delete/$', 
        views.BookDeleteView.as_view(), name="delete_book"), 
    url(r'^api/bookpage$', 
        views.BookPageView.as_view(), name="page_book"), 
    url(r'^api/bookfilter$', 
        views.BookFilterView.as_view(), name="filter_book")
]


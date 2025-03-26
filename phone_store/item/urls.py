from django.urls import path


from . import views

app_name = 'item'

urlpatterns = [
    path('', views.browse, name='browse'),
    path('new/', views.new, name='new'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('predictive_search/', views.predictive_search, name='predictive_search'),
    path("search_documents/", views.search_documents, name='search_documents'),

]
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views 
# Import views from the current app


urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/index.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('buy/', views.buy, name='buy'),
    path('item/<int:property_id>/', views.item_details, name='item_details'),  # Details page URL
    path('sell/', views.post_ad, name='sell'),
    path('post-ad/', views.post_ad, name='post_ad'),
    path('My_ads', views.My_ads, name='My_ads'),
    path('update/<int:property_id>', views.update_details, name='update'),
    path('delete/<int:property_id>', views.delete_ad, name='delete'), 
]
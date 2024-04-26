from django.urls import path
from .views import home,signup,user_login,createuser,logout,dashboard,stockdetails,removewatchlist

from .apis import search,watchlist,fetchdetails,graphdata

urlpatterns = [
    path('',home,name="home"),
    path('signup',signup,name="signup"),
    path('login',user_login,name="login"),
    path('createuser',createuser,name="createuser"),
    path('logout',logout,name="logout"),
    path('dashboard',dashboard,name="dashboard"),
    path('details/<str:query>',stockdetails,name="stockdetails"),
    path('removewatchlist/<str:symbol>',removewatchlist,name="removewatchlist"),
    path('api/search/<str:query>',search,name="search"),
    path('api/watchlist/<str:query>',watchlist,name="watchlist"),
    path('api/fetchdetails/<str:query>',fetchdetails,name="fetchdetails"),
    path('api/graphdata/<str:query>',graphdata,name="graphdata"),
]
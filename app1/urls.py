from django.urls import path
from . import views

from .apis import search,watchlist,fetchdetails,graphdata,portfolio,portfoliochart,income,holdings,addtoWatchlist

urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('login',views.user_login,name="login"),
    path('createuser',views.createuser,name="createuser"),
    path('logout',views.logout,name="logout"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('details/<str:query>',views.stockdetails,name="stockdetails"),
    path('removewatchlist/<str:symbol>',views.removewatchlist,name="removewatchlist"),
    path('portfolio',views.user_portfolio,name="user_portfolio"),
    path('updatestocks',views.updatestocks,name="updatestocks"),
    path('errorpage',views.errorpage,name="errorpage"),
    path('settings',views.settings,name="settings"),
    path('transactionHistory',views.transactionHistory,name="tHistory"),
    path('api/search/<str:query>',search,name="search"),
    path('api/watchlist/<str:query>',watchlist,name="watchlist"),
    path('api/addtowatchlist/<str:query>',addtoWatchlist,name="addtoWatchlist"),
    path('api/fetchdetails/<str:query>',fetchdetails,name="fetchdetails"),
    path('api/graphdata/<str:query>/<str:start>/<str:end>',graphdata,name="graphdata"),
    path('api/portfolio',portfolio,name="portfolio"),
    path('api/portfoliochart',portfoliochart,name="portfoliochart"),
    path('api/incomecalculate',income,name="income"),
    path('api/holdings/<str:query>',holdings,name="holdings"),
]
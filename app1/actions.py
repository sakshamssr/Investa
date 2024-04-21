from .models import users

name=users.objects.create(watchlist={"symbol":["aapl","goog","meta","msft","sony"]})
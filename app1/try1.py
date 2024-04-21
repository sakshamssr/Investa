from .models import users

user = users.objects.first()
user.watchlist={"symbol": ["msft", "meta", "goog", "aapl","sony"]}
user.save()
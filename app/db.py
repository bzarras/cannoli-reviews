import datetime
from app.models import Review


mock_data = [
    Review(
        title="Fortunato Bros",
        location="Brooklyn, NY",
        date=datetime.date(2023, 6,15),
        slug="fortunato-bros",
        summary="I first learned about Fortunato Bros two years ago when @bambambaklava featured them at his Williamsburg block party and proclaimed them the best cannoli in the world. The line was so long at the block party that I wound up just going straight to the actual bakery to try the cannoli. I was not disappointed.",
        liked="This is an excellent cannoli. The deep fried shell maintains a solid crunch and has a nice flavor, unlike the overly flaky and bland shells at Mike’s (sorry 😬). The filling is thick and has an authentic ricotta taste with just the right amount of sweetness. This cannoli feels like it was made with care, and it looks great with Fortunato’s signature star-tipped piping. Definitely worthy of being called one of NY’s best.",
        disliked="It’s hard to find faults with this one, but a few things to note are that the size can be a bit inconsistent (could be seen as a plus, proof that they’re hand-crafted), and they’re filled ahead of time, leaving you wondering how long they’ve been in the case (probably not too long though, because they’re always crunchy).",
        rating=9.1,
        tags=["cannoli", "williamsburg", "brooklyn", "nyc", "dessert", "pastry", "foodie", "fuckthatsdelicious"]
    )
] * 10


def get_all_reviews() -> list[Review]:
    return mock_data

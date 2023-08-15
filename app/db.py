import datetime
from app.models import Review


mock_data = [
    Review(
        title="Fortunato Bros",
        location="Brooklyn, NY",
        date=datetime.date(2023,6,15),
        slug="fortunato-bros",
        summary="I first learned about Fortunato Bros two years ago when @bambambaklava featured them at his Williamsburg block party and proclaimed them the best cannoli in the world. The line was so long at the block party that I wound up just going straight to the actual bakery to try the cannoli. I was not disappointed.",
        liked="This is an excellent cannoli. The deep fried shell maintains a solid crunch and has a nice flavor, unlike the overly flaky and bland shells at Mike’s (sorry 😬). The filling is thick and has an authentic ricotta taste with just the right amount of sweetness. This cannoli feels like it was made with care, and it looks great with Fortunato’s signature star-tipped piping. Definitely worthy of being called one of NY’s best.",
        disliked="It’s hard to find faults with this one, but a few things to note are that the size can be a bit inconsistent (could be seen as a plus, proof that they’re hand-crafted), and they’re filled ahead of time, leaving you wondering how long they’ve been in the case (probably not too long though, because they’re always crunchy).",
        rating=9.1,
        img_url="/static/fortunato_bros.jpg",
        tags=["cannoli", "williamsburg", "brooklyn", "nyc", "dessert", "pastry", "foodie", "fuckthatsdelicious"]
    ),
    Review(
        title="Bova's Bakery",
        location="Boston, MA",
        date=datetime.date(2023,6,4),
        slug="bovas",
        summary="Rounding out our North End cannoli tour was Bova’s Bakery!",
        liked="The cream was thick and sweet, the shell had a decent crunch to it, and there was a good ratio of chocolate chips. Overall it had the flavor profile that I look for in a cannoli.",
        disliked="This cannoli was the smallest of the three venerable North End bakeries. The shell was a tinyyy bit soft (likely because it had been sitting in the case) and there was definitely room for more cream. Where Bova’s shined was their Florentine cannoli, which tasted like toffee and was huge and very good overall. I would give a higher score if I were judging the Florentine, but gotta stick to the basics here.",
        rating=7.8,
        img_url="/static/bovas.jpg",
        tags=["cannoli", "northend", "boston", "northendboston", "massachusetts", "dessert", "foodie", "tasty", "foodporn", "dessertporn", "pastry", "fuckthatsdelicious"]
    )
] * 5


def get_all_reviews() -> list[Review]:
    return mock_data

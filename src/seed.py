from decimal import Decimal

from src.core.database import SessionLocal
from src.core.models import Product

PRODUCTS = [
    (
        "Red Roses Classic (15 stems)",
        "Fifteen long red roses wrapped in kraft paper. The timeless symbol of love, with a soft natural scent.",
        "59.00", 12, ["red"],
        ["romantic", "anniversary", "wife", "girlfriend", "classic", "luxury"],
    ),
    (
        "Pink Peony Cloud",
        "A full, fluffy bouquet of seven pink peonies. Gentle, romantic and very popular as a gift for women of any age.",
        "54.00", 8, ["pink"],
        ["birthday", "mothers_day", "mother", "grandmother", "elegant", "gentle_scent"],
    ),
    (
        "Grandma's Garden",
        "A soft mix of pastel carnations, freesia and white chrysanthemums. Easy to care for, long lasting, with a pleasant light scent. Our first choice for older ladies.",
        "38.00", 15, ["pink", "white", "lilac"],
        ["birthday", "grandmother", "mother", "mothers_day", "long_lasting", "gentle_scent", "classic"],
    ),
    (
        "Sunny Day Sunflowers",
        "Five bright sunflowers with greenery. Brings instant good mood and fits almost any cheerful occasion.",
        "29.00", 20, ["yellow"],
        ["birthday", "friend", "colleague", "congratulations", "get_well", "cheerful", "budget", "no_scent"],
    ),
    (
        "White Lilies Elegance",
        "Five large white lilies in a tall bouquet. Elegant and formal, with a strong, rich scent.",
        "45.00", 10, ["white"],
        ["sympathy", "wedding", "elegant", "luxury"],
    ),
    (
        "Pastel Tulip Spring",
        "Twenty-five tulips in soft pink, peach and cream. A light, fresh bouquet that feels like spring.",
        "34.00", 18, ["pink", "peach", "cream"],
        ["birthday", "mothers_day", "teacher", "mother", "grandmother", "cheerful", "no_scent"],
    ),
    (
        "Lavender Dream",
        "A fragrant bundle of fresh lavender with eucalyptus. Calming, rustic, and the scent lasts for weeks as it dries.",
        "27.00", 14, ["purple"],
        ["thank_you", "get_well", "grandmother", "friend", "housewarming", "long_lasting", "budget"],
    ),
    (
        "Orchid in Ceramic Pot",
        "A white phalaenopsis orchid in a hand-finished ceramic pot. Lasts for months with simple care, no scent, very low effort. Perfect for people who dislike fading bouquets.",
        "49.00", 9, ["white"],
        ["housewarming", "grandmother", "mother", "teacher", "elegant", "long_lasting", "no_scent", "minimal"],
    ),
    (
        "Mixed Spring Basket",
        "A woven basket with ranunculus, tulips, daffodils and fresh greenery. Ready to put on a table, no vase needed.",
        "42.00", 11, ["yellow", "pink", "white"],
        ["birthday", "mothers_day", "grandmother", "get_well", "cheerful", "gentle_scent"],
    ),
    (
        "Blush Rose Bouquet",
        "Twenty blush-pink roses with baby's breath. Soft, romantic and a little more modern than classic red.",
        "64.00", 7, ["pink"],
        ["anniversary", "romantic", "wife", "girlfriend", "elegant", "luxury"],
    ),
    (
        "Wedding White Collection",
        "Cream roses, white lisianthus and eucalyptus tied with a silk ribbon. Designed for brides and wedding tables.",
        "89.00", 4, ["white", "cream"],
        ["wedding", "luxury", "elegant"],
    ),
    (
        "Daisy Joy",
        "A cheerful armful of white and yellow daisies. Simple, honest and budget friendly.",
        "19.00", 25, ["white", "yellow"],
        ["friend", "thank_you", "colleague", "birthday", "cheerful", "budget", "no_scent"],
    ),
    (
        "Gerbera Rainbow",
        "Ten colorful gerberas in a bright mix. Big, happy flowers that last a long time in water.",
        "26.00", 16, ["red", "orange", "yellow", "pink"],
        ["birthday", "congratulations", "get_well", "new_baby", "cheerful", "long_lasting", "budget", "no_scent"],
    ),
    (
        "Baby Blue Hydrangea",
        "A lush bouquet of blue hydrangeas with soft greenery. Calm, delicate and different from the usual choices.",
        "46.00", 6, ["blue"],
        ["new_baby", "housewarming", "mother", "elegant", "no_scent"],
    ),
    (
        "Apology Roses",
        "Twelve soft peach and white roses. A gentle, sincere way to say sorry.",
        "48.00", 9, ["peach", "white"],
        ["apology", "girlfriend", "wife", "romantic", "gentle_scent"],
    ),
    (
        "Single Red Rose",
        "One long-stem red rose in a glass tube. Minimal and romantic when less is more.",
        "9.00", 40, ["red"],
        ["romantic", "minimal", "budget", "girlfriend"],
    ),
    (
        "Autumn Warmth",
        "Orange roses, rust chrysanthemums and golden solidago with dried leaves. Warm colors for autumn gifts.",
        "36.00", 10, ["orange", "yellow", "red"],
        ["thank_you", "birthday", "housewarming", "friend", "cheerful", "long_lasting"],
    ),
    (
        "Freesia Fragrance",
        "A delicate bunch of cream and lilac freesias. Light, sweet scent that fills a room.",
        "31.00", 13, ["cream", "lilac"],
        ["birthday", "grandmother", "mother", "mothers_day", "gentle_scent", "elegant"],
    ),
    (
        "Green Minimal Eucalyptus",
        "A modern bouquet of mixed eucalyptus and a few white anemones. Fresh and clean, with a light herbal scent.",
        "33.00", 8, ["green", "white"],
        ["housewarming", "colleague", "minimal", "elegant", "long_lasting"],
    ),
    (
        "Get Well Soon Box",
        "A small flower box with white and yellow chrysanthemums and daisies. Mild scent, sturdy flowers, easy to carry to a hospital room.",
        "32.00", 12, ["white", "yellow"],
        ["get_well", "grandmother", "friend", "colleague", "long_lasting", "gentle_scent", "no_scent"],
    ),
    (
        "Luxury Red & White Roses (40 stems)",
        "Forty premium roses in a hat box, red with white accents. For anniversaries and big gestures.",
        "149.00", 3, ["red", "white"],
        ["anniversary", "wedding", "romantic", "wife", "luxury"],
    ),
    (
        "Mini Succulent Trio",
        "Three small succulents in ceramic pots. Almost impossible to kill, perfect for desks and windowsills.",
        "22.00", 22, ["green"],
        ["colleague", "teacher", "thank_you", "housewarming", "minimal", "budget", "long_lasting", "no_scent"],
    ),
    (
        "Lilac Spring Armful",
        "Fresh-cut lilac branches with a very strong, sweet spring scent. Short season, limited stock.",
        "35.00", 0,  # out of stock on purpose: tests the in-stock filter
        ["lilac", "white"],
        ["mothers_day", "grandmother", "birthday", "elegant"],
    ),
    (
        "Teacher's Thank You Bouquet",
        "A bright bouquet of alstroemeria, daisies and statice. Cheerful, sturdy and fairly priced.",
        "24.00", 17, ["pink", "yellow", "purple"],
        ["teacher", "thank_you", "congratulations", "cheerful", "budget", "no_scent"],
    ),
]


def seed() -> None:
    db = SessionLocal()
    try:
        if db.query(Product).count() > 0:
            print("Products already exist, skipping seed.")
            return

        for name, description, price, stock, colors, tags in PRODUCTS:
            db.add(
                Product(
                    name=name,
                    description=description,
                    price=Decimal(price),
                    stock=stock,
                    colors=colors,
                    tags=tags,
                )
            )
        db.commit()
        print(f"Added {len(PRODUCTS)} products.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
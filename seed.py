#!/usr/bin/env python3
"""
Seed the database with sample Sri Lanka tourist attractions.
Run from the project root with the virtual environment active:
    python seed.py
"""
import sys
import uuid
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database import engine, SessionLocal, Base
from models import User, Attraction, AttractionImage, Comment
from auth import hash_password

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# Image download helper
# ---------------------------------------------------------------------------

def download_image(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            dest.write_bytes(resp.read())
        return True
    except Exception as e:
        print(f"  [warn] Could not download {url}: {e}")
        return False


# ---------------------------------------------------------------------------
# Seed data
# ---------------------------------------------------------------------------

USERS = [
    {"email": "demo@slexplore.com",   "password": "demo1234"},
    {"email": "amara@slexplore.com",  "password": "demo1234"},
]

ATTRACTIONS = [
    {
        "name": "Sigiriya Rock Fortress",
        "province": "Central Province",
        "district": "Matale",
        "latitude": 7.9572,
        "longitude": 80.7603,
        "img_url": "https://picsum.photos/id/29/800/550",
        "description": (
            "Rising 200 metres above the surrounding plains, Sigiriya is an ancient rock fortress "
            "and palace ruin built during the reign of King Kashyapa in the 5th century AD. "
            "The site features extensive remains of a former city, stunning frescoes, mirror-wall "
            "graffiti, and landscaped gardens considered among the oldest in the world. "
            "A UNESCO World Heritage Site and one of Sri Lanka's most iconic landmarks."
        ),
        "comments": [
            ("amara@slexplore.com", "Absolutely breathtaking! The climb is worth every step. Go early morning to avoid the heat and crowds."),
            ("demo@slexplore.com",  "The frescoes near the summit are incredible. One of the best historical sites I've visited in Asia."),
        ],
    },
    {
        "name": "Temple of the Sacred Tooth Relic",
        "province": "Central Province",
        "district": "Kandy",
        "latitude": 7.2936,
        "longitude": 80.6413,
        "img_url": "https://picsum.photos/id/159/800/550",
        "description": (
            "The Sri Dalada Maligawa, or Temple of the Tooth, is a sacred Buddhist temple in the royal "
            "palace complex of the former Kingdom of Kandy. It houses the relic of the tooth of the "
            "Buddha and is one of the most venerated sites in the Buddhist world. "
            "The temple is a UNESCO World Heritage Site and draws pilgrims and tourists from across the globe. "
            "The annual Kandy Esala Perahera festival held here is one of the grandest spectacles in Asia."
        ),
        "comments": [
            ("amara@slexplore.com", "The evening puja ceremony is mesmerizing. The drums and the golden casket are truly moving."),
        ],
    },
    {
        "name": "Galle Dutch Fort",
        "province": "Southern Province",
        "district": "Galle",
        "latitude": 6.0238,
        "longitude": 80.2170,
        "img_url": "https://picsum.photos/id/1015/800/550",
        "description": (
            "Built first in 1588 by the Portuguese and later fortified by the Dutch in the 17th century, "
            "Galle Fort is a UNESCO World Heritage Site and the largest remaining European fortress in Asia. "
            "Its ramparts offer stunning views of the Indian Ocean, while narrow cobblestone streets within "
            "are lined with colonial-era boutiques, cafés, art galleries, and historic churches. "
            "Walking the ramparts at sunset is considered one of Sri Lanka's quintessential experiences."
        ),
        "comments": [
            ("amara@slexplore.com", "Walking the ramparts at sunset is magical. Don't miss the lighthouse and the nearby cricket ground."),
            ("demo@slexplore.com",  "Great boutique cafes and shops inside. Perfect spot to spend a whole afternoon exploring."),
        ],
    },
    {
        "name": "Yala National Park",
        "province": "Southern Province",
        "district": "Hambantota",
        "latitude": 6.3731,
        "longitude": 81.5197,
        "img_url": "https://picsum.photos/id/582/800/550",
        "description": (
            "Sri Lanka's most visited national park, Yala is famous for having one of the highest leopard "
            "densities in the world. The park covers 979 km² of diverse ecosystems including scrub jungle, "
            "open woodland, and coastal lagoons. Visitors can spot elephants, sloth bears, crocodiles, "
            "and hundreds of bird species alongside the elusive Sri Lankan leopard. "
            "Morning jeep safaris offer the best chance of big cat sightings."
        ),
        "comments": [
            ("demo@slexplore.com", "Spotted 3 leopards in a single morning safari — absolutely incredible!"),
        ],
    },
    {
        "name": "Horton Plains & World's End",
        "province": "Central Province",
        "district": "Nuwara Eliya",
        "latitude": 6.8018,
        "longitude": 80.8031,
        "img_url": "https://picsum.photos/id/1018/800/550",
        "description": (
            "Horton Plains National Park is a UNESCO World Heritage Site covering a high-altitude "
            "plateau at over 2,100 metres above sea level. The centrepiece is World's End, a sheer "
            "cliff with an 880-metre drop offering breathtaking panoramic views over southern Sri Lanka. "
            "The misty landscape of montane grasslands and cloud forest is home to sambar deer, "
            "purple-faced langurs, and over 24 species of endemic birds."
        ),
        "comments": [
            ("demo@slexplore.com",  "Arrive before 8 AM before the clouds roll in. The drop at World's End is absolutely vertiginous!"),
            ("amara@slexplore.com", "The most beautiful morning hike I've ever done. Mist, rolling grasslands, and hidden waterfalls."),
        ],
    },
    {
        "name": "Polonnaruwa Ancient City",
        "province": "North Central Province",
        "district": "Polonnaruwa",
        "latitude": 7.9403,
        "longitude": 81.0188,
        "img_url": "https://picsum.photos/id/1011/800/550",
        "description": (
            "Polonnaruwa was the medieval capital of Sri Lanka from the 11th to 13th centuries. "
            "This UNESCO World Heritage Site contains some of the best-preserved ancient ruins in Asia, "
            "including the Gal Vihara — four magnificent Buddha statues carved from a single granite face. "
            "Royal palaces, bathing pools, and stunning stupas are spread across the vast archaeological park. "
            "Exploring by bicycle is the most popular and rewarding way to visit the site."
        ),
        "comments": [
            ("amara@slexplore.com", "Rent a bicycle to explore the grounds. The Gal Vihara rock statues are awe-inspiring in person."),
        ],
    },
    {
        "name": "Anuradhapura Sacred City",
        "province": "North Central Province",
        "district": "Anuradhapura",
        "latitude": 8.3114,
        "longitude": 80.4037,
        "img_url": "https://picsum.photos/id/137/800/550",
        "description": (
            "One of the ancient capitals of Sri Lanka and a UNESCO World Heritage Site, "
            "Anuradhapura is home to some of the world's oldest and tallest ancient brick monuments. "
            "The sacred Bodhi tree — grown from a cutting of the original tree under which the Buddha "
            "attained enlightenment — has been tended continuously for over 2,300 years, making it "
            "the oldest documented living tree in the world with a known planting date."
        ),
        "comments": [
            ("demo@slexplore.com",  "The scale of the stupas is humbling. Ruwanwelisaya is extraordinary at sunrise."),
            ("amara@slexplore.com", "A deeply spiritual place. The Bodhi tree at Jaya Sri Maha Bodhi is breathtaking."),
        ],
    },
    {
        "name": "Nine Arch Bridge, Ella",
        "province": "Uva Province",
        "district": "Badulla",
        "latitude": 6.8736,
        "longitude": 81.0460,
        "img_url": "https://picsum.photos/id/1047/800/550",
        "description": (
            "The Nine Arch Bridge in Ella is one of the most photographed landmarks in Sri Lanka. "
            "Built entirely from brick, stone, and cement without any steel during the British colonial era, "
            "this magnificent viaduct spans a lush valley surrounded by tea plantations and jungle. "
            "The best moment is when the scenic Kandy-Badulla train passes over the bridge, "
            "creating one of the most iconic travel photographs in all of Asia."
        ),
        "comments": [
            ("amara@slexplore.com", "Time your visit for when the train passes — an absolutely iconic shot. Check the timetable beforehand!"),
            ("demo@slexplore.com",  "Surrounded by tea estates and jungle. One of the most beautiful spots in Sri Lanka."),
        ],
    },
    {
        "name": "Mirissa Beach",
        "province": "Southern Province",
        "district": "Matara",
        "latitude": 5.9477,
        "longitude": 80.4567,
        "img_url": "https://picsum.photos/id/119/800/550",
        "description": (
            "Mirissa is a small beach town on the south coast of Sri Lanka, renowned for its crescent-shaped "
            "golden beach, turquoise waters, and vibrant cafe scene. It is one of the world's best "
            "destinations for whale watching — blue whales and sperm whales can be spotted offshore "
            "between November and April. The iconic Parrot Rock is a short swim from the main beach "
            "and offers panoramic views over the bay."
        ),
        "comments": [
            ("demo@slexplore.com", "The whale watching trip from Mirissa was the absolute highlight of our entire trip to Sri Lanka!"),
        ],
    },
    {
        "name": "Jaffna Fort",
        "province": "Northern Province",
        "district": "Jaffna",
        "latitude": 9.6611,
        "longitude": 80.0087,
        "img_url": "https://picsum.photos/id/1069/800/550",
        "description": (
            "Jaffna Fort is a historic fortification originally built by the Portuguese in 1618 and later "
            "expanded by the Dutch, making it one of the largest Dutch forts in Asia. "
            "Located on the Jaffna peninsula overlooking a saltwater lagoon, the fort's star-shaped "
            "ramparts are a fine example of European military architecture in South Asia. "
            "The surrounding peninsula offers a fascinating insight into the rich Tamil culture and heritage "
            "of northern Sri Lanka."
        ),
        "comments": [
            ("amara@slexplore.com", "The fort is massive and beautifully restored. The view from the ramparts over the lagoon is lovely."),
        ],
    },
    {
        "name": "Pigeon Island Marine National Park",
        "province": "Eastern Province",
        "district": "Trincomalee",
        "latitude": 8.8924,
        "longitude": 81.1776,
        "img_url": "https://picsum.photos/id/96/800/550",
        "description": (
            "Pigeon Island National Park off the coast of Nilaveli is one of Sri Lanka's finest "
            "snorkelling and diving destinations. The island's crystal-clear waters are home to "
            "vibrant coral gardens, blacktip reef sharks, sea turtles, moray eels, "
            "and hundreds of tropical fish species. The island itself is an important nesting site "
            "for the rock pigeon, giving it its distinctive name. Best visited between April and October."
        ),
        "comments": [
            ("demo@slexplore.com",  "The coral is stunning! Saw a reef shark on our first snorkel. Totally unmissable."),
            ("amara@slexplore.com", "Water so clear you can see the reef from the boat. Best snorkelling spot in Sri Lanka."),
        ],
    },
    {
        "name": "Adam's Peak (Sri Pada)",
        "province": "Sabaragamuwa Province",
        "district": "Ratnapura",
        "latitude": 6.8096,
        "longitude": 80.4994,
        "img_url": "https://picsum.photos/id/167/800/550",
        "description": (
            "Adam's Peak, known as Sri Pada, is a 2,243-metre conical mountain sacred to four major "
            "religions — Buddhism, Hinduism, Islam, and Christianity. At its summit lies the 'Sacred Footprint', "
            "venerated as the footprint of the Buddha, Shiva, Adam, or St. Thomas depending on one's faith. "
            "The pilgrimage season runs from December to May. The climb up thousands of illuminated steps "
            "is traditionally done at night to witness the spectacular sunrise from the summit."
        ),
        "comments": [
            ("demo@slexplore.com",  "Start the climb at 2 AM to reach the top for sunrise. The pyramid shadow cast at dawn is absolutely surreal."),
            ("amara@slexplore.com", "An incredible spiritual experience. The chain of lights going up the mountain at night is unforgettable."),
        ],
    },
]


# ---------------------------------------------------------------------------
# Main seeder
# ---------------------------------------------------------------------------

def seed():
    db = SessionLocal()
    try:
        # Skip if data already exists
        if db.query(Attraction).count() > 0:
            print("Database already has attractions. Skipping seed.")
            return

        print("Creating users...")
        user_map: dict[str, User] = {}
        for u in USERS:
            user = User(email=u["email"], hashed_password=hash_password(u["password"]))
            db.add(user)
            db.flush()
            user_map[u["email"]] = user
            print(f"  Created user: {u['email']}")

        print("\nCreating attractions and downloading images...")
        owner = user_map["demo@slexplore.com"]

        for idx, data in enumerate(ATTRACTIONS, 1):
            print(f"  [{idx:02d}/{len(ATTRACTIONS)}] {data['name']}")

            attr = Attraction(
                name=data["name"],
                province=data["province"],
                district=data["district"],
                description=data["description"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                user_id=owner.id,
            )
            db.add(attr)
            db.flush()

            # Download image
            ext = ".jpg"
            filename = f"{uuid.uuid4()}{ext}"
            dest = UPLOAD_DIR / filename
            ok = download_image(data["img_url"], dest)
            if ok:
                db.add(AttractionImage(attraction_id=attr.id, image_path=f"uploads/{filename}"))
                print(f"       Image saved: {filename}")
            else:
                print(f"       Skipped image (download failed)")

            # Add comments
            for commenter_email, content in data.get("comments", []):
                commenter = user_map.get(commenter_email, owner)
                db.add(Comment(
                    attraction_id=attr.id,
                    user_id=commenter.id,
                    content=content,
                ))

        db.commit()
        print(f"\nDone! Seeded {len(ATTRACTIONS)} attractions.")
        print("\nDemo login credentials:")
        for u in USERS:
            print(f"  Email: {u['email']}   Password: {u['password']}")

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed()

#!/usr/bin/env python3
"""Add 50 more attractions spread across all 9 provinces."""
import sys, uuid, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database import engine, SessionLocal, Base
from models import User, Attraction, AttractionImage, Comment

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
Base.metadata.create_all(bind=engine)


def download_image(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            dest.write_bytes(r.read())
        return True
    except Exception as e:
        print(f"  [warn] {url}: {e}")
        return False


ATTRACTIONS = [
    # ── WESTERN PROVINCE ─────────────────────────────────────────────────────
    {
        "name": "Gangaramaya Temple",
        "province": "Western Province", "district": "Colombo",
        "latitude": 6.9167, "longitude": 79.8567,
        "img": "https://picsum.photos/id/159/800/550",
        "description": (
            "One of Colombo's most important and eclectic temples, Gangaramaya blends Sri Lankan, "
            "Thai, Indian, and Chinese architectural styles. Founded in the late 19th century, the "
            "complex houses a museum crammed with Buddha statues, antique vehicles, tusked elephants "
            "and rare artefacts donated by devotees worldwide. The annual Navam Perahera — held on "
            "the full moon of February — is one of the largest processions in Sri Lanka."
        ),
        "comments": [("amara@slexplore.com", "A fascinating sensory overload of religious art and culture. Don't skip the museum inside.")],
    },
    {
        "name": "Galle Face Green",
        "province": "Western Province", "district": "Colombo",
        "latitude": 6.9178, "longitude": 79.8463,
        "img": "https://picsum.photos/id/1060/800/550",
        "description": (
            "Stretching 500 metres along the Indian Ocean in the heart of Colombo, Galle Face Green "
            "is the city's most beloved urban promenade. Laid out by the British in 1859, it remains "
            "a cherished gathering spot for locals and visitors alike. Families fly kites at sunset, "
            "street vendors sell spicy isso vadei (prawn fritters) and fresh coconut, and the "
            "sweeping ocean views across the Colombo harbour are simply spectacular."
        ),
        "comments": [("demo@slexplore.com", "Perfect sunset spot. Grab some isso vadei from the stalls — absolutely delicious!")],
    },
    {
        "name": "National Museum of Colombo",
        "province": "Western Province", "district": "Colombo",
        "latitude": 6.9024, "longitude": 79.8612,
        "img": "https://picsum.photos/id/301/800/550",
        "description": (
            "Founded in 1877, the National Museum of Colombo is the country's largest museum and "
            "an essential starting point for understanding Sri Lanka's rich history. Housed in a "
            "magnificent neo-classical white building in Viharamahadevi Park, its galleries contain "
            "the royal regalia of the last King of Kandy, ancient stone inscriptions, "
            "a remarkable collection of traditional masks, and artefacts spanning 2,500 years."
        ),
        "comments": [("amara@slexplore.com", "Excellent introduction to Sri Lankan history. The royal regalia collection is impressive.")],
    },
    {
        "name": "Beira Lake & Seema Malaka Temple",
        "province": "Western Province", "district": "Colombo",
        "latitude": 6.9172, "longitude": 79.8553,
        "img": "https://picsum.photos/id/1019/800/550",
        "description": (
            "Seema Malaka is a stunning Buddhist meditation centre and temple that floats on the "
            "serene Beira Lake in central Colombo. Designed by the renowned architect Geoffrey Bawa, "
            "the structure of open pavilions connected by wooden walkways blends modernist design "
            "with traditional religious architecture. At night the temple reflects beautifully on "
            "the still lake, creating one of the most photographed scenes in the capital."
        ),
        "comments": [("demo@slexplore.com", "Geoffrey Bawa's design is extraordinary. Magical at night when everything is lit up.")],
    },
    {
        "name": "Negombo Beach & Fish Market",
        "province": "Western Province", "district": "Gampaha",
        "latitude": 7.2092, "longitude": 79.8359,
        "img": "https://picsum.photos/id/1039/800/550",
        "description": (
            "Negombo is a bustling coastal city just 35 km north of Colombo and the first stop for "
            "most travellers arriving at Bandaranaike International Airport. Its long sandy beach, "
            "colourful fishing fleet, and vibrant fish market — one of the largest in Sri Lanka — "
            "make it a lively and atmospheric destination. The city's Dutch canal system, "
            "colonial churches, and excellent seafood restaurants add to its considerable charm."
        ),
        "comments": [("amara@slexplore.com", "The morning fish market is absolutely worth the early wake-up. Freshest seafood anywhere!")],
    },
    {
        "name": "Muthurajawela Wetlands",
        "province": "Western Province", "district": "Gampaha",
        "latitude": 7.1500, "longitude": 79.8800,
        "img": "https://picsum.photos/id/397/800/550",
        "description": (
            "Muthurajawela is Sri Lanka's largest coastal peat bog and a vital wetland ecosystem "
            "on the western coast near Negombo. The 3,068-hectare reserve supports over 190 species "
            "of birds, dozens of reptiles including crocodiles, and rich mangrove forests. "
            "Boat tours through the canals offer a tranquil way to spot wildlife and experience "
            "the natural beauty of this often-overlooked ecological treasure."
        ),
        "comments": [("demo@slexplore.com", "Took the boat tour at dawn. Saw crocodiles, kingfishers, and herons. Highly recommend.")],
    },
    {
        "name": "Kalutara Bodhiya",
        "province": "Western Province", "district": "Kalutara",
        "latitude": 6.5854, "longitude": 79.9625,
        "img": "https://picsum.photos/id/48/800/550",
        "description": (
            "The Kalutara Bodhiya is a magnificent hollow stupa on the banks of the Kalu Ganga river, "
            "unique in Sri Lanka for being the only dagoba with a Bodhi tree inside it. "
            "The gleaming white dome and its serene riverside setting make it one of the most "
            "photographed religious structures along the southern coastal highway. "
            "Pilgrims stop here year-round and the site is especially vibrant during Vesak celebrations."
        ),
        "comments": [("amara@slexplore.com", "The hollow stupa concept is unique. Beautiful at dusk with the river behind it.")],
    },
    {
        "name": "Bentota Beach",
        "province": "Western Province", "district": "Kalutara",
        "latitude": 6.4264, "longitude": 79.9967,
        "img": "https://picsum.photos/id/106/800/550",
        "description": (
            "Bentota is Sri Lanka's premier beach resort destination on the south-west coast, "
            "where the Bentota River meets the Indian Ocean forming a stunning coastal lagoon. "
            "The beach is long, golden, and fringed with swaying palms, offering calm waters "
            "ideal for swimming, water sports, and surfing. The lagoon is perfect for boat rides, "
            "water-skiing, and windsurfing. Luxury resorts, Ayurveda spas, and the Geoffrey Bawa–designed "
            "Brief Garden are nearby highlights."
        ),
        "comments": [("demo@slexplore.com", "The lagoon side is perfect for watersports. One of the best beach setups in the whole country.")],
    },
    # ── CENTRAL PROVINCE ─────────────────────────────────────────────────────
    {
        "name": "Peradeniya Royal Botanical Gardens",
        "province": "Central Province", "district": "Kandy",
        "latitude": 7.2686, "longitude": 80.5966,
        "img": "https://picsum.photos/id/145/800/550",
        "description": (
            "Covering 147 acres on a bend of the Mahaweli River just outside Kandy, Peradeniya is "
            "the finest botanical garden in Sri Lanka and one of the best in all of Asia. "
            "The gardens contain over 4,000 species of plants including a 160-year-old Java fig tree "
            "with an extraordinary canopy spread, a spectacular avenue of royal palms, "
            "a vast orchid house, and ancient specimens of spice trees. Beloved by families, "
            "students, and nature lovers alike."
        ),
        "comments": [
            ("amara@slexplore.com", "The giant Java fig tree alone is worth the trip. Absolutely magnificent specimen."),
            ("demo@slexplore.com", "Beautifully maintained. The orchid collection is one of the finest I've seen."),
        ],
    },
    {
        "name": "Udawatta Kele Forest Sanctuary",
        "province": "Central Province", "district": "Kandy",
        "latitude": 7.2980, "longitude": 80.6380,
        "img": "https://picsum.photos/id/192/800/550",
        "description": (
            "Udawatta Kele is a 104-hectare royal forest reserve that sits directly above the Temple "
            "of the Tooth Relic in Kandy. Once the private forest of Kandyan kings, this ancient "
            "reserve is an urban oasis of dense forest, tranquil ponds, and gentle walking trails. "
            "It harbours over 68 species of birds, monkeys, giant squirrels, and rare orchids. "
            "The forest offers a peaceful escape from the busy city below."
        ),
        "comments": [("amara@slexplore.com", "Peaceful and green right in the heart of Kandy. Saw purple-faced langurs on the trail.")],
    },
    {
        "name": "Lankathilake Temple",
        "province": "Central Province", "district": "Kandy",
        "latitude": 7.2414, "longitude": 80.5672,
        "img": "https://picsum.photos/id/244/800/550",
        "description": (
            "Lankathilake is a magnificent medieval Buddhist and Hindu temple built by King Bhuvanekabahu IV "
            "in the 14th century on a dramatic rocky outcrop. The four-storey brick shrine room, built "
            "in the Dravidian style, towers 30 metres above the surrounding rice paddies and lakes. "
            "The approach through the village and over a wooden causeway, combined with the views from "
            "the summit, makes this one of the most atmospheric temple visits near Kandy."
        ),
        "comments": [("demo@slexplore.com", "The dramatic rock setting is incredible. Views over the paddy fields are stunning.")],
    },
    {
        "name": "Aluvihare Rock Temple",
        "province": "Central Province", "district": "Matale",
        "latitude": 7.4667, "longitude": 80.6167,
        "img": "https://picsum.photos/id/247/800/550",
        "description": (
            "Aluvihare Rock Temple is a historically significant cave temple near Matale where, "
            "according to tradition, the Pali Canon — the complete teachings of the Buddha — was first "
            "committed to writing on ola-leaf manuscripts in the 1st century BC. "
            "The complex of natural caves contains beautiful ancient murals, reclining Buddhas, "
            "and a library of palm-leaf manuscripts. A small museum displays original ola-leaf writings."
        ),
        "comments": [("amara@slexplore.com", "Fascinating historical significance. The cave murals depicting the writing of the Pali Canon are remarkable.")],
    },
    {
        "name": "Hakgala Botanical Gardens",
        "province": "Central Province", "district": "Nuwara Eliya",
        "latitude": 6.8703, "longitude": 80.8244,
        "img": "https://picsum.photos/id/146/800/550",
        "description": (
            "Situated at 1,745 metres above sea level on the slopes of Hakgala Rock, these botanical "
            "gardens were established in 1861 as an experimental station for cinchona cultivation. "
            "Today the 27-acre garden is famous for its spectacular rose collection, a large "
            "fernery, magnolias, and an extraordinary temperate garden zone. According to legend, "
            "Hakgala Rock is the site where Hanuman found the magical medicinal herb sanjivani "
            "in the Ramayana epic."
        ),
        "comments": [("demo@slexplore.com", "The rose garden is breathtaking in bloom. The cool mountain air and misty atmosphere are wonderful.")],
    },
    {
        "name": "Gregory Lake, Nuwara Eliya",
        "province": "Central Province", "district": "Nuwara Eliya",
        "latitude": 6.9698, "longitude": 80.7706,
        "img": "https://picsum.photos/id/338/800/550",
        "description": (
            "Gregory Lake is a picturesque man-made reservoir at the heart of Nuwara Eliya, "
            "the cool highland city often called 'Little England'. Created in 1873 by Governor "
            "Sir William Gregory, the lake is surrounded by manicured lawns, colonial-era bungalows, "
            "and the lush Piduruthalagala mountain. Paddle boating, horse riding, and leisurely "
            "lakeside strolls are popular activities. The Victoria Park and the famous Hill Club "
            "are nearby attractions."
        ),
        "comments": [
            ("amara@slexplore.com", "The strawberry season in Nuwara Eliya with this backdrop is incredible. Very English atmosphere!"),
            ("demo@slexplore.com", "The April season horse races at the nearby track make this area extra lively."),
        ],
    },
    # ── SOUTHERN PROVINCE ────────────────────────────────────────────────────
    {
        "name": "Hikkaduwa Coral Reef",
        "province": "Southern Province", "district": "Galle",
        "latitude": 6.1395, "longitude": 80.1042,
        "img": "https://picsum.photos/id/97/800/550",
        "description": (
            "Hikkaduwa National Park protects a shallow coral sanctuary just metres from the beach, "
            "making it one of the most accessible snorkelling destinations in Sri Lanka. "
            "Glass-bottom boats glide over the reef where green sea turtles feed alongside "
            "parrotfish, pufferfish, and a dazzling array of reef life. The town also offers "
            "world-class surfing, lively beach bars, and a famous Coral Museum. "
            "Best visited outside the monsoon season between November and April."
        ),
        "comments": [("amara@slexplore.com", "The turtles are incredibly tame! Snorkelled right alongside three of them near the beach.")],
    },
    {
        "name": "Unawatuna Beach",
        "province": "Southern Province", "district": "Galle",
        "latitude": 6.0095, "longitude": 80.2490,
        "img": "https://picsum.photos/id/290/800/550",
        "description": (
            "Just 5 km south of Galle Fort, Unawatuna is a crescent-shaped bay of warm turquoise "
            "water backed by a fringe of coconut palms and a lively strip of restaurants and guesthouses. "
            "The sheltered bay is safe for swimming and snorkelling, with a coral reef at its southern "
            "end. The Jungle Beach cove and the hilltop Japanese Peace Pagoda nearby offer quieter "
            "alternatives for those seeking more solitude."
        ),
        "comments": [("demo@slexplore.com", "The best combination of beach and food in the south. Brilliant for a few relaxing days.")],
    },
    {
        "name": "Weligama Bay",
        "province": "Southern Province", "district": "Matara",
        "latitude": 5.9742, "longitude": 80.4298,
        "img": "https://picsum.photos/id/430/800/550",
        "description": (
            "Weligama — meaning 'sandy village' in Sinhala — is a large, sweeping bay on the south "
            "coast renowned as one of Sri Lanka's best beginner surfing spots. The long, gently curving "
            "beach is safe for swimming and the town retains an authentic fishing village character "
            "with colourful outrigger boats lining the shore each morning. The famous stilt fishermen "
            "of Weligama, balancing on cross-poles driven into the sea bed, are one of the most "
            "iconic sights in Sri Lanka."
        ),
        "comments": [
            ("amara@slexplore.com", "Great beginner surf lessons here. The stilt fishermen at sunrise are an extraordinary sight."),
            ("demo@slexplore.com", "Genuine fishing village feel. The kottu roti and fresh fish curry are outstanding."),
        ],
    },
    {
        "name": "Dondra Lighthouse",
        "province": "Southern Province", "district": "Matara",
        "latitude": 5.9219, "longitude": 80.5892,
        "img": "https://picsum.photos/id/365/800/550",
        "description": (
            "Standing at the southernmost tip of Sri Lanka, the Dondra Head Lighthouse is the tallest "
            "lighthouse in South Asia at 49 metres. Built by the British in 1890, the white tower "
            "offers panoramic views over the meeting point of the Indian Ocean, where the waters "
            "change colour dramatically. The nearby Dondra Vishnu Temple is one of the holiest "
            "Hindu shrines in Sri Lanka, adding cultural significance to the scenic location."
        ),
        "comments": [("amara@slexplore.com", "Stood at the southernmost tip of Sri Lanka! The lighthouse keeper was kind enough to let us climb to the top.")],
    },
    {
        "name": "Bundala National Park",
        "province": "Southern Province", "district": "Hambantota",
        "latitude": 6.1932, "longitude": 81.2114,
        "img": "https://picsum.photos/id/582/800/550",
        "description": (
            "Bundala National Park is a UNESCO Ramsar Wetland of International Importance on Sri Lanka's "
            "southern coast. The park is a critical wintering ground for migratory birds from across "
            "Eurasia, with over 200 bird species recorded. Flamingos are the star attraction, often "
            "seen wading in the coastal lagoons in spectacular pink flocks. Elephants, crocodiles, "
            "and sea turtles also frequent the park's coastal habitat."
        ),
        "comments": [("demo@slexplore.com", "The flamingo flocks at the lagoon are breathtaking. Far fewer crowds than Yala but equally rewarding.")],
    },
    # ── NORTH WESTERN PROVINCE ───────────────────────────────────────────────
    {
        "name": "Wilpattu National Park",
        "province": "North Western Province", "district": "Puttalam",
        "latitude": 8.4500, "longitude": 80.0167,
        "img": "https://picsum.photos/id/593/800/550",
        "description": (
            "Sri Lanka's largest national park at 1,317 km², Wilpattu is characterised by its "
            "unique villus — natural lakes and basins that attract wildlife. Once the preferred hunting "
            "ground of colonial governors, the park is today one of the best places to spot "
            "Sri Lankan leopards in a remarkably wild and undisturbed setting. "
            "Sloth bears, elephants, spotted deer, and a rich birdlife also abound. "
            "The park's remoteness means fewer visitors and a more authentic safari experience."
        ),
        "comments": [
            ("amara@slexplore.com", "More wilderness feel than Yala. Spotted a leopard and her cub resting by a villu at midday."),
            ("demo@slexplore.com", "The sloth bear sighting was totally unexpected. Empty roads and pristine nature — incredible."),
        ],
    },
    {
        "name": "Kalpitiya Beach & Dolphins",
        "province": "North Western Province", "district": "Puttalam",
        "latitude": 8.2333, "longitude": 79.7667,
        "img": "https://picsum.photos/id/119/800/550",
        "description": (
            "The Kalpitiya peninsula is a narrow strip of land flanked by the Bar Reef Marine Sanctuary "
            "on the west and a series of coastal lagoons to the east. The area is world-renowned for "
            "spinner dolphin pods that can number in the thousands, offering some of the most "
            "spectacular dolphin encounters anywhere on earth. The Bar Reef is excellent for diving, "
            "with whale sharks occasionally spotted. Between May and October, kitesurfers flock here "
            "for consistently powerful winds."
        ),
        "comments": [("amara@slexplore.com", "The dolphin pods here are absolutely enormous. Hundreds of spinner dolphins leaping around the boat!")],
    },
    {
        "name": "Yapahuwa Rock Fortress",
        "province": "North Western Province", "district": "Kurunegala",
        "latitude": 7.8328, "longitude": 80.3247,
        "img": "https://picsum.photos/id/1045/800/550",
        "description": (
            "Yapahuwa was the capital of Sri Lanka for a brief but significant period in the 13th "
            "century when it served as the refuge of the Sacred Tooth Relic. The fortress is built "
            "around a 90-metre granite rock rising dramatically from the flat plain of the North-Western "
            "Province. The ornate decorative staircase at the entrance — richly carved with makaras, "
            "lions, and maidens — is considered a masterpiece of medieval Sri Lankan sculpture."
        ),
        "comments": [("demo@slexplore.com", "The carved staircase is a masterpiece. Far fewer tourists than Sigiriya but equally impressive architecture.")],
    },
    {
        "name": "Ridi Viharaya (Silver Temple)",
        "province": "North Western Province", "district": "Kurunegala",
        "latitude": 7.4833, "longitude": 80.3833,
        "img": "https://picsum.photos/id/1048/800/550",
        "description": (
            "Ridi Viharaya, the 'Silver Temple', is one of the most revered cave temples in Sri Lanka, "
            "said to have been founded in the 2nd century BC when silver ore was discovered on the site "
            "and used to fund the construction of the great stupa at Anuradhapura. "
            "The main cave houses a magnificent 9-metre reclining Buddha and a fascinating collection "
            "of Dutch-era ivory panels. The temple's riverside setting and ancient atmosphere make "
            "it an off-the-beaten-path gem."
        ),
        "comments": [("amara@slexplore.com", "A hidden gem. The Dutch ivory panels in the cave are extraordinary and completely unexpected.")],
    },
    # ── NORTH CENTRAL PROVINCE ────────────────────────────────────────────────
    {
        "name": "Mihintale",
        "province": "North Central Province", "district": "Anuradhapura",
        "latitude": 8.3497, "longitude": 80.5091,
        "img": "https://picsum.photos/id/1036/800/550",
        "description": (
            "Mihintale is considered the cradle of Buddhism in Sri Lanka, the sacred hilltop where "
            "the monk Mahinda — son of the Indian emperor Ashoka — introduced Buddhism to King "
            "Devanampiya Tissa in 247 BC. The site comprises a series of rocky hills linked by "
            "1,840 granite steps leading to ancient stupas, caves, and shrines, including the "
            "remarkable Ambasthalaya Dagoba marking the exact spot of conversion. "
            "The panoramic views across the ancient kingdom are spectacular."
        ),
        "comments": [
            ("demo@slexplore.com", "The climb up 1,840 steps is worth every breath. The view from the top at sunset is extraordinary."),
            ("amara@slexplore.com", "The most spiritually significant site in Sri Lankan Buddhism. Deeply moving atmosphere."),
        ],
    },
    {
        "name": "Aukana Buddha Statue",
        "province": "North Central Province", "district": "Anuradhapura",
        "latitude": 8.0333, "longitude": 80.5833,
        "img": "https://picsum.photos/id/257/800/550",
        "description": (
            "The Aukana Buddha is a magnificent 12-metre standing statue carved from a single granite "
            "outcrop during the reign of King Dhatusena in the 5th century AD. One of the finest "
            "examples of ancient Sri Lankan rock sculpture, the statue stands in the Abhaya mudra "
            "posture with extraordinary serenity and artistic refinement. "
            "According to tradition, the statue can only be fully appreciated in the early morning "
            "when rainwater running from the head drips from the nose but not the shoulders."
        ),
        "comments": [("amara@slexplore.com", "The scale and artistic quality is humbling. Arriving at dawn in the mist makes it truly magical.")],
    },
    {
        "name": "Medirigiriya Vatadage",
        "province": "North Central Province", "district": "Polonnaruwa",
        "latitude": 7.9833, "longitude": 81.0333,
        "img": "https://picsum.photos/id/1003/800/550",
        "description": (
            "Medirigiriya contains one of the best-preserved vatadages — circular relic houses — "
            "in Sri Lanka, dating back to the 7th century and later restored by King Aggabodhi IV. "
            "Four perfectly preserved seated Buddha statues face the cardinal directions, surrounded "
            "by three concentric rings of stone pillars that once supported a wooden roof. "
            "The site lies off the main tourist trail, preserving a wonderful sense of peaceful "
            "antiquity far from the crowds of Polonnaruwa."
        ),
        "comments": [("demo@slexplore.com", "One of the most beautiful and peaceful ancient sites in the whole country. Completely crowd-free.")],
    },
    # ── NORTHERN PROVINCE ─────────────────────────────────────────────────────
    {
        "name": "Nainativu Island",
        "province": "Northern Province", "district": "Jaffna",
        "latitude": 9.6667, "longitude": 79.9167,
        "img": "https://picsum.photos/id/1043/800/550",
        "description": (
            "Nainativu is a small sacred island in the Jaffna lagoon accessible only by boat from "
            "Kurikadduwan. It is home to two of the most sacred shrines in northern Sri Lanka: "
            "the Nainativu Nagapooshani Amman Kovil, one of the most revered Hindu temples in "
            "the country, and the Nainativu Buddhist temple associated with one of the Buddha's "
            "legendary visits to Sri Lanka. Pilgrims of both faiths share the island in remarkable harmony."
        ),
        "comments": [("amara@slexplore.com", "The boat journey through the lagoon and the sight of pilgrims from both faiths is deeply moving.")],
    },
    {
        "name": "Keerimalai Hot Springs",
        "province": "Northern Province", "district": "Jaffna",
        "latitude": 9.8167, "longitude": 80.0333,
        "img": "https://picsum.photos/id/142/800/550",
        "description": (
            "Keerimalai is a sacred coastal site at the northern tip of the Jaffna peninsula, "
            "home to natural freshwater springs that bubble up directly beside the sea. "
            "The springs, said to have healing properties, are fed by natural limestone aquifers "
            "and have been used for sacred bathing for centuries. The adjacent Maviddapuram Kandaswamy "
            "Temple is one of the most important Hindu shrines in Sri Lanka, drawing pilgrims year-round."
        ),
        "comments": [("demo@slexplore.com", "Surreal to swim in fresh spring water with the sea crashing just metres away. Steeped in legend.")],
    },
    {
        "name": "Mannar Fort",
        "province": "Northern Province", "district": "Mannar",
        "latitude": 8.9797, "longitude": 79.9039,
        "img": "https://picsum.photos/id/1050/800/550",
        "description": (
            "Mannar Fort is a large Portuguese-built fortification on Mannar Island, constructed in "
            "1560 and later renovated by the Dutch and the British. The massive coral-stone ramparts "
            "overlook the shallow straits separating Sri Lanka from India. The nearby Baobab tree — "
            "said to be over 700 years old and the largest in Asia — is a magnificent living monument "
            "to the island's ancient Arab trading connections. Mannar is also famous for its wading "
            "birds and the seasonal flamingo gatherings on the salt flats."
        ),
        "comments": [("amara@slexplore.com", "The ancient baobab tree near the fort is absolutely extraordinary. Thought I was in Africa for a moment!")],
    },
    # ── EASTERN PROVINCE ─────────────────────────────────────────────────────
    {
        "name": "Koneswaram Temple, Trincomalee",
        "province": "Eastern Province", "district": "Trincomalee",
        "latitude": 8.5774, "longitude": 81.2348,
        "img": "https://picsum.photos/id/1071/800/550",
        "description": (
            "The Koneswaram Kovil is a classical Hindu temple dedicated to Lord Shiva, dramatically "
            "perched on Swami Rock — a sheer cliff that plunges 130 metres into Trincomalee harbour. "
            "The site was one of the most magnificent temples in ancient Asia before it was demolished "
            "by Portuguese colonists in 1624. Rebuilt and consecrated in the 20th century, the temple "
            "today draws thousands of pilgrims and the views from the cliff edge over the natural "
            "harbour are simply spectacular."
        ),
        "comments": [("demo@slexplore.com", "The cliff-top setting is dramatic. The view over Trincomalee harbour from Lovers' Leap is unforgettable.")],
    },
    {
        "name": "Marble Beach, Trincomalee",
        "province": "Eastern Province", "district": "Trincomalee",
        "latitude": 8.6167, "longitude": 81.2333,
        "img": "https://picsum.photos/id/200/800/550",
        "description": (
            "Marble Beach is a secluded, pristine stretch of white sand within the former Sri Lanka "
            "Air Force base near Trincomalee, now open to the public. The beach's clear, calm turquoise "
            "waters and lack of commercialisation make it one of the cleanest and most beautiful beaches "
            "on the east coast. Nestled between rocky headlands and fringed with casuarina trees, "
            "it offers a sense of seclusion and natural beauty increasingly rare in Sri Lanka."
        ),
        "comments": [("amara@slexplore.com", "The clearest water I saw in all of Sri Lanka. Completely unspoilt and uncrowded even in season.")],
    },
    {
        "name": "Batticaloa Fort",
        "province": "Eastern Province", "district": "Batticaloa",
        "latitude": 7.7167, "longitude": 81.7000,
        "img": "https://picsum.photos/id/1074/800/550",
        "description": (
            "Batticaloa Fort is a well-preserved Dutch colonial fort built in 1665 on a small island "
            "in the Batticaloa Lagoon, connected to the mainland by a causeway. The fort's thick coral "
            "walls enclose a cluster of colonial-era buildings now used as government offices. "
            "Batticaloa Lagoon itself is famous for its 'singing fish' — a mysterious musical sound "
            "said to emanate from the lagoon floor on certain nights near Kallady Bridge, attributed "
            "to shellfish vibrating in the current."
        ),
        "comments": [("demo@slexplore.com", "The lagoon and the fort together make for a lovely afternoon. Went at dusk hoping to hear the singing fish!")],
    },
    {
        "name": "Arugam Bay",
        "province": "Eastern Province", "district": "Ampara",
        "latitude": 6.8433, "longitude": 81.8342,
        "img": "https://picsum.photos/id/433/800/550",
        "description": (
            "Arugam Bay is Sri Lanka's most famous surf destination and one of the top surf breaks "
            "in the world, consistently ranked among the best point breaks in Asia. The crescent "
            "bay on the southeast coast draws international surfers between May and October when the "
            "swells from the Indian Ocean produce long, perfect right-handers. Beyond surfing, "
            "the laid-back fishing village atmosphere, nearby Kumana National Park, and the "
            "spectacularly beautiful lagoon attract a diverse crowd of travellers."
        ),
        "comments": [
            ("amara@slexplore.com", "World-class surf and a beautifully mellow atmosphere. The main break at 'The Point' is phenomenal."),
            ("demo@slexplore.com", "Went for the surf, stayed for the vibe. The lagoon safari to spot leopards is fantastic."),
        ],
    },
    {
        "name": "Lahugala National Park",
        "province": "Eastern Province", "district": "Ampara",
        "latitude": 6.8500, "longitude": 81.7000,
        "img": "https://picsum.photos/id/76/800/550",
        "description": (
            "Lahugala Kitulana National Park is a small but remarkable sanctuary centred on three "
            "ancient tanks — Lahugala, Kitulana, and Henanigala — that attract the largest "
            "concentration of wild elephants in Sri Lanka. During the dry months of August and "
            "September, up to 150 elephants can gather at the tanks simultaneously, creating one "
            "of the most extraordinary wildlife spectacles in all of Asia. The park is tiny and "
            "compact, making it possible to cover in a short afternoon visit."
        ),
        "comments": [("amara@slexplore.com", "Over 100 elephants at the tank at once. Truly one of the great wildlife spectacles on earth.")],
    },
    # ── UVA PROVINCE ─────────────────────────────────────────────────────────
    {
        "name": "Dunhinda Falls",
        "province": "Uva Province", "district": "Badulla",
        "latitude": 7.0000, "longitude": 81.0167,
        "img": "https://picsum.photos/id/167/800/550",
        "description": (
            "Dunhinda Falls is the most spectacular waterfall in Sri Lanka, plunging 64 metres into "
            "a misty rocky gorge in the hills above Badulla. The name 'Dunhinda' means 'smoky water' "
            "in Sinhala, a reference to the permanent cloud of mist created by the thundering cascade. "
            "The 1.5 km jungle walk to the falls through dense forest, crossing a suspension bridge "
            "over the river gorge, is an experience in itself. Swimming is not permitted but the "
            "viewing platform offers dramatic close-up views."
        ),
        "comments": [
            ("demo@slexplore.com", "The jungle walk builds the anticipation perfectly. The roar you hear long before you see it is thrilling."),
            ("amara@slexplore.com", "The mist from the falls soaks you completely. Absolutely magnificent — bring a rain jacket!"),
        ],
    },
    {
        "name": "Bogoda Wooden Bridge",
        "province": "Uva Province", "district": "Badulla",
        "latitude": 6.9833, "longitude": 81.1833,
        "img": "https://picsum.photos/id/534/800/550",
        "description": (
            "The Bogoda Bridge near Hali-Ela is believed to be the oldest surviving wooden bridge in "
            "Sri Lanka, dating back approximately 500 years to the Kandyan Kingdom era. The ancient "
            "structure spans the Gallanda Oya river and remains in daily use by locals. "
            "The adjacent Bogoda Viharaya is a small rock-cave temple with well-preserved painted "
            "wooden ceilings depicting traditional floral and animal motifs. The serene forest "
            "setting and the sound of the river below make this a wonderfully tranquil stop."
        ),
        "comments": [("amara@slexplore.com", "Completely off the tourist trail. The 500-year-old bridge is still in daily use — remarkable!")],
    },
    {
        "name": "Maligawila Buddha Statue",
        "province": "Uva Province", "district": "Monaragala",
        "latitude": 6.7500, "longitude": 81.1333,
        "img": "https://picsum.photos/id/338/800/550",
        "description": (
            "The Maligawila Buddha statue is a colossal 10.6-metre standing figure carved from a "
            "single limestone rock during the 7th century AD, making it one of the largest ancient "
            "freestanding Buddha statues in the world. The statue was found fallen and broken into "
            "three pieces in the jungle and was painstakingly restored in 1991. The site also "
            "includes a 10-metre Bodhisattva statue of equal antiquity. Both statues stand in "
            "a peaceful forested clearing that feels worlds away from modern life."
        ),
        "comments": [("demo@slexplore.com", "Stumbling upon this monumental statue in a jungle clearing feels like a genuine discovery. Extraordinary.")],
    },
    {
        "name": "Buduruwagala Rock Temple",
        "province": "Uva Province", "district": "Monaragala",
        "latitude": 6.3167, "longitude": 81.0833,
        "img": "https://picsum.photos/id/1025/800/550",
        "description": (
            "Buduruwagala is a remote cave temple near Wellawaya containing seven magnificent rock "
            "relief sculptures carved from a sheer granite face during the Mahayana Buddhist period "
            "of the 8th or 9th century AD. The central standing Buddha figure stands 15 metres tall "
            "and still bears traces of its original stucco and orange paint. "
            "A unique feature is a flame-shaped halo and a Bodhisattva figure holding a thunderbolt "
            "— iconographic rarities in Sri Lankan art. The site is surrounded by jungle and "
            "visited by very few tourists."
        ),
        "comments": [
            ("amara@slexplore.com", "Remote, atmospheric, and extraordinary. The traces of original paint on the 1,200-year-old figures are visible."),
            ("demo@slexplore.com", "The 15-metre central Buddha still has an ethereal quality despite its age. A true hidden treasure."),
        ],
    },
    # ── SABARAGAMUWA PROVINCE ─────────────────────────────────────────────────
    {
        "name": "Sinharaja Forest Reserve",
        "province": "Sabaragamuwa Province", "district": "Ratnapura",
        "latitude": 6.4012, "longitude": 80.4881,
        "img": "https://picsum.photos/id/56/800/550",
        "description": (
            "Sinharaja is Sri Lanka's last viable area of primary tropical rainforest and a UNESCO "
            "World Heritage Site of outstanding biological diversity. The 88-km² reserve is home to "
            "64% of the country's endemic tree species and a remarkable concentration of endemic birds, "
            "including the rare Sri Lanka blue magpie. The forest is characterised by towering trees, "
            "a dense understorey, and the constant chorus of birds, frogs, and insects. "
            "Guided treks reveal extraordinary biodiversity at every step."
        ),
        "comments": [
            ("demo@slexplore.com", "The endemic bird flock was phenomenal — 12 species travelling together through the forest. Hire a local guide."),
            ("amara@slexplore.com", "The biodiversity is staggering. Saw purple-faced langurs, giant squirrels, and dozens of endemic birds in one morning."),
        ],
    },
    {
        "name": "Pinnawala Elephant Orphanage",
        "province": "Sabaragamuwa Province", "district": "Kegalle",
        "latitude": 7.2989, "longitude": 80.3522,
        "img": "https://picsum.photos/id/1084/800/550",
        "description": (
            "Pinnawala Elephant Orphanage was established in 1975 and is the world's first and largest "
            "sanctuary for orphaned and injured wild elephants. The herd of over 90 elephants follows "
            "a daily routine — grazing in the grounds, then walking in a spectacular procession down "
            "to the Ma Oya river for their daily bath. Watching these magnificent animals splash in "
            "the river while calves play around them is one of the most joyful wildlife experiences "
            "Sri Lanka has to offer."
        ),
        "comments": [
            ("amara@slexplore.com", "The river bathing procession is truly joyful. The baby elephants are irresistibly charming."),
            ("demo@slexplore.com", "Magical to see so many elephants up close in a relatively natural setting. Go early for the bath time."),
        ],
    },
    {
        "name": "Kitulgala Rainforest & Rafting",
        "province": "Sabaragamuwa Province", "district": "Kegalle",
        "latitude": 6.9897, "longitude": 80.4183,
        "img": "https://picsum.photos/id/358/800/550",
        "description": (
            "Kitulgala is a small riverside town nestled in a lush valley of the Kelani River, "
            "famous as the filming location for David Lean's 1957 classic 'The Bridge on the River Kwai'. "
            "Today it draws adventure seekers for white-water rafting on the Class 3–4 rapids of the "
            "Kelani River, as well as canyoning, abseiling, and jungle trekking. The surrounding "
            "montane rainforest is rich in endemic birdlife and offers some of the best bird watching "
            "in Sri Lanka."
        ),
        "comments": [("amara@slexplore.com", "The white water rafting is a brilliant rush! The rainforest valley setting makes it even more spectacular.")],
    },
    {
        "name": "Ratnapura Gem Museum",
        "province": "Sabaragamuwa Province", "district": "Ratnapura",
        "latitude": 6.6833, "longitude": 80.4000,
        "img": "https://picsum.photos/id/175/800/550",
        "description": (
            "Ratnapura, meaning 'City of Gems', is the gem mining capital of Sri Lanka and the world's "
            "most prolific source of blue sapphires, rubies, cat's eyes, and alexandrite. "
            "The Gem Museum and mine tours offer a fascinating insight into the traditional pit-mining "
            "techniques unchanged for centuries. Visitors can watch miners sift gravel in shallow "
            "pools and purchase certified gemstones directly from licensed traders. "
            "The surrounding paddy fields are dotted with small mining pits."
        ),
        "comments": [("demo@slexplore.com", "Watching the mining process and the excitement when a gem is found is captivating. Bought a beautiful blue sapphire!")],
    },
    # ── ADDITIONAL VARIETY ────────────────────────────────────────────────────
    {
        "name": "Knuckles Mountain Range",
        "province": "Central Province", "district": "Kandy",
        "latitude": 7.4167, "longitude": 80.7833,
        "img": "https://picsum.photos/id/217/800/550",
        "description": (
            "The Knuckles Mountain Range — named for its knuckle-like appearance from the plains below — "
            "is a UNESCO World Heritage Site covering 155 km² of rugged peaks, deep valleys, and "
            "cloud forests in the central highlands. The range contains an extraordinary concentration "
            "of endemic flora and fauna including 34 endemic bird species and rare mammals. "
            "Trekking routes through remote villages, waterfalls, and misty forest offer some of "
            "Sri Lanka's most rewarding multi-day hiking adventures."
        ),
        "comments": [
            ("amara@slexplore.com", "Three-day trek through the range was the highlight of my trip. Remote villages, waterfalls, and cloud forest."),
            ("demo@slexplore.com", "The biodiversity is extraordinary. Saw purple-faced langurs, giant squirrels, and endemic birds on every trail."),
        ],
    },
    {
        "name": "Nalanda Gedige",
        "province": "Central Province", "district": "Matale",
        "latitude": 7.5833, "longitude": 80.7000,
        "img": "https://picsum.photos/id/1068/800/550",
        "description": (
            "Nalanda Gedige is a unique Hindu-Buddhist shrine dating from approximately the 8th century "
            "and one of the finest examples of syncretic religious architecture in Sri Lanka. "
            "Built in a style reminiscent of South Indian temples, the stone shrine room sits in "
            "the middle of a man-made lake, accessible via a causeway. Carvings on the outer walls "
            "combine Buddhist and Tantric Hindu iconography — a remarkable testament to the religious "
            "tolerance of medieval Sri Lanka."
        ),
        "comments": [("amara@slexplore.com", "The island setting in the lake is beautiful. The blend of Hindu and Buddhist iconography is fascinating.")],
    },
    {
        "name": "Mulgirigala Rock Temple",
        "province": "Southern Province", "district": "Hambantota",
        "latitude": 6.0383, "longitude": 80.6833,
        "img": "https://picsum.photos/id/403/800/550",
        "description": (
            "Mulgirigala is a magnificent rock temple complex built over five levels of a 214-metre "
            "granite inselberg rising from the southern plains. Ancient cave temples at each level "
            "contain large reclining Buddhas and well-preserved murals depicting the life of the "
            "Buddha, dating from the 18th century. At the summit, a small white stupa offers "
            "panoramic 360-degree views over the coconut palms and paddy fields of the Hambantota "
            "district. The site is often called the 'Little Sigiriya of the south'."
        ),
        "comments": [("demo@slexplore.com", "Climbing through five levels of cave temples is an incredible experience. The summit views are stunning.")],
    },
    {
        "name": "Tangalle Beach",
        "province": "Southern Province", "district": "Hambantota",
        "latitude": 6.0239, "longitude": 80.7952,
        "img": "https://picsum.photos/id/626/800/550",
        "description": (
            "Tangalle is a charming fishing town on the south coast with a beautiful natural harbour "
            "and a series of secluded beaches stretching along the coast. Rekawa Beach, a short "
            "distance east, is one of the most important sea turtle nesting sites in Sri Lanka, "
            "where five species of sea turtle come ashore to nest between May and September. "
            "Lagoon trips, snorkelling, and the slow, unhurried pace of Tangalle town make this "
            "one of the south coast's most appealing destinations."
        ),
        "comments": [
            ("amara@slexplore.com", "Watched five loggerhead turtles nest on Rekawa Beach at night. An utterly unforgettable experience."),
        ],
    },
    {
        "name": "Mannar Baobab Tree",
        "province": "Northern Province", "district": "Mannar",
        "latitude": 8.9797, "longitude": 79.9128,
        "img": "https://picsum.photos/id/442/800/550",
        "description": (
            "The Ancient Baobab Tree of Mannar is believed to be over 700 years old and is the largest "
            "and oldest baobab in Asia, with a trunk circumference exceeding 19 metres. "
            "It was likely brought to Sri Lanka as a seed by Arab traders in the 13th or 14th century "
            "as part of the thriving maritime trade route between Arabia and the Far East. "
            "The tree stands near the Mannar Fort and is a beloved local landmark, its immense "
            "and otherworldly form recognisable from a great distance."
        ),
        "comments": [("amara@slexplore.com", "Standing next to this 700-year-old tree is humbling. It belongs in Africa but here it is in Sri Lanka!")],
    },
    {
        "name": "Mullaitivu Beach",
        "province": "Northern Province", "district": "Mullaitivu",
        "latitude": 9.2667, "longitude": 80.8167,
        "img": "https://picsum.photos/id/1049/800/550",
        "description": (
            "The Mullaitivu coast is one of the wildest and least-visited stretches of coastline in "
            "Sri Lanka, with long undeveloped beaches of white sand backed by casuarina forests. "
            "The Nanthikadal Lagoon near Mullaitivu is a hauntingly beautiful water body fringed "
            "with mangroves and rich in migratory birds. The area is seeing gradual development as "
            "tourism slowly returns to the far north, offering travellers a genuinely remote and "
            "unspoilt coastal experience with few facilities but extraordinary natural beauty."
        ),
        "comments": [("demo@slexplore.com", "One of the last truly undiscovered coastlines in Sri Lanka. Empty beaches and absolute tranquility.")],
    },
    {
        "name": "Vavuniya Town & Temple",
        "province": "Northern Province", "district": "Vavuniya",
        "latitude": 8.7514, "longitude": 80.4975,
        "img": "https://picsum.photos/id/1041/800/550",
        "description": (
            "Vavuniya is the gateway city to the far north of Sri Lanka and a fascinating crossroads "
            "of Tamil, Sinhalese, and Muslim cultures. The Kandaswamy Kovil is a significant Hindu "
            "temple dedicated to Lord Murugan, drawing pilgrims from across the north. "
            "The surrounding region contains numerous ancient tanks, Buddhist ruins, and wetlands "
            "that are increasingly accessible to visitors as northern Sri Lanka continues to "
            "open up to tourism after decades of isolation."
        ),
        "comments": [("amara@slexplore.com", "A great base to explore the north. The ancient tank landscapes around the town are beautiful.")],
    },
    {
        "name": "Nilaveli Beach",
        "province": "Eastern Province", "district": "Trincomalee",
        "latitude": 8.7167, "longitude": 81.2167,
        "img": "https://picsum.photos/id/100/800/550",
        "description": (
            "Nilaveli is widely considered one of the most beautiful beaches in Sri Lanka — a vast "
            "expanse of white sand and crystal-clear blue water stretching for kilometres north of "
            "Trincomalee. The beach is calm and sheltered between May and September, making it "
            "ideal for swimming and snorkelling. It provides the main access point for boat trips to "
            "the Pigeon Island Marine Sanctuary. Dolphins are commonly spotted offshore, and whale "
            "sightings are frequent in the bay during the season."
        ),
        "comments": [
            ("demo@slexplore.com", "The most beautiful beach in the entire country in my opinion. White sand, blue water, almost no crowds."),
            ("amara@slexplore.com", "Saw dolphins from the beach at sunset. The water here is impossibly clear and warm."),
        ],
    },
    {
        "name": "Ravana Falls, Ella",
        "province": "Uva Province", "district": "Badulla",
        "latitude": 6.8697, "longitude": 81.0589,
        "img": "https://picsum.photos/id/15/800/550",
        "description": (
            "Ravana Falls near Ella is one of the widest waterfalls in Sri Lanka, where the stream "
            "fans out dramatically across a broad rock face before plunging into a pool below. "
            "Named after the legendary demon king Ravana of the Ramayana epic — who is said to have "
            "hidden Sita in the cave behind the falls — the waterfall holds both natural beauty "
            "and mythological significance. During the wet season the volume of water is spectacular, "
            "and the pool at the base is popular for a refreshing swim."
        ),
        "comments": [
            ("amara@slexplore.com", "During the rains the whole rock face becomes a curtain of white water. Spectacular from the road below."),
        ],
    },
    {
        "name": "Ella Rock Hike",
        "province": "Uva Province", "district": "Badulla",
        "latitude": 6.8671, "longitude": 81.0465,
        "img": "https://picsum.photos/id/1080/800/550",
        "description": (
            "The hike to the summit of Ella Rock is one of the most rewarding short treks in Sri Lanka, "
            "rewarding walkers with breathtaking 360-degree views over the surrounding tea valleys, "
            "the Ella Gap, and as far as the southern plains on a clear day. "
            "The trail follows the railway line before ascending through tea estates and jungle, "
            "passing over the iconic Nine Arch Bridge. The hike typically takes 3–4 hours round trip "
            "and is best started early morning before the afternoon mist rolls in."
        ),
        "comments": [
            ("demo@slexplore.com", "Follow the railway tracks and then the trail up through tea estates. The view at the top is worth every step."),
            ("amara@slexplore.com", "Started at 6 AM and had the summit entirely to ourselves. The Ella Gap view is extraordinary."),
        ],
    },
]


def seed_more():
    db = SessionLocal()
    try:
        user1 = db.query(User).filter(User.email == "demo@slexplore.com").first()
        user2 = db.query(User).filter(User.email == "amara@slexplore.com").first()

        if not user1 or not user2:
            print("Users not found. Run seed.py first.")
            return

        user_map = {"demo@slexplore.com": user1, "amara@slexplore.com": user2}

        print(f"Adding {len(ATTRACTIONS)} attractions...\n")
        for idx, data in enumerate(ATTRACTIONS, 1):
            owner = user1 if idx % 2 == 1 else user2
            print(f"  [{idx:02d}/{len(ATTRACTIONS)}] {data['name']} → {owner.email}")

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

            ext = ".jpg"
            filename = f"{uuid.uuid4()}{ext}"
            dest = UPLOAD_DIR / filename
            if download_image(data["img"], dest):
                db.add(AttractionImage(attraction_id=attr.id, image_path=f"uploads/{filename}"))

            for commenter_email, content in data.get("comments", []):
                commenter = user_map.get(commenter_email, owner)
                db.add(Comment(attraction_id=attr.id, user_id=commenter.id, content=content))

        db.commit()
        print(f"\nDone! Added {len(ATTRACTIONS)} attractions.")

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_more()

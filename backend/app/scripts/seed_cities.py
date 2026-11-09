from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import City


CITIES = [
    ("Mumbai", "Maharashtra", 19.0760, 72.8777),
    ("Pune", "Maharashtra", 18.5204, 73.8567),
    ("Nagpur", "Maharashtra", 21.1458, 79.0882),
    ("Nashik", "Maharashtra", 19.9975, 73.7898),
    ("Thane", "Maharashtra", 19.2183, 72.9781),
    ("Chhatrapati Sambhajinagar", "Maharashtra", 19.8762, 75.3433),
    ("Solapur", "Maharashtra", 17.6599, 75.9064),
    ("Kolhapur", "Maharashtra", 16.7050, 74.2433),
    ("Delhi", "Delhi", 28.6139, 77.2090),
    ("New Delhi", "Delhi", 28.6139, 77.2090),
    ("Bengaluru", "Karnataka", 12.9716, 77.5946),
    ("Mysuru", "Karnataka", 12.2958, 76.6394),
    ("Mangaluru", "Karnataka", 12.9141, 74.8560),
    ("Hubballi", "Karnataka", 15.3647, 75.1240),
    ("Belagavi", "Karnataka", 15.8497, 74.4977),
    ("Chennai", "Tamil Nadu", 13.0827, 80.2707),
    ("Coimbatore", "Tamil Nadu", 11.0168, 76.9558),
    ("Madurai", "Tamil Nadu", 9.9252, 78.1198),
    ("Tiruchirappalli", "Tamil Nadu", 10.7905, 78.7047),
    ("Salem", "Tamil Nadu", 11.6643, 78.1460),
    ("Hyderabad", "Telangana", 17.3850, 78.4867),
    ("Warangal", "Telangana", 17.9689, 79.5941),
    ("Nizamabad", "Telangana", 18.6725, 78.0941),
    ("Karimnagar", "Telangana", 18.4386, 79.1288),
    ("Vijayawada", "Andhra Pradesh", 16.5062, 80.6480),
    ("Visakhapatnam", "Andhra Pradesh", 17.6868, 83.2185),
    ("Guntur", "Andhra Pradesh", 16.3067, 80.4365),
    ("Tirupati", "Andhra Pradesh", 13.6288, 79.4192),
    ("Rajahmundry", "Andhra Pradesh", 17.0005, 81.8040),
    ("Kochi", "Kerala", 9.9312, 76.2673),
    ("Thiruvananthapuram", "Kerala", 8.5241, 76.9366),
    ("Kozhikode", "Kerala", 11.2588, 75.7804),
    ("Thrissur", "Kerala", 10.5276, 76.2144),
    ("Kollam", "Kerala", 8.8932, 76.6141),
    ("Kolkata", "West Bengal", 22.5726, 88.3639),
    ("Howrah", "West Bengal", 22.5958, 88.2636),
    ("Siliguri", "West Bengal", 26.7271, 88.3953),
    ("Durgapur", "West Bengal", 23.5204, 87.3119),
    ("Asansol", "West Bengal", 23.6739, 86.9524),
    ("Ahmedabad", "Gujarat", 23.0225, 72.5714),
    ("Surat", "Gujarat", 21.1702, 72.8311),
    ("Vadodara", "Gujarat", 22.3072, 73.1812),
    ("Rajkot", "Gujarat", 22.3039, 70.8022),
    ("Gandhinagar", "Gujarat", 23.2156, 72.6369),
    ("Jaipur", "Rajasthan", 26.9124, 75.7873),
    ("Jodhpur", "Rajasthan", 26.2389, 73.0243),
    ("Udaipur", "Rajasthan", 24.5854, 73.7125),
    ("Kota", "Rajasthan", 25.2138, 75.8648),
    ("Ajmer", "Rajasthan", 26.4499, 74.6399),
    ("Lucknow", "Uttar Pradesh", 26.8467, 80.9462),
    ("Kanpur", "Uttar Pradesh", 26.4499, 80.3319),
    ("Varanasi", "Uttar Pradesh", 25.3176, 82.9739),
    ("Agra", "Uttar Pradesh", 27.1767, 78.0081),
    ("Prayagraj", "Uttar Pradesh", 25.4358, 81.8463),
    ("Meerut", "Uttar Pradesh", 28.9845, 77.7064),
    ("Ghaziabad", "Uttar Pradesh", 28.6692, 77.4538),
    ("Noida", "Uttar Pradesh", 28.5355, 77.3910),
    ("Gorakhpur", "Uttar Pradesh", 26.7606, 83.3732),
    ("Bareilly", "Uttar Pradesh", 28.3670, 79.4304),
    ("Bhopal", "Madhya Pradesh", 23.2599, 77.4126),
    ("Indore", "Madhya Pradesh", 22.7196, 75.8577),
    ("Gwalior", "Madhya Pradesh", 26.2183, 78.1828),
    ("Jabalpur", "Madhya Pradesh", 23.1815, 79.9864),
    ("Ujjain", "Madhya Pradesh", 23.1765, 75.7885),
    ("Patna", "Bihar", 25.5941, 85.1376),
    ("Gaya", "Bihar", 24.7955, 84.9994),
    ("Bhagalpur", "Bihar", 25.2425, 86.9842),
    ("Muzaffarpur", "Bihar", 26.1209, 85.3647),
    ("Ranchi", "Jharkhand", 23.3441, 85.3096),
    ("Jamshedpur", "Jharkhand", 22.8046, 86.2029),
    ("Dhanbad", "Jharkhand", 23.7957, 86.4304),
    ("Bhubaneswar", "Odisha", 20.2961, 85.8245),
    ("Cuttack", "Odisha", 20.4625, 85.8830),
    ("Rourkela", "Odisha", 22.2604, 84.8536),
    ("Raipur", "Chhattisgarh", 21.2514, 81.6296),
    ("Bhilai", "Chhattisgarh", 21.1938, 81.3509),
    ("Bilaspur", "Chhattisgarh", 22.0797, 82.1409),
    ("Chandigarh", "Chandigarh", 30.7333, 76.7794),
    ("Ludhiana", "Punjab", 30.9010, 75.8573),
    ("Amritsar", "Punjab", 31.6340, 74.8723),
    ("Jalandhar", "Punjab", 31.3260, 75.5762),
    ("Patiala", "Punjab", 30.3398, 76.3869),
    ("Gurugram", "Haryana", 28.4595, 77.0266),
    ("Faridabad", "Haryana", 28.4089, 77.3178),
    ("Panipat", "Haryana", 29.3909, 76.9635),
    ("Karnal", "Haryana", 29.6857, 76.9905),
    ("Dehradun", "Uttarakhand", 30.3165, 78.0322),
    ("Haridwar", "Uttarakhand", 29.9457, 78.1642),
    ("Roorkee", "Uttarakhand", 29.8543, 77.8880),
    ("Shimla", "Himachal Pradesh", 31.1048, 77.1734),
    ("Dharamshala", "Himachal Pradesh", 32.2190, 76.3234),
    ("Srinagar", "Jammu and Kashmir", 34.0837, 74.7973),
    ("Jammu", "Jammu and Kashmir", 32.7266, 74.8570),
    ("Guwahati", "Assam", 26.1445, 91.7362),
    ("Dibrugarh", "Assam", 27.4728, 94.9120),
    ("Silchar", "Assam", 24.8333, 92.7789),
    ("Imphal", "Manipur", 24.8170, 93.9368),
    ("Shillong", "Meghalaya", 25.5788, 91.8933),
    ("Agartala", "Tripura", 23.8315, 91.2868),
    ("Aizawl", "Mizoram", 23.7271, 92.7176),
    ("Kohima", "Nagaland", 25.6751, 94.1086),
    ("Itanagar", "Arunachal Pradesh", 27.0844, 93.6053),
    ("Gangtok", "Sikkim", 27.3389, 88.6065),
]


def seed_cities():
    db = SessionLocal()

    try:
        inserted = 0
        skipped = 0

        for name, state, latitude, longitude in CITIES:
            existing_city = db.scalar(
                select(City).where(
                    City.name == name,
                    City.state == state,
                )
            )

            if existing_city:
                skipped += 1
                continue

            db.add(
                City(
                    name=name,
                    state=state,
                    latitude=latitude,
                    longitude=longitude,
                )
            )
            inserted += 1

        db.commit()

        print(f"Total cities in seed list: {len(CITIES)}")
        print(f"New cities inserted: {inserted}")
        print(f"Existing cities skipped: {skipped}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_cities()
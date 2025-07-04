import os
import logging
from dotenv import load_dotenv
from typing import List
load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_env_variable(key: str) -> str:
    value = os.getenv(key)
    if not value:
        logger.error(f"Missing environment variable: {key}")
        raise EnvironmentError(f"{key} not found in .env or environment variables.")
    return value

API_KEY = get_env_variable("WEATHERAPI_KEY")
BASE_URL = get_env_variable("WEATHER_BASE_URL")
    
cities = [
        # Western Cape
        "Cape Town", "Stellenbosch", "Paarl", "Worcester", "George", "Knysna", "Mossel Bay", "Beaufort West", "Malmesbury", "Oudtshoorn",
        "Ceres", "Grabouw", "Vredenburg", "Caledon", "Swellendam", "Laingsburg", "Franschhoek", "Bonnievale", "Bredasdorp", "Langebaan",

        # Gauteng
        "Johannesburg", "Pretoria", "Soweto", "Benoni", "Boksburg", "Vereeniging", "Brakpan", "Krugersdorp", "Germiston", "Randburg",
        "Centurion", "Alberton", "Midrand", "Tembisa", "Roodepoort", "Springs", "Kempton Park", "Nigel", "Meyerton", "Carletonville",

        # KwaZulu-Natal
        "Durban", "Pietermaritzburg", "Richards Bay", "Newcastle", "Port Shepstone", "Empangeni", "Ulundi", "Ladysmith", "Margate", "Ixopo",
        "Vryheid", "Estcourt", "Hibberdene", "Howick", "Dundee", "Eshowe", "KwaDukuza", "Matatiele", "Umkomaas", "Mtubatuba",

        # Eastern Cape
        "East London", "Port Elizabeth", "Mthatha", "Queenstown", "Grahamstown", "Butterworth", "Aliwal North", "Humansdorp", "Uitenhage", "Qumbu",
        "Graaff-Reinet", "Despatch", "King William’s Town", "Stutterheim", "Mount Fletcher", "Mount Ayliff", "Cradock", "Fort Beaufort", "Burgersdorp", "Joubertina",

        # Free State
        "Bloemfontein", "Welkom", "Bethlehem", "Phuthaditjhaba", "Kroonstad", "Sasolburg", "Virginia", "Harrismith", "Ficksburg", "Parys",
        "Heilbron", "Ladybrand", "Senekal", "Fouriesburg", "Odendaalsrus", "Smithfield", "Trompsburg", "Zastron", "Wepener", "Theunissen",

        # Limpopo
        "Polokwane", "Thohoyandou", "Tzaneen", "Lephalale", "Musina", "Giyani", "Mokopane", "Phalaborwa", "Modimolle", "Bela-Bela",
        "Makhado", "Louis Trichardt", "Marble Hall", "Jane Furse", "Dendron", "Mogwadi", "Hoedspruit", "Sekhukhune", "Haenertsburg", "Groblersdal",

        # Mpumalanga
        "Nelspruit", "Witbank", "Secunda", "Ermelo", "Middelburg", "Barberton", "Sabie", "Graskop", "Hazyview", "White River",
        "Lydenburg", "Delmas", "Bethal", "Komatipoort", "Standerton", "Volksrust", "Skukuza", "Pilgrim's Rest", "Malelane", "Chrissiesmeer",

        # North West
        "Rustenburg", "Mahikeng", "Potchefstroom", "Klerksdorp", "Brits", "Zeerust", "Vryburg", "Lichtenburg", "Wolmaransstad", "Schweizer-Reneke",
        "Stilfontein", "Orkney", "Ventersdorp", "Mabopane", "Ga-Rankuwa", "Mmabatho", "Delareyville", "Coligny", "Ottosdal", "Groot-Marico",

        # Northern Cape
        "Kimberley", "Upington", "Springbok", "De Aar", "Kuruman", "Kathu", "Colesberg", "Douglas", "Calvinia", "Postmasburg",
        "Prieska", "Keimoes", "Pofadder", "Carnavon", "Britstown", "Victoria West", "Hopetown", "Hartswater", "Danielskuil", "Strydenburg"
    ]
    # Remove duplicates while preserving order
CITIES = set(cities)

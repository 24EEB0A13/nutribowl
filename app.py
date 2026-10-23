import streamlit as st
import requests
import re
import json
import html
import concurrent.futures
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from ddgs import DDGS


# =========================================================
# 1. PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="NutriBowl | Smart Cooking",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# 2. DESIGN
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

.stApp {
    background: #faf8f0;
    color: #263d31;
    font-family: 'DM Sans', sans-serif;
}

/* ---------- Force readable text colours (fixes white text) ---------- */
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] li {
    color: #263d31;
}
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] * {
    color: #65746a !important;
}
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #163b32 !important;
    font-weight: 600;
}
/* Nutrition metrics */
[data-testid="stMetric"] {
    background: #f6f9f2;
    border: 1px solid #e1e8de;
    border-radius: 12px;
    padding: 10px 14px;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    color: #52685b !important;
    font-weight: 600;
}
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #163b32 !important;
    font-weight: 700;
}
/* Inputs */
[data-testid="stTextInput"] input {
    border-radius: 10px;
    color: #163b32 !important;
    background: #ffffff !important;
}
/* Slider values */
[data-testid="stSliderThumbValue"],
[data-testid="stTickBarMin"],
[data-testid="stTickBarMax"] {
    color: #163b32 !important;
}
/* Expander */
[data-testid="stExpander"] {
    border: 1px solid #e1e8de;
    border-radius: 12px;
    background: white;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #163b32 !important;
}
/* Links */
[data-testid="stMarkdownContainer"] a {
    color: #176548 !important;
    font-weight: 600;
}
/* Recipe card (bordered container) */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border: 1px solid #e1e8de !important;
    border-radius: 20px !important;
    box-shadow: 0 7px 22px rgba(26,55,36,.05);
}

.block-container {
    max-width: 1450px;
    padding-top: 1.3rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    color: #163b32 !important;
    font-family: 'Playfair Display', serif !important;
}
.brand {
    color: #176548;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 18px;
}
.hero {
    display: grid;
    grid-template-columns: 1.1fr 0.9fr;
    gap: 28px;
    align-items: center;
    padding: 38px;
    border-radius: 26px;
    border: 1px solid #e0e7d9;
    background: linear-gradient(120deg,#eef2e7,#f7f4e9,#e5eddf);
    margin-bottom: 30px;
}
.hero h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(2.2rem,4vw,4rem);
    line-height: 1.12;
    margin: 12px 0;
}
.stApp .hero p {
    color: #52685b;
    font-size: 1rem;
    line-height: 1.8;
}
.eyebrow {
    color: #176548;
    font-weight: 700;
    font-size: .76rem;
    letter-spacing: 2px;
}
.hero img {
    width: 100%;
    height: 310px;
    object-fit: cover;
    border-radius: 20px;
}
.section-title {
    font-family: 'Playfair Display',serif;
    font-size: 1.8rem;
    color: #163b32;
    margin: 26px 0 4px;
}
.subtle {
    color: #65746a;
    margin-bottom: 18px;
}
.inspiration {
    background: white;
    border: 1px solid #e1e8de;
    border-radius: 17px;
    overflow: hidden;
    margin-bottom: 12px;
}
.inspiration img {
    width: 100%;
    height: 145px;
    object-fit: cover;
    display: block;
}
.inspiration div {
    padding: 12px 14px 15px;
}
.inspiration h4 {
    font-family: 'Playfair Display',serif;
    font-size: 1.05rem;
    margin: 0 0 5px;
    color: #163b32;
}
.stApp .inspiration p {
    font-size: .82rem;
    color: #65746a;
    margin: 0;
}
.match-pill {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 24px;
    background: #e8f3e8;
    color: #176548;
    border: 1px solid #d4e6d4;
    font-size: .8rem;
    font-weight: 700;
    margin: 5px 0 12px;
}
.chip {
    display: inline-block;
    background: #f0f4eb;
    border: 1px solid #e1e8da;
    color: #345443;
    border-radius: 20px;
    padding: 5px 9px;
    margin: 3px 4px 3px 0;
    font-size: .78rem;
}
.stButton > button, .stFormSubmitButton > button {
    background: #176548;
    color: white !important;
    border: none;
    border-radius: 11px;
    min-height: 44px;
    font-weight: 700;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: #104d37;
    color: white !important;
}
.footer {
    border-top: 1px solid #dce5d8;
    margin-top: 40px;
    padding-top: 20px;
    text-align: center;
    color: #65746a;
    font-size: .85rem;
}
@media(max-width:750px) {
    .hero { grid-template-columns: 1fr; padding: 22px; }
    .hero img { height: 230px; }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. HOMEPAGE
# =========================================================

st.markdown('<div class="brand">🥗 NUTRIBOWL</div>', unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div>
    <div class="eyebrow">YOUR KITCHEN, YOUR POSSIBILITIES</div>
    <h1>Good food starts with what you have.</h1>
    <p>
      Discover delicious Indian recipes from the ingredients already
      in your kitchen. Explore new meals, compare ingredient matches,
      and check nutrition information when available.
    </p>
  </div>
  <img
    src="https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=1200&q=85"
    alt="Colourful meal">
</div>
<div class="section-title">A little inspiration</div>
<div class="subtle">Everyday ingredients. Beautiful possibilities.</div>
""", unsafe_allow_html=True)

inspiration_cards = [
    ("South Indian", "Comforting, familiar flavours",
     "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=650&q=80"),
    ("Comfort Food", "Warm and satisfying meals",
     "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=650&q=80"),
    ("Fresh & Colourful", "Fresh ideas for your plate",
     "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=650&q=80"),
    ("Spice & Flavour", "Explore bold Indian flavours",
     "https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=650&q=80"),
]

columns = st.columns(4)
for col, (title, subtitle, picture) in zip(columns, inspiration_cards):
    with col:
        st.markdown(f"""
        <div class="inspiration">
          <img src="{picture}" alt="{html.escape(title)}">
          <div>
            <h4>{html.escape(title)}</h4>
            <p>{html.escape(subtitle)}</p>
          </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# 4. RECIPE SITES AND REQUEST SETTINGS
# =========================================================

ALLOWED_DOMAINS = [
    "hebbarskitchen.com",
    "indianhealthyrecipes.com",
    "vegrecipesofindia.com",
    "archanaskitchen.com",
    "tarladalal.com",
    "cookwithmanali.com",
    "rakskitchen.net",
    "subbuskitchen.com",
    "nishamadhulika.com",
    "sharmispassions.com",
    "masalaandchai.com",
    "pipingpotcurry.com",
    "mygingergarlickitchen.com",
    "swasthi.recipes",
    "food.ndtv.com",
    "sanjeevkapoor.com",
    "indianveggiedelight.com",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/130.0.0.0 Safari/537.36"
    )
}

FALLBACK_IMAGE = (
    "https://images.unsplash.com/photo-1547592180-85f173990554"
    "?auto=format&fit=crop&w=900&q=80"
)


# =========================================================
# 5. INGREDIENT NAME CLEANING AND ALIASES
# =========================================================

ALIASES = {
    "tomatoes": "tomato",
    "onions": "onion",
    "potatoes": "potato",
    "chillies": "chilli",
    "chilies": "chilli",
    "green chillies": "green chilli",
    "green chilies": "green chilli",
    "bell pepper": "capsicum",
    "bell peppers": "capsicum",
    "capsicums": "capsicum",
    "eggplant": "brinjal",
    "aubergine": "brinjal",
    "okra": "bhindi",
    "lady finger": "bhindi",
    "ladyfinger": "bhindi",
    "yogurt": "curd",
    "yoghurt": "curd",
    "dahi": "curd",
    "gram flour": "besan",
    "chickpea flour": "besan",
    "whole wheat flour": "atta",
    "wheat flour": "atta",
    "cilantro": "coriander",
    "coriander leaves": "coriander",
    "jeera": "cumin",
    "cumin seeds": "cumin",
    "haldi": "turmeric",
    "mirchi": "chilli",
    "green peas": "peas",
    "frozen peas": "peas",
    "garlic cloves": "garlic",
    "vegetable oil": "oil",
    "cooking oil": "oil",
    "chickpeas": "chickpea",
    "garbanzo beans": "chickpea",
    "kidney beans": "rajma",
    "semolina": "rava",
    "sooji": "rava",
    "flattened rice": "poha",
    "beaten rice": "poha",
    "rice flakes": "poha",
    "cottage cheese": "paneer",
    "groundnuts": "peanut",
    "groundnut": "peanut",
    "red lentils": "masoor dal",
    "pigeon pea": "toor dal",
    "black gram": "urad dal",
}


def clean_text(value):
    value = html.unescape(str(value or "")).lower()
    value = value.replace("_", " ").replace("-", " ")
    return re.sub(r"\s+", " ", value).strip()


def md_safe(text):
    """Stop '$' in scraped text from being rendered as LaTeX."""
    return str(text).replace("$", r"\$")


def normalise_ingredient(value):
    value = clean_text(value)
    value = re.sub(r"^\d+([./]\d+)?\s*", "", value)
    value = re.sub(
        r"\b(cups?|tablespoons?|tbsp|teaspoons?|tsp|grams?|g|"
        r"kilograms?|kg|ml|litres?|liters?|pinches?|cloves?|"
        r"pieces?|medium|large|small)\b",
        " ",
        value,
    )
    value = re.sub(r"\s+", " ", value).strip(" ,.;:")
    return ALIASES.get(value, value)


def split_ingredients(text):
    items = []
    for part in re.split(r"[,;\n]+", text):
        item = normalise_ingredient(part)
        if item and item not in items:
            items.append(item)
    return items


# If the ingredient is directly followed by one of these words, the line
# is a DIFFERENT product (e.g. "rice vinegar", "rice flour", "rice noodles").
NOT_FOLLOWED_BY = {
    "vinegar", "wine", "flour", "bran", "noodle", "noodles", "paper",
    "syrup", "stock", "broth", "cooker", "ketchup", "sauce", "cake",
    "flakes", "vermicelli", "starch", "malt", "cracker", "crackers",
    "seasoning", "essence", "extract",
}

# If the ingredient is directly preceded by one of these words, it is a
# different product (e.g. "coconut milk" is not "milk").
NOT_PRECEDED_BY = {
    "milk": {"coconut", "almond", "soy", "soya", "oat", "cashew", "rice"},
    "oil": {"essential"},
}


def _variants(word):
    """The word plus its simple singular forms."""
    forms = {word}
    if word.endswith("ies") and len(word) > 4:
        forms.add(word[:-3] + "y")
    if word.endswith("es") and len(word) > 3:
        forms.add(word[:-2])
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        forms.add(word[:-1])
    return forms


def _word_pattern(word):
    """Whole-word pattern accepting singular/plural forms."""
    forms = sorted(_variants(word), key=len, reverse=True)
    alternatives = "|".join(re.escape(f) for f in forms)
    return (
        r"(?<![a-z0-9])(?:" + alternatives + r")(?:e?s)?(?![a-z0-9])"
    )


def _phrase_present(phrase, text, check_context=True, base_name=None):
    """True if phrase appears as a real ingredient (not part of another one)."""
    for match in re.finditer(_word_pattern(phrase), text):
        if check_context:
            after = re.match(r"[\s,]*([a-z]+)", text[match.end():])
            before = re.search(r"([a-z]+)[\s]*$", text[:match.start()])

            if after and after.group(1) in NOT_FOLLOWED_BY:
                continue

            blocked_before = NOT_PRECEDED_BY.get(base_name or phrase, set())
            if before and before.group(1) in blocked_before:
                continue

        return True

    return False


def ingredient_in_text(ingredient, text):
    """Check ONE ingredient line (or text) for an ingredient."""
    ingredient = normalise_ingredient(ingredient)
    text = clean_text(text)

    if not ingredient:
        return False

    if _phrase_present(ingredient, text, base_name=ingredient):
        return True

    for alias, standard in ALIASES.items():
        if standard == ingredient:
            if _phrase_present(alias, text, base_name=ingredient):
                return True

    return False


def ingredient_in_lines(ingredient, lines):
    """Check each ingredient line separately so words never join across lines."""
    return any(ingredient_in_text(ingredient, line) for line in lines)


# =========================================================
# 6. RECIPE PAGE IMAGE EXTRACTION
# =========================================================

def usable_url(value):
    if isinstance(value, str):
        value = value.strip()
        if value.startswith("//"):
            value = "https:" + value
        if value.startswith("http://") or value.startswith("https://"):
            return value
    return None


def get_image(recipe, soup, page_url):
    """Try schema data, social image metadata, then recipe-page images."""
    image = recipe.get("image")

    if isinstance(image, list):
        image = image[0] if image else None

    if isinstance(image, dict):
        image = image.get("url") or image.get("contentUrl")

    image_url = usable_url(image)
    if image_url:
        return image_url

    for attribute, value in [
        ("property", "og:image"),
        ("name", "twitter:image"),
        ("property", "og:image:secure_url"),
    ]:
        tag = soup.find("meta", attrs={attribute: value})
        if tag:
            image_url = usable_url(tag.get("content"))
            if image_url:
                return image_url

    # Prefer an image whose alt text resembles the recipe title.
    title = clean_text(recipe.get("name", ""))

    for img in soup.find_all("img"):
        alt = clean_text(img.get("alt", ""))
        src = (
            img.get("src")
            or img.get("data-src")
            or img.get("data-lazy-src")
            or img.get("data-original")
        )
        image_url = usable_url(src)

        if image_url and title and alt and (
            title in alt or alt in title or any(
                word in alt for word in
                ["recipe", "curry", "rice", "paneer", "biryani"]
            )
        ):
            return image_url

    return FALLBACK_IMAGE


# =========================================================
# 7. PARSE RECIPE STRUCTURED DATA
# =========================================================

def is_recipe_object(obj):
    types = obj.get("@type", [])
    if isinstance(types, str):
        types = [types]
    return any(str(t).rstrip("/").split("/")[-1] == "Recipe" for t in types)


def find_recipe_objects(data):
    found = []

    if isinstance(data, dict):
        if is_recipe_object(data):
            found.append(data)

        if "@graph" in data:
            found.extend(find_recipe_objects(data["@graph"]))

    elif isinstance(data, list):
        for item in data:
            found.extend(find_recipe_objects(item))

    return found


def instructions_to_list(value):
    output = []

    if isinstance(value, str):
        text_value = BeautifulSoup(value, "html.parser").get_text(" ", strip=True)
        if text_value:
            output.append(text_value)

    elif isinstance(value, list):
        for item in value:
            output.extend(instructions_to_list(item))

    elif isinstance(value, dict):
        if value.get("text"):
            output.extend(instructions_to_list(value["text"]))
        elif value.get("itemListElement"):
            output.extend(instructions_to_list(value["itemListElement"]))
        elif value.get("name"):
            output.extend(instructions_to_list(value["name"]))

    return output


def clean_url(url):
    try:
        parsed = urlparse(url)
        return urlunparse((
            parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", "", ""
        ))
    except Exception:
        return url


def parse_recipe_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        recipe_objects = []

        for script in soup.find_all("script", type="application/ld+json"):
            raw = script.string or script.get_text()

            try:
                recipe_objects.extend(find_recipe_objects(json.loads(raw)))
            except (json.JSONDecodeError, TypeError):
                continue

        if not recipe_objects:
            return None

        recipe = recipe_objects[0]
        title = recipe.get("name", "")

        if isinstance(title, list):
            title = " ".join(map(str, title))

        if not title:
            return None

        ingredients = recipe.get("recipeIngredient", [])
        if not isinstance(ingredients, list):
            ingredients = []

        ingredients = [
            BeautifulSoup(str(item), "html.parser").get_text(" ", strip=True)
            for item in ingredients
        ]

        instructions = instructions_to_list(
            recipe.get("recipeInstructions", [])
        )

        # Nutrition values only if supplied by the recipe page.
        raw_nutrition = recipe.get("nutrition", {})
        if not isinstance(raw_nutrition, dict):
            raw_nutrition = {}

        nutrition = {}
        nutrition_map = {
            "calories": "Calories",
            "proteinContent": "Protein",
            "carbohydrateContent": "Carbs",
            "fatContent": "Fat",
        }

        for field, label in nutrition_map.items():
            value = raw_nutrition.get(field)
            if value not in (None, ""):
                nutrition[label] = str(value)

        servings = recipe.get("recipeYield")
        if isinstance(servings, list):
            servings = servings[0] if servings else None

        image = get_image(recipe, soup, url)

        return {
            "title": html.unescape(str(title)).strip(),
            "url": clean_url(url),
            "source": urlparse(url).netloc.replace("www.", ""),
            "image": image,
            "ingredients": ingredients,
            "instructions": instructions,
            "nutrition": nutrition,
            "servings": str(servings) if servings else "",
        }

    except (requests.RequestException, ValueError, TypeError, AttributeError):
        return None


# =========================================================
# 8. NUTRITION ESTIMATOR
# =========================================================
# Approximate nutrition per 100 g: (kcal, protein, carbs, fat).
# Estimates are shown only when ingredient quantities can be read.
# These are approximate generic values, not lab results.

NUTRITION_PER_100G = {
    "rice": (360, 7.0, 80.0, 0.7),
    "poha": (350, 6.5, 77.0, 1.0),
    "oats": (389, 16.9, 66.3, 6.9),
    "atta": (340, 13.0, 72.0, 2.5),
    "rava": (360, 12.0, 73.0, 1.0),
    "potato": (77, 2.0, 17.0, 0.1),
    "tomato": (18, 0.9, 3.9, 0.2),
    "onion": (40, 1.1, 9.3, 0.1),
    "peas": (81, 5.4, 14.5, 0.4),
    "carrot": (41, 0.9, 9.6, 0.2),
    "capsicum": (31, 1.0, 6.0, 0.3),
    "bhindi": (33, 1.9, 7.5, 0.2),
    "brinjal": (25, 1.0, 6.0, 0.2),
    "spinach": (23, 2.9, 3.6, 0.4),
    "paneer": (265, 18.3, 1.2, 20.8),
    "tofu": (76, 8.0, 1.9, 4.8),
    "curd": (61, 3.5, 4.7, 3.3),
    "milk": (61, 3.2, 4.8, 3.3),
    "chickpea": (164, 8.9, 27.4, 2.6),
    "rajma": (127, 8.7, 22.8, 0.5),
    "dal": (116, 9.0, 20.0, 0.4),
    "moong dal": (105, 7.0, 19.0, 0.4),
    "masoor dal": (116, 9.0, 20.0, 0.4),
    "toor dal": (120, 7.0, 21.0, 1.0),
    "besan": (387, 22.0, 58.0, 6.7),
    "egg": (143, 12.6, 0.7, 9.5),
    "chicken": (165, 31.0, 0.0, 3.6),
    "fish": (130, 26.0, 0.0, 3.0),
    "oil": (884, 0.0, 0.0, 100.0),
    "ghee": (900, 0.0, 0.0, 100.0),
    "peanut": (567, 25.8, 16.1, 49.2),
    "almond": (579, 21.2, 21.6, 49.9),
    "banana": (89, 1.1, 22.8, 0.3),
    "sugar": (387, 0.0, 100.0, 0.0),
    "coconut": (354, 3.3, 15.2, 33.5),
}

# Approximate grams in ONE CUP of each ingredient.
CUP_GRAMS = {
    "rice": 185, "poha": 100, "oats": 90, "atta": 120, "rava": 160,
    "paneer": 225, "tofu": 250, "curd": 245, "milk": 245,
    "oil": 218, "ghee": 227, "besan": 92,
    "dal": 200, "moong dal": 200, "masoor dal": 200, "toor dal": 200,
    "chickpea": 165, "rajma": 177,
    "potato": 150, "tomato": 180, "onion": 160, "peas": 145,
    "carrot": 128, "capsicum": 120, "spinach": 30, "brinjal": 100,
    "bhindi": 100, "peanut": 146, "almond": 143, "sugar": 200,
    "coconut": 80, "chicken": 140, "fish": 150, "banana": 150,
}

# Approximate grams of ONE whole item (for lines like "2 potatoes").
PIECE_GRAMS = {
    "egg": 50, "potato": 150, "tomato": 120, "onion": 110,
    "carrot": 60, "capsicum": 120, "banana": 118, "brinjal": 150,
}

UNICODE_FRACTIONS = {
    "½": "1/2", "¼": "1/4", "¾": "3/4",
    "⅓": "1/3", "⅔": "2/3", "⅛": "1/8",
}

_QTY_PATTERN = re.compile(
    r"(?<!\w)(\d+\s+\d+/\d+|\d+/\d+|\d+(?:\.\d+)?)\s*"
    r"(kg|kilograms?|g|grams?|ml|litres?|liters?|"
    r"cups?|tbsp|tablespoons?|tsp|teaspoons?)\b"
)


def _to_number(text):
    text = text.strip()
    try:
        if " " in text:
            whole, fraction = text.split(None, 1)
            numerator, denominator = fraction.split("/")
            return float(whole) + float(numerator) / float(denominator)
        if "/" in text:
            numerator, denominator = text.split("/")
            return float(numerator) / float(denominator)
        return float(text)
    except (ValueError, ZeroDivisionError):
        return None


def quantity_grams(line, name=None):
    """Estimated grams for a measurement line; None if it can't be read."""
    text = clean_text(line)
    for symbol, replacement in UNICODE_FRACTIONS.items():
        text = text.replace(symbol, " " + replacement)
    text = re.sub(r"\s+", " ", text).strip()

    match = _QTY_PATTERN.search(text)

    if not match:
        # Countable items such as "2 potatoes" or "2 eggs".
        count_match = re.match(r"^(\d+(?:\.\d+)?)\s+", text)
        if count_match and name in PIECE_GRAMS:
            return float(count_match.group(1)) * PIECE_GRAMS[name]
        return None

    amount = _to_number(match.group(1))
    if amount is None:
        return None

    unit = match.group(2)
    cup_weight = CUP_GRAMS.get(name, 150)

    if unit.startswith(("kg", "kilogram")):
        return amount * 1000
    if unit in ("g", "gram", "grams"):
        return amount
    if unit == "ml":
        return amount
    if unit.startswith(("litre", "liter")):
        return amount * 1000
    if unit.startswith(("tbsp", "tablespoon")):
        return amount * cup_weight / 16
    if unit.startswith(("tsp", "teaspoon")):
        return amount * cup_weight / 48
    if unit.startswith("cup"):
        return amount * cup_weight

    return None


def identify_nutrition_ingredient(line):
    """Find a known ingredient in an ingredient-list line."""
    text = clean_text(line)

    # Longer names first to avoid matching a generic word prematurely.
    for name in sorted(NUTRITION_PER_100G, key=len, reverse=True):
        if ingredient_in_text(name, text):
            return name

    return None


def estimate_nutrition(ingredients, servings_text=""):
    """
    Estimate nutrition only when quantities and ingredients can be
    interpreted. Return None if too little information is available.
    """
    totals = [0.0, 0.0, 0.0, 0.0]
    used_items = 0

    for line in ingredients:
        name = identify_nutrition_ingredient(line)
        if not name:
            continue

        grams = quantity_grams(line, name)

        # Never invent an amount for a recognised ingredient.
        if grams is None:
            continue

        values = NUTRITION_PER_100G[name]
        factor = grams / 100

        for i, value in enumerate(values):
            totals[i] += value * factor

        used_items += 1

    # Require multiple measured ingredients for a useful estimate.
    if used_items < 2:
        return None

    servings = 1
    if servings_text:
        serving_match = re.search(r"\d+", servings_text)
        if serving_match:
            servings = max(1, int(serving_match.group()))

    totals = [value / servings for value in totals]

    return {
        "Calories": f"~{round(totals[0])} kcal",
        "Protein": f"~{totals[1]:.1f} g",
        "Carbs": f"~{totals[2]:.1f} g",
        "Fat": f"~{totals[3]:.1f} g",
        "basis": "Estimated per serving from quantities the app could interpret",
    }


# =========================================================
# 9. SEARCH ACROSS LISTED RECIPE WEBSITES
# =========================================================

def is_allowed_url(url):
    try:
        host = (urlparse(url).hostname or "").lower()
        return any(
            host == domain or host.endswith("." + domain)
            for domain in ALLOWED_DOMAINS
        )
    except Exception:
        return False


def search_one_query(query):
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=5) or [])
    except Exception:
        return []


def search_recipes(user_ingredients):
    ingredient_text = ", ".join(user_ingredients)

    queries = [
        f"Indian recipes using {ingredient_text}",
        f"Indian dishes with {ingredient_text}",
        f"Indian regional recipes with {ingredient_text}",
    ]

    # Explicitly search every configured website.
    for domain in ALLOWED_DOMAINS:
        queries.append(f"site:{domain} recipe {ingredient_text}")

    # Additional searches for individual ingredients.
    for ingredient in user_ingredients[:3]:
        queries.append(f"Indian recipes using {ingredient}")

    queries = list(dict.fromkeys(queries))
    urls = []
    seen_urls = set()

    progress = st.progress(0, text="Searching Indian recipe websites...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(search_one_query, query): query
            for query in queries
        }

        total = max(1, len(futures))
        completed = 0

        for future in concurrent.futures.as_completed(futures):
            completed += 1
            progress.progress(
                int(completed / total * 40),
                text=f"Searching websites... {completed}/{total}",
            )

            try:
                results = future.result()
            except Exception:
                results = []

            for result in results:
                url = result.get("href") or result.get("url")
                if not url or not is_allowed_url(url):
                    continue

                url = clean_url(url)
                if url not in seen_urls:
                    seen_urls.add(url)
                    urls.append(url)

    # A bounded number of pages keeps search time manageable.
    urls = urls[:70]

    if not urls:
        progress.empty()
        return []

    recipes = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(parse_recipe_page, url): url
            for url in urls
        }

        total = max(1, len(futures))
        completed = 0

        for future in concurrent.futures.as_completed(futures):
            completed += 1
            progress.progress(
                40 + int(completed / total * 60),
                text=f"Reading recipe pages... {completed}/{total}",
            )

            try:
                recipe = future.result()
                if recipe:
                    recipes.append(recipe)
            except Exception:
                continue

    progress.empty()

    for recipe in recipes:
        matched = [
            item for item in user_ingredients
            if ingredient_in_lines(item, recipe["ingredients"])
        ]

        recipe["matched_ingredients"] = matched
        recipe["match_percentage"] = round(
            len(matched) / len(user_ingredients) * 100
        ) if user_ingredients else 0

        # Use recipe-site nutrition first; otherwise estimate if possible.
        if recipe["nutrition"]:
            recipe["nutrition_basis"] = "Provided by the recipe website"
        else:
            estimated = estimate_nutrition(
                recipe["ingredients"],
                recipe.get("servings", ""),
            )
            recipe["nutrition"] = estimated or {}
            recipe["nutrition_basis"] = (
                estimated["basis"] if estimated else
                "Nutrition information was unavailable or quantities were insufficient"
            )
            if estimated:
                recipe["nutrition"].pop("basis", None)

    # Deduplicate near-identical titles and URLs.
    unique = []
    seen_titles = set()
    seen_recipe_urls = set()

    recipes.sort(
        key=lambda r: (r["match_percentage"], len(r["matched_ingredients"])),
        reverse=True,
    )

    for recipe in recipes:
        title_key = re.sub(r"[^a-z0-9]", "", clean_text(recipe["title"]))
        url_key = recipe["url"]

        if not title_key or title_key in seen_titles or url_key in seen_recipe_urls:
            continue

        seen_titles.add(title_key)
        seen_recipe_urls.add(url_key)
        unique.append(recipe)

    return unique


# =========================================================
# 10. SEARCH FORM AND LIVE SLIDER
# =========================================================

st.markdown('<div class="section-title">What is in your kitchen?</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="subtle">Enter ingredients separated by commas and find '
    'recipes from Indian cooking websites.</div>',
    unsafe_allow_html=True,
)

# Outside the form: slider changes immediately and filters existing results.
minimum_match = st.slider(
    "Minimum ingredient match",
    min_value=1,
    max_value=100,
    value=75,
    step=1,
    format="%d%%",
    key="minimum_match_slider",
)

st.caption(
    f"Current threshold: {minimum_match}%. "
    "Move the slider to change which recipes are displayed."
)

with st.form("recipe_search_form"):
    ingredient_input = st.text_input(
        "YOUR INGREDIENTS",
        placeholder="e.g. rice, tomato, onion, potato, curd",
    )

    # width="stretch" on new Streamlit, use_container_width on older ones
    try:
        submitted = st.form_submit_button(
            "Discover my recipes  →", width="stretch"
        )
    except TypeError:
        submitted = st.form_submit_button(
            "Discover my recipes  →", use_container_width=True
        )


# =========================================================
# 11. KEEP RESULTS BETWEEN SLIDER CHANGES
# =========================================================

if "nutribowl_recipes" not in st.session_state:
    st.session_state.nutribowl_recipes = []

if "nutribowl_ingredients" not in st.session_state:
    st.session_state.nutribowl_ingredients = []

if submitted:
    ingredients = split_ingredients(ingredient_input)

    if not ingredients:
        st.warning("Please enter at least one ingredient.")
    else:
        st.session_state.nutribowl_ingredients = ingredients
        st.session_state.nutribowl_recipes = search_recipes(ingredients)

        if not st.session_state.nutribowl_recipes:
            st.warning(
                "No readable recipe pages were found. Some sites may block "
                "search access or may not expose structured recipe data. "
                "Try again with different ingredient names."
            )


# =========================================================
# 12. RECIPE CARDS
# =========================================================

def show_image(url):
    try:
        st.image(url, width="stretch")
    except TypeError:
        st.image(url, use_container_width=True)


all_recipes = st.session_state.nutribowl_recipes

if all_recipes:
    filtered = [
        recipe for recipe in all_recipes
        if recipe["match_percentage"] >= minimum_match
    ]

    filtered.sort(
        key=lambda r: (r["match_percentage"], len(r["matched_ingredients"])),
        reverse=True,
    )

    st.markdown('<div class="section-title">Your recipe discoveries</div>',
                unsafe_allow_html=True)
    st.caption(
        f"{len(filtered)} recipes meet the {minimum_match}% threshold. "
        f"{len(all_recipes)} unique recipes were collected."
    )

    if not filtered:
        st.info(
            "No recipes meet this match percentage. Move the slider lower "
            "to see more results."
        )

    for number, recipe in enumerate(filtered, start=1):
        # A real bordered container, so the widgets sit inside the card.
        with st.container(border=True):
            image_col, detail_col = st.columns([0.9, 1.4], gap="large")

            with image_col:
                show_image(recipe.get("image") or FALLBACK_IMAGE)

            with detail_col:
                st.markdown(f"### {number}. {md_safe(recipe['title'])}")
                st.markdown(
                    f'<span class="match-pill">'
                    f'{recipe["match_percentage"]}% ingredient match'
                    f'</span>',
                    unsafe_allow_html=True,
                )

                st.markdown("**Ingredients you already have**")
                chips = "".join(
                    f'<span class="chip">{html.escape(item)}</span>'
                    for item in recipe["matched_ingredients"]
                )
                st.markdown(
                    chips or "No matched ingredients.",
                    unsafe_allow_html=True,
                )

                st.markdown(
                    f"**Source:** {html.escape(recipe['source'])}"
                )
                st.markdown(
                    f"[Open original recipe ↗]({recipe['url']})"
                )

            nutrition = recipe.get("nutrition", {})

            if nutrition:
                st.markdown("**Nutrition per serving**")
                metric_cols = st.columns(4)
                for col, key in zip(
                    metric_cols,
                    ["Calories", "Protein", "Carbs", "Fat"],
                ):
                    with col:
                        st.metric(key, nutrition.get(key, "Not available"))

                st.caption(recipe.get("nutrition_basis", ""))
            else:
                st.caption(
                    "Calories and macros are unavailable for this recipe "
                    "because the source did not provide them and there was "
                    "not enough measurable ingredient information to "
                    "estimate them reliably."
                )

            with st.expander("View ingredients and cooking method"):
                if recipe["ingredients"]:
                    st.markdown("**Ingredients from the original recipe**")
                    for item in recipe["ingredients"]:
                        st.markdown(f"- {md_safe(item)}")
                else:
                    st.write(
                        "The source did not provide a structured "
                        "ingredient list."
                    )

                if recipe["instructions"]:
                    st.markdown("**Cooking method**")
                    for step, instruction in enumerate(
                        recipe["instructions"], start=1
                    ):
                        st.markdown(f"{step}. {md_safe(instruction)}")
                else:
                    st.write(
                        "The source did not expose structured cooking "
                        "instructions. Open the original recipe for the "
                        "full method."
                    )

elif not submitted:
    st.markdown("""
    <div style="background:white;border:1px solid #e1e8de;
    border-radius:18px;padding:22px;margin-top:15px;color:#52685b;">
      <strong style="color:#163b32;">Ready to discover something delicious?</strong>
      <p style="margin-bottom:0;">Add ingredients and click
      <em>Discover my recipes</em> to begin.</p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 13. FOOTER
# =========================================================

st.markdown("""
<div class="footer">
  <strong>NutriBowl</strong> · Make the most of what you have.
  <br>
  Recipe images, ingredients, instructions and nutrition depend on the
  information accessible from the original recipe sources.
</div>
""", unsafe_allow_html=True)

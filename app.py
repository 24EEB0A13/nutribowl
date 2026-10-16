
import streamlit as st
import random
import re

st.set_page_config(
    page_title="NutriBowl | Smart Cooking",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- DESIGN --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --green: #176548;
    --dark: #163b32;
    --sage: #e8efe3;
    --cream: #faf8f0;
    --line: #dce5d8;
}

.stApp {
    background: var(--cream);
    color: var(--dark);
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1450px;
    padding: 1.5rem 2rem 3rem;
}

h1, h2, h3 {
    color: var(--dark) !important;
    font-family: 'Playfair Display', Georgia, serif !important;
}

p, label, li, span, div {
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(250,248,240,.95);
}

.hero {
    background: linear-gradient(105deg, #eef2e7 0%, #f7f4e9 55%, #e5eddf 100%);
    border: 1px solid #e0e7d9;
    border-radius: 24px;
    padding: 34px;
    margin: 12px 0 24px;
}

.brand {
    font-size: 27px;
    font-weight: 700;
    color: var(--green);
    letter-spacing: -.8px;
}

.eyebrow {
    color: var(--green);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(35px, 4vw, 54px);
    font-weight: 700;
    line-height: 1.13;
    color: var(--dark);
    margin: 14px 0;
}

.hero-copy {
    font-size: 16px;
    line-height: 1.8;
    color: #4c6558;
    max-width: 650px;
}

.feature {
    background: rgba(255,255,255,.65);
    border: 1px solid rgba(220,229,216,.8);
    padding: 18px;
    border-radius: 16px;
    min-height: 142px;
}

.feature-icon {
    font-size: 25px;
    margin-bottom: 8px;
}

.feature-title {
    color: var(--green);
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 5px;
}

.feature-copy {
    color: #52685a;
    font-size: 13px;
    line-height: 1.6;
}

.section-panel {
    background: #eef3e9;
    border: 1px solid #dfe8da;
    border-radius: 20px;
    padding: 22px;
    margin: 18px 0;
}

.section-label {
    color: var(--green);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700;
}

.section-heading {
    color: var(--dark);
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 28px;
    font-weight: 700;
    margin: 5px 0 8px;
}

.muted {
    color: #617366;
    font-size: 14px;
    line-height: 1.6;
}

.pantry-box {
    background: #fffefa;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 20px;
    min-height: 150px;
}

.recipe-card {
    background: #fffefa;
    border: 1px solid #e0e6db;
    border-radius: 17px;
    overflow: hidden;
    margin-bottom: 12px;
    box-shadow: 0 3px 10px rgba(26, 60, 43, .04);
}

.recipe-card img {
    width: 100%;
    height: 175px;
    object-fit: cover;
}

.recipe-content {
    padding: 15px;
}

.recipe-title {
    font-weight: 700;
    font-size: 17px;
    color: var(--dark);
    margin-bottom: 6px;
}

.recipe-description {
    color: #607164;
    font-size: 12px;
    line-height: 1.6;
    min-height: 38px;
}

.match-pill {
    display: inline-block;
    color: #fff;
    background: var(--green);
    border-radius: 20px;
    padding: 5px 10px;
    font-size: 11px;
    font-weight: 700;
}

.ingredient-pill {
    display: inline-block;
    color: #315941;
    background: #e7efe1;
    padding: 5px 9px;
    margin: 3px 3px 3px 0;
    border-radius: 20px;
    font-size: 11px;
}

.nutrition {
    border-top: 1px solid #e8ede4;
    border-bottom: 1px solid #e8ede4;
    padding: 10px 0;
    margin: 10px 0;
    color: #41614c;
    font-size: 11px;
    line-height: 2;
}

div.stButton > button {
    background: var(--green);
    color: white;
    border: 1px solid var(--green);
    border-radius: 12px;
    font-weight: 700;
    padding: 10px 16px;
    transition: all .2s ease;
}

div.stButton > button:hover {
    background: #104d36;
    color: white;
    border-color: #104d36;
}

[data-testid="stSelectbox"] div,
[data-testid="stMultiSelect"] div {
    border-radius: 10px;
}

[data-baseweb="select"] > div {
    background-color: #fffefa !important;
    color: #163b32 !important;
    border-color: #d5e0d2 !important;
}

[data-baseweb="select"] span,
[data-baseweb="select"] input {
    color: #163b32 !important;
    -webkit-text-fill-color: #163b32 !important;
}

[data-baseweb="popover"], [role="listbox"] {
    background: #fffefa !important;
}

[role="option"] {
    background: #fffefa !important;
    color: #163b32 !important;
}

[role="option"]:hover {
    background: #e8efe3 !important;
}

[data-baseweb="tag"] {
    background: #dcebd6 !important;
}

[data-baseweb="tag"] span {
    color: #163b32 !important;
}

input, textarea {
    color: #163b32 !important;
    background: #fffefa !important;
}

[data-testid="stMetric"] {
    background: #f0f4eb;
    border: 1px solid #dfe8da;
    padding: 12px;
    border-radius: 12px;
}

hr {
    border-color: #dfe7da;
}

@media (max-width: 700px) {
    .block-container {
        padding: 1rem;
    }
    .hero {
        padding: 22px;
    }
}
</style>
""", unsafe_allow_html=True)

# -------------------- INGREDIENTS --------------------

INGREDIENTS = [
    "rice", "brown rice", "poha", "oats", "wheat flour", "bread",
    "pasta", "noodles", "semolina", "millet", "potato", "sweet potato",
    "tomato", "onion", "carrot", "peas", "spinach", "capsicum",
    "cauliflower", "cabbage", "broccoli", "cucumber", "corn", "beans",
    "mushroom", "pumpkin", "beetroot", "brinjal", "okra",
    "bottle gourd", "chickpeas", "kidney beans", "black beans",
    "moong dal", "toor dal", "masoor dal", "urad dal", "lentils",
    "soy chunks", "tofu", "paneer", "milk", "curd", "yogurt",
    "cheese", "eggs", "chicken", "fish", "peanuts", "almonds",
    "cashews", "sesame seeds", "chia seeds", "banana", "apple",
    "mango", "lemon", "coconut", "ginger", "garlic", "green chilli",
    "coriander", "mint", "curry leaves", "cumin", "mustard seeds",
    "turmeric", "chilli powder", "garam masala", "black pepper",
    "salt", "oil", "olive oil", "ghee", "butter", "honey",
    "jaggery", "dates", "raisins", "tomato puree", "coconut milk"
]

# -------------------- RECIPE DATA --------------------

BASE_RECIPES = [
    {"name":"Vegetable Pulao","ingredients":["rice","carrot","peas","onion","oil","cumin"],"method":"Cook rice with vegetables, cumin and seasoning until fluffy.","calories":320,"protein":7,"carbs":58,"fat":7,"time":25,"category":"Rice & Bowls","description":"Fragrant rice with everyday vegetables.","image":"photo-1512058564366-18510be2db19","tags":["Rice","Vegetarian"]},
    {"name":"Poha","ingredients":["poha","onion","peas","peanuts","oil","lemon"],"method":"Soften poha, sauté onion and peas, mix together and finish with lemon.","calories":280,"protein":7,"carbs":43,"fat":9,"time":15,"category":"Breakfast","description":"A light, tangy Indian breakfast favourite.","image":"photo-1547592180-85f173990554","tags":["Breakfast","Vegetarian"]},
    {"name":"Masala Oats","ingredients":["oats","tomato","onion","carrot","peas","oil"],"method":"Cook oats with chopped vegetables, spices and water until creamy.","calories":270,"protein":10,"carbs":42,"fat":7,"time":15,"category":"Breakfast","description":"Comforting oats with savoury vegetables.","image":"photo-1517673132405-a56a62b18caf","tags":["Oats","High Fibre"]},
    {"name":"Vegetable Upma","ingredients":["semolina","onion","carrot","peas","mustard seeds","oil"],"method":"Toast semolina, sauté vegetables and cook together with water.","calories":300,"protein":8,"carbs":49,"fat":8,"time":20,"category":"Breakfast","description":"Soft semolina with gently spiced vegetables.","image":"photo-1547592180-85f173990554","tags":["Breakfast","Vegetarian"]},
    {"name":"Aloo Paratha","ingredients":["wheat flour","potato","coriander","oil","salt"],"method":"Fill rolled wheat dough with seasoned potato and cook on a pan.","calories":350,"protein":8,"carbs":55,"fat":10,"time":30,"category":"Indian","description":"Golden flatbread with a savoury potato filling.","image":"photo-1565557623262-b51c2513a641","tags":["Indian","Comfort Food"]},
    {"name":"Chickpea Salad","ingredients":["chickpeas","tomato","cucumber","onion","lemon","coriander"],"method":"Combine cooked chickpeas and chopped vegetables with lemon and herbs.","calories":260,"protein":12,"carbs":42,"fat":5,"time":10,"category":"Salads","description":"Fresh, zesty and full of plant-based protein.","image":"photo-1512621776951-a57141f2eefd","tags":["Chickpeas","High Fibre"]},
    {"name":"Rajma Rice","ingredients":["kidney beans","rice","tomato","onion","ginger","garlic"],"method":"Simmer cooked kidney beans in tomato gravy and serve with rice.","calories":410,"protein":15,"carbs":72,"fat":7,"time":35,"category":"Rice & Bowls","description":"A hearty bowl of beans, rice and rich gravy.","image":"photo-1512058564366-18510be2db19","tags":["Rice","Protein"]},
    {"name":"Dal Rice","ingredients":["rice","moong dal","turmeric","cumin","garlic","oil"],"method":"Cook dal with spices and serve with rice.","calories":360,"protein":14,"carbs":62,"fat":7,"time":25,"category":"Indian","description":"Simple, warming lentils with rice.","image":"photo-1547592180-85f173990554","tags":["Lentils","Comfort Food"]},
    {"name":"Palak Paneer","ingredients":["spinach","paneer","onion","tomato","garlic","oil"],"method":"Cook spinach into a gravy and simmer with paneer.","calories":330,"protein":19,"carbs":15,"fat":22,"time":25,"category":"Indian","description":"Paneer in a creamy spinach-based sauce.","image":"photo-1565557623262-b51c2513a641","tags":["Paneer","Vegetarian"]},
    {"name":"Paneer Bhurji","ingredients":["paneer","tomato","onion","capsicum","turmeric","oil"],"method":"Crumble paneer and sauté with vegetables and spices.","calories":310,"protein":20,"carbs":13,"fat":21,"time":20,"category":"Indian","description":"A quick, savoury paneer scramble.","image":"photo-1565557623262-b51c2513a641","tags":["Paneer","High Protein"]},
    {"name":"Vegetable Fried Rice","ingredients":["rice","carrot","beans","capsicum","garlic","oil"],"method":"Stir-fry cooked rice with vegetables and garlic.","calories":330,"protein":7,"carbs":57,"fat":8,"time":20,"category":"Rice & Bowls","description":"Colourful rice with crisp vegetables.","image":"photo-1512058564366-18510be2db19","tags":["Rice","Quick"]},
    {"name":"Tomato Pasta","ingredients":["pasta","tomato","garlic","onion","olive oil","cheese"],"method":"Cook pasta and toss with tomato-garlic sauce and a little cheese.","calories":390,"protein":14,"carbs":62,"fat":11,"time":25,"category":"Pasta","description":"Pasta tossed in a bright tomato sauce.","image":"photo-1473093295043-cdd812d0e601","tags":["Pasta","Vegetarian"]},
    {"name":"Vegetable Sandwich","ingredients":["bread","cucumber","tomato","onion","cheese","butter"],"method":"Layer vegetables and cheese between bread and toast.","calories":320,"protein":12,"carbs":38,"fat":13,"time":10,"category":"Snacks","description":"A crisp sandwich for a quick meal.","image":"photo-1528735602780-2552fd46c7af","tags":["Quick","Vegetarian"]},
    {"name":"Oats Banana Bowl","ingredients":["oats","milk","banana","almonds","honey"],"method":"Cook oats in milk and top with banana, almonds and honey.","calories":350,"protein":13,"carbs":55,"fat":10,"time":10,"category":"Breakfast","description":"A naturally sweet and filling breakfast bowl.","image":"photo-1517673132405-a56a62b18caf","tags":["Oats","Breakfast"]},
    {"name":"Banana Smoothie","ingredients":["banana","milk","oats","almonds"],"method":"Blend banana, milk, oats and almonds until smooth.","calories":300,"protein":12,"carbs":48,"fat":8,"time":5,"category":"Drinks","description":"A creamy smoothie with a satisfying finish.","image":"photo-1505252585461-04db1eb84625","tags":["Smoothie","Quick"]},
    {"name":"Moong Dal Chilla","ingredients":["moong dal","onion","green chilli","coriander","oil"],"method":"Blend soaked dal into batter, add vegetables and cook like pancakes.","calories":250,"protein":15,"carbs":34,"fat":6,"time":20,"category":"Breakfast","description":"Savoury lentil pancakes with fresh herbs.","image":"photo-1547592180-85f173990554","tags":["Lentils","Protein"]},
    {"name":"Besan Chilla","ingredients":["wheat flour","onion","tomato","green chilli","coriander","oil"],"method":"Make a savoury batter with flour and vegetables and cook on a pan.","calories":260,"protein":11,"carbs":35,"fat":8,"time":15,"category":"Breakfast","description":"A fast savoury pancake with vegetables.","image":"photo-1547592180-85f173990554","tags":["Breakfast","Quick"]},
    {"name":"Egg Bhurji","ingredients":["eggs","onion","tomato","green chilli","oil"],"method":"Scramble eggs with sautéed onion, tomato and spices.","calories":270,"protein":18,"carbs":8,"fat":18,"time":12,"category":"Breakfast","description":"A spicy, protein-rich egg scramble.","image":"photo-1525351484163-7529414344d8","tags":["Egg","High Protein"]},
    {"name":"Boiled Egg Salad","ingredients":["eggs","cucumber","tomato","onion","lemon"],"method":"Slice boiled eggs and toss with chopped vegetables and lemon.","calories":240,"protein":17,"carbs":10,"fat":14,"time":15,"category":"Salads","description":"A fresh salad with satisfying protein.","image":"photo-1512621776951-a57141f2eefd","tags":["Egg","Protein"]},
    {"name":"Tofu Stir-Fry","ingredients":["tofu","broccoli","carrot","capsicum","garlic","oil"],"method":"Sauté tofu and vegetables until cooked but still slightly crisp.","calories":290,"protein":19,"carbs":20,"fat":15,"time":20,"category":"Rice & Bowls","description":"Plant-based protein with colourful vegetables.","image":"photo-1512621776951-a57141f2eefd","tags":["Tofu","Vegan"]},
    {"name":"Chicken Rice Bowl","ingredients":["chicken","rice","carrot","peas","garlic","oil"],"method":"Cook seasoned chicken thoroughly and serve with rice and vegetables.","calories":430,"protein":32,"carbs":54,"fat":10,"time":30,"category":"Rice & Bowls","description":"A filling bowl with chicken and vegetables.","image":"photo-1512058564366-18510be2db19","tags":["Chicken","High Protein"]},
    {"name":"Fish with Vegetables","ingredients":["fish","broccoli","carrot","lemon","black pepper","oil"],"method":"Season fish, cook thoroughly and serve with vegetables and lemon.","calories":340,"protein":30,"carbs":18,"fat":15,"time":25,"category":"Main Course","description":"A simple meal with fish and fresh vegetables.","image":"photo-1467003909585-2f8a72700288","tags":["Fish","High Protein"]},
    {"name":"Sweet Potato Bowl","ingredients":["sweet potato","chickpeas","spinach","lemon","olive oil"],"method":"Roast or steam sweet potato and serve with chickpeas and spinach.","calories":360,"protein":13,"carbs":59,"fat":9,"time":25,"category":"Rice & Bowls","description":"A colourful plant-based bowl with fibre.","image":"photo-1512621776951-a57141f2eefd","tags":["Vegan","High Fibre"]},
    {"name":"Corn Salad","ingredients":["corn","tomato","cucumber","lemon","coriander"],"method":"Mix cooked corn with chopped vegetables, herbs and lemon.","calories":210,"protein":6,"carbs":42,"fat":3,"time":10,"category":"Salads","description":"Sweet corn with a bright citrus dressing.","image":"photo-1512621776951-a57141f2eefd","tags":["Salad","Quick"]},
    {"name":"Lentil Soup","ingredients":["lentils","tomato","onion","carrot","garlic","cumin"],"method":"Simmer lentils and vegetables with water and spices until soft.","calories":280,"protein":17,"carbs":45,"fat":4,"time":30,"category":"Soups","description":"A warming bowl of lentils and vegetables.","image":"photo-1547592180-85f173990554","tags":["Lentils","High Fibre"]}
]

# -------------------- CREATE 200 SUGGESTIONS --------------------

VARIATIONS = [
    ("Classic", None),
    ("Spinach Edition", "spinach"),
    ("Tomato Edition", "tomato"),
    ("Carrot Edition", "carrot"),
    ("Peas Edition", "peas"),
    ("Capsicum Edition", "capsicum"),
    ("Garlic Edition", "garlic"),
    ("Lemon Edition", "lemon")
]

recipes = []

for base in BASE_RECIPES:
    for variation_name, extra in VARIATIONS:
        recipe = base.copy()
        recipe["ingredients"] = base["ingredients"].copy()
        recipe["tags"] = base["tags"].copy()

        if extra and extra not in recipe["ingredients"]:
            recipe["ingredients"].append(extra)

        if variation_name != "Classic":
            recipe["name"] = f"{base['name']} - {variation_name}"

        recipe["variation"] = variation_name

        if extra and extra not in base["ingredients"]:
            recipe["calories"] = base["calories"] + 8
            recipe["protein"] = round(base["protein"] + 0.3, 1)
            recipe["carbs"] = round(base["carbs"] + 1.5, 1)
            recipe["fat"] = round(base["fat"] + 0.1, 1)

        recipes.append(recipe)

# -------------------- FUNCTIONS --------------------

def normalise(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def match_recipe(recipe, pantry):
    required = set(normalise(x) for x in recipe["ingredients"])
    available = set(normalise(x) for x in pantry)
    matched = required & available
    missing = required - available
    score = round(100 * len(matched) / len(required)) if required else 0
    return score, sorted(matched), sorted(missing)

def substitutions_for(recipe, pantry):
    available = set(normalise(x) for x in pantry)
    required = set(normalise(x) for x in recipe["ingredients"])

    swaps = {
        "butter": "olive oil",
        "ghee": "olive oil",
        "oil": "olive oil",
        "honey": "dates"
    }

    result = []
    for original, replacement in swaps.items():
        if original in available and original in required:
            if replacement not in required:
                result.append((original, replacement))
    return result

def food_image(recipe):
    return (
        "https://images.unsplash.com/" + recipe["image"]
        + "?auto=format&fit=crop&w=900&q=80"
    )

# -------------------- HEADER --------------------

header_left, header_right = st.columns([3, 1])

with header_left:
    st.markdown(
        '<div class="brand">🥗 NutriBowl</div>'
        '<div class="muted">SMART COOKING &nbsp; • &nbsp; BETTER EATING</div>',
        unsafe_allow_html=True
    )

with header_right:
    st.markdown(
        '<div style="text-align:right;padding-top:10px;color:#176548;">'
        '🌿 Healthy Meals &nbsp; ♥</div>',
        unsafe_allow_html=True
    )

# -------------------- HERO --------------------

hero_left, hero_right = st.columns([1.15, 0.85], gap="large")

with hero_left:
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">Your kitchen, reimagined</div>
        <div class="hero-title">Good food starts<br>with what you have.</div>
        <div class="hero-copy">
            Turn everyday ingredients into satisfying meal ideas.
            Discover recipes, explore estimated nutrition, and find
            thoughtful ingredient alternatives — all in one place.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin:0 0 25px;">
      <div class="feature" style="flex:1;min-width:145px;">
        <div class="feature-icon">🍲</div>
        <div class="feature-title">Discover recipes</div>
        <div class="feature-copy">Find dishes that match your pantry.</div>
      </div>
      <div class="feature" style="flex:1;min-width:145px;">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Understand nutrition</div>
        <div class="feature-copy">Explore calories and macronutrients.</div>
      </div>
      <div class="feature" style="flex:1;min-width:145px;">
        <div class="feature-icon">🌿</div>
        <div class="feature-title">Smarter swaps</div>
        <div class="feature-copy">Explore ingredient alternatives.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with hero_right:
    st.image(
        "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1100&q=85",
        use_container_width=True
    )
    st.caption("Real food. Thoughtful choices.")

# -------------------- PANTRY --------------------

st.markdown("""
<div class="section-panel">
  <div class="section-label">01 / Pantry</div>
  <div class="section-heading">What's in your kitchen?</div>
  <div class="muted">Choose ingredients you have and add your quantities if you know them.</div>
</div>
""", unsafe_allow_html=True)

if "pantry" not in st.session_state:
    st.session_state.pantry = {}

input_col, pantry_col = st.columns([1.1, 0.9], gap="large")

with input_col:
    with st.container(border=True):
        ingredient = st.selectbox(
            "Ingredient",
            ["Choose an ingredient"] + INGREDIENTS,
            key="ingredient_choice"
        )
        custom_ingredient = st.text_input(
            "Or type another ingredient",
            placeholder="e.g. zucchini"
        )

        qty_col, unit_col = st.columns(2)
        with qty_col:
            quantity = st.number_input(
                "Quantity",
                min_value=0.1,
                max_value=999.0,
                value=1.0,
                step=0.5
            )
        with unit_col:
            unit = st.selectbox(
                "Measure",
                ["Piece", "Bowl", "Cup", "Gram", "Kilogram", "Spoon", "Tablespoon"]
            )

        if st.button("＋ Add to pantry", use_container_width=True):
            chosen = custom_ingredient.strip().lower()

            if not chosen and ingredient != "Choose an ingredient":
                chosen = ingredient

            if chosen:
                st.session_state.pantry[chosen] = {
                    "quantity": quantity,
                    "unit": unit
                }
                st.rerun()
            else:
                st.warning("Choose or type an ingredient first.")

with pantry_col:
    with st.container(border=True):
        pantry_header, clear_col = st.columns([2, 1])

        with pantry_header:
            st.markdown("### 🧺 Your pantry")

        with clear_col:
            if st.button("Clear pantry", use_container_width=True):
                st.session_state.pantry = {}
                st.session_state.pop("matching_recipes", None)
                st.rerun()

        if st.session_state.pantry:
            for name, detail in st.session_state.pantry.items():
                item_col, remove_col = st.columns([4, 1])
                with item_col:
                    st.markdown(
                        f"**{name.title()}** — "
                        f"{detail['quantity']:g} {detail['unit'].lower()}"
                    )
                with remove_col:
                    if st.button("✕", key="remove_" + name):
                        del st.session_state.pantry[name]
                        st.rerun()
        else:
            st.markdown("""
            <div style="text-align:center;padding:28px 10px;color:#718474;">
              <div style="font-size:42px;">🥬</div>
              <b>Your pantry is empty</b><br>
              Add a few ingredients above to unlock recipe suggestions.
            </div>
            """, unsafe_allow_html=True)

# -------------------- DISCOVERY CONTROLS --------------------

st.markdown("""
<div class="section-panel">
  <div class="section-label">02 / Discover</div>
  <div class="section-heading">Find your next favourite meal</div>
  <div class="muted">Choose your match threshold, category and food goal.</div>
</div>
""", unsafe_allow_html=True)

filter_a, filter_b, filter_c, filter_d = st.columns([1.2, 1, 1, 0.8])

with filter_a:
    minimum_match = st.slider(
        "Minimum ingredient match",
        25, 100, 75, 5
    )

with filter_b:
    category = st.selectbox(
        "Recipe category",
        ["All categories", "Breakfast", "Indian", "Rice & Bowls",
         "Salads", "Pasta", "Snacks", "Drinks", "Soups", "Main Course"]
    )

with filter_c:
    goal = st.selectbox(
        "What matters most to you?",
        ["Best match", "Lower calories", "Higher protein", "Quick meals"]
    )

with filter_d:
    st.write("")
    st.write("")
    search_clicked = st.button(
        "⌕ Find Recipes",
        use_container_width=True
    )

# -------------------- RECIPE MATCHING --------------------

if search_clicked:
    pantry = list(st.session_state.pantry.keys())

    if not pantry:
        st.warning("Add ingredients to your pantry first.")
    else:
        results = []

        for recipe in recipes:
            score, matched, missing = match_recipe(recipe, pantry)

            if score < minimum_match:
                continue

            if category != "All categories" and recipe["category"] != category:
                continue

            result = recipe.copy()
            result["score"] = score
            result["matched"] = matched
            result["missing"] = missing
            results.append(result)

        if goal == "Best match":
            results.sort(key=lambda r: (r["score"], len(r["matched"])), reverse=True)
        elif goal == "Lower calories":
            results.sort(key=lambda r: r["calories"])
        elif goal == "Higher protein":
            results.sort(key=lambda r: r["protein"], reverse=True)
        else:
            results.sort(key=lambda r: r["time"])

        st.session_state.matching_recipes = results
        st.session_state.search_pantry = pantry

# -------------------- RESULTS --------------------

if "matching_recipes" in st.session_state:
    results = st.session_state.matching_recipes

    st.markdown("---")
    results_title, results_count = st.columns([3, 1])

    with results_title:
        st.markdown("## 👩‍🍳 Your recipe matches")

    with results_count:
        st.markdown(
            f'<div style="text-align:right;padding-top:15px;color:#176548;">'
            f'{len(results)} ideas found</div>',
            unsafe_allow_html=True
        )

    if not results:
        st.info(
            "No recipes match these settings. Try lowering the slider, "
            "choosing another category or adding ingredients."
        )
    else:
        display_limit = st.selectbox(
            "Recipes to show",
            [10, 20, 30, 50, 100, 200],
            index=2
        )

        results = results[:display_limit]

        for start in range(0, len(results), 3):
            card_cols = st.columns(3, gap="medium")

            for col, recipe in zip(card_cols, results[start:start + 3]):
                with col:
                    with st.container(border=True):
                        st.image(
                            food_image(recipe),
                            use_container_width=True
                        )

                        st.markdown(
                            f'<span class="match-pill">{recipe["score"]}% match</span>',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f'<div class="recipe-title">{recipe["name"]}</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f'<div class="muted">⏱ {recipe["time"]} min '
                            f'&nbsp; • &nbsp; {recipe["category"]}</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f'<div class="recipe-description">{recipe["description"]}</div>',
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f'<div class="nutrition">'
                            f'🔥 {recipe["calories"]} kcal &nbsp; '
                            f'💪 {recipe["protein"]} g protein<br>'
                            f'🌾 {recipe["carbs"]} g carbs &nbsp; '
                            f'🫒 {recipe["fat"]} g fat'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                        for tag in recipe["tags"]:
                            st.markdown(
                                f'<span class="ingredient-pill">{tag}</span>',
                                unsafe_allow_html=True
                            )

                        with st.expander("View recipe"):
                            st.markdown("**Ingredients**")
                            for item in recipe["ingredients"]:
                                if item in recipe["matched"]:
                                    st.write(f"✅ {item.title()}")
                                else:
                                    st.write(f"＋ {item.title()}")

                            st.markdown("**Preparation**")
                            st.write(recipe["method"])

                            st.markdown("**You already have**")
                            st.write(
                                ", ".join(x.title() for x in recipe["matched"])
                                or "No matching ingredients"
                            )

                            st.markdown("**You may still need**")
                            st.write(
                                ", ".join(x.title() for x in recipe["missing"])
                                or "You have all listed ingredients"
                            )

                            swaps = substitutions_for(
                                recipe,
                                st.session_state.search_pantry
                            )

                            st.markdown("**Possible ingredient swaps**")
                            if swaps:
                                for original, replacement in swaps:
                                    st.write(
                                        f"{original.title()} → {replacement.title()}"
                                    )
                            else:
                                st.write(
                                    "No relevant swap suggestion for your current ingredients."
                                )

# -------------------- FOOTER --------------------

st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:20px 0;">
  <div class="brand">🥗 NutriBowl</div>
  <p class="muted">Good food. Thoughtful choices. One ingredient at a time.</p>
  <p style="font-size:11px;color:#879488;">
    Nutrition figures are estimates per serving, not medical advice.
    Ingredient quantities do not currently adjust the nutrition estimates.
  </p>
</div>
""", unsafe_allow_html=True)

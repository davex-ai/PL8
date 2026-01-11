import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# Import your models and DB setup
from db import engine, SessionLocal
from models import Base, Category, Product, Review

# Load environment variables
load_dotenv()

# Sample product data (converted from JS)
products = [
    {
        "name": "Fresh organic apple 1kg simla morning",
        "image": "/uploads/products/fresh-apples.png",
        "price": 120.25,
        "stock": 80,
        "category": "Fruits",
        "rating": 4.5,
        "num_reviews": 45,
        "reviews": [
            {"rating": 5, "comment": "Sweet and crisp."}
        ]
    },
    {
        "name": "Organic fresh venilla farm watermelon 5kg",
        "image": "/uploads/products/watermelon.png",
        "price": 50.30,
        "stock": 30,
        "category": "Fruits",
        "rating": 3.2,
        "num_reviews": 32,
        "reviews": [
            {"rating": 4, "comment": "Juicy and refreshing."}
        ]
    },
    {
        "name": "Fresh Organic Carrots Bundle",
        "image": "/uploads/products/carrots.png",
        "price": 8.99,
        "stock": 150,
        "category": "Fruits",
        "rating": 4.7,
        "num_reviews": 65,
        "reviews": [
            {"rating": 5, "comment": "Crunchy and sweet!"}
        ]
    },
    {
        "name": "Rainbow Bell Peppers Trio",
        "image": "/uploads/products/bell-peppers.png",
        "price": 12.50,
        "stock": 80,
        "category": "Fruits",
        "rating": 4.5,
        "num_reviews": 42,
        "reviews": [
            {"rating": 5, "comment": "Vibrant and flavorful."}
        ]
    },
    {
        "name": "Ripe Bananas - 6 Pack",
        "image": "/uploads/products/bananas.png",
        "price": 5.99,
        "stock": 200,
        "category": "Fruits",
        "rating": 4.6,
        "num_reviews": 120,
        "reviews": [
            {"rating": 5, "comment": "Perfectly ripe every time."}
        ]
    },
    {
        "name": "Juicy Watermelon Slices",
        "image": "/uploads/products/watermelon-slices.png",
        "price": 7.50,
        "stock": 90,
        "category": "Fruits",
        "rating": 4.9,
        "num_reviews": 110,
        "reviews": [
            {"rating": 5, "comment": "So juicy and refreshing!"}
        ]
    },
    {
        "name": "Sweet Yellow Mangoes - 4 Pack",
        "image": "/uploads/products/yellow-mangoes.png",
        "price": 14.99,
        "stock": 75,
        "category": "Fruits",
        "rating": 4.7,
        "num_reviews": 60,
        "reviews": [
            {"rating": 5, "comment": "Buttery and sweet."}
        ]
    },
    {
        "name": "Creamy Avocado - 3 Pack",
        "image": "/uploads/products/avocado.png",
        "price": 10.99,
        "stock": 85,
        "category": "Fruits",
        "rating": 4.9,
        "num_reviews": 95,
        "reviews": [
            {"rating": 5, "comment": "So creamy — perfect for toast!"}
        ]
    },
    {
        "name": "Zesty Oranges - 6 Pack",
        "image": "/uploads/products/oranges.png",
        "price": 8.50,
        "stock": 110,
        "category": "Fruits",
        "rating": 4.7,
        "num_reviews": 78,
        "reviews": [
            {"rating": 5, "comment": "Bright and full of vitamin C."}
        ]
    },
    {
        "name": "Ruby Red Pomegranate",
        "image": "/uploads/products/pomegranate.png",
        "price": 9.50,
        "stock": 60,
        "category": "Fruits",
        "rating": 4.8,
        "num_reviews": 45,
        "reviews": [
            {"rating": 5, "comment": "Bursting with flavor!"}
        ]
    },
    {
        "name": "Tropical Mango Juice Blend",
        "image": "/uploads/products/mango-juice.png",
        "price": 9.99,
        "stock": 100,
        "category": "Fruits",
        "rating": 4.8,
        "num_reviews": 88,
        "reviews": [
            {"rating": 5, "comment": "Refreshing and naturally sweet!"}
        ]
    },
    {
        "name": "Spiky Durian Whole Fruit",
        "image": "/uploads/products/durian.png",
        "price": 25.00,
        "stock": 30,
        "category": "Fruits",
        "rating": 3.8,
        "num_reviews": 25,
        "reviews": [
            {"rating": 5, "comment": "Bold flavor — worth it!"}
        ]
    },
    {
        "name": "Angie's Boomchickapop Sweet and Wonnies",
        "image": "/uploads/products/angies-pops.png",
        "price": 238.85,
        "stock": 120,
        "category": "Snacks",
        "rating": 4.6,
        "num_reviews": 85,
        "reviews": [
            {"rating": 5, "comment": "Addictive snack!"}
        ]
    },
    {
        "name": "Blue Diamond Almonds Lightly Salted",
        "image": "/uploads/products/blue-diamond-almonds.png",
        "price": 238.85,
        "stock": 120,
        "category": "Snacks",
        "rating": 4.8,
        "num_reviews": 88,
        "reviews": [
            {"rating": 5, "comment": "Perfect crunchy snack."}
        ]
    },
    {
        "name": "Best snacks with hazel nut pack 200gm",
        "image": "/uploads/products/hazel-nuts.png",
        "price": 145.00,
        "stock": 60,
        "category": "Snacks",
        "rating": 5.0,
        "num_reviews": 50,
        "reviews": [
            {"rating": 5, "comment": "Best nuts I’ve ever had!"}
        ]
    },
    {
        "name": "Sweet crunchy nut mix 250gm pack",
        "image": "/uploads/products/nut-mix.png",
        "price": 120.25,
        "stock": 50,
        "category": "Snacks",
        "rating": 5.0,
        "num_reviews": 50,
        "reviews": [
            {"rating": 5, "comment": "Perfect blend of crunch and flavor."}
        ]
    },
    {
        "name": "Dried Mango Slices Snack Pack",
        "image": "/uploads/products/dried-mango.png",
        "price": 11.50,
        "stock": 120,
        "category": "Snacks",
        "rating": 4.6,
        "num_reviews": 70,
        "reviews": [
            {"rating": 5, "comment": "Chewy, tangy, and addictive!"}
        ]
    },
    {
        "name": "Popchips Original Sea Salt",
        "image": "/uploads/products/popchips.jpg",
        "price": 18.99,
        "stock": 90,
        "category": "Snacks",
        "rating": 4.5,
        "num_reviews": 60,
        "reviews": [
            {"rating": 5, "comment": "Light, airy, and satisfying!"}
        ]
    },
    {
        "name": "Cheez-It Original Baked Snack",
        "image": "/uploads/products/cheez-it.png",
        "price": 16.50,
        "stock": 100,
        "category": "Snacks",
        "rating": 4.7,
        "num_reviews": 80,
        "reviews": [
            {"rating": 5, "comment": "Cheesy, crunchy, can’t stop eating!"}
        ]
    },
    {
        "name": "Oreo Original Chocolate Sandwich Cookies",
        "image": "/uploads/products/oreos.png",
        "price": 14.99,
        "stock": 120,
        "category": "Snacks",
        "rating": 4.9,
        "num_reviews": 200,
        "reviews": [
            {"rating": 5, "comment": "Classic favorite — twist, lick, dunk!"}
        ]
    },
    {
        "name": "Lay's Classic Potato Chips",
        "image": "/uploads/products/lays.png",
        "price": 12.99,
        "stock": 150,
        "category": "Snacks",
        "rating": 4.6,
        "num_reviews": 180,
        "reviews": [
            {"rating": 5, "comment": "Betcha can't eat just one!"}
        ]
    },
    {
        "name": "Nature's Trail Mix - Nuts & Berries",
        "image": "/uploads/products/trail-mix.png",
        "price": 22.00,
        "stock": 70,
        "category": "Snacks",
        "rating": 4.8,
        "num_reviews": 65,
        "reviews": [
            {"rating": 5, "comment": "Perfect healthy on-the-go snack!"}
        ]
    },
    {
        "name": "Nature Valley Crunchy Granola Bars",
        "image": "/uploads/products/granola-bars.png",
        "price": 19.99,
        "stock": 110,
        "category": "Snacks",
        "rating": 4.5,
        "num_reviews": 90,
        "reviews": [
            {"rating": 4, "comment": "Great for breakfast or hiking!"}
        ]
    },
    {
        "name": "Haribo Gold-Bears Gummy Candy",
        "image": "/uploads/products/gummy-bears.png",
        "price": 10.99,
        "stock": 130,
        "category": "Snacks",
        "rating": 4.7,
        "num_reviews": 140,
        "reviews": [
            {"rating": 5, "comment": "Kid and adult favorite!"}
        ]
    },
    {
        "name": "Organic Cage-Free Grade A Large Brown Eggs",
        "image": "/uploads/products/organic-eggs.png",
        "price": 32.85,
        "stock": 80,
        "category": "Dairy & Eggs",
        "rating": 4.0,
        "num_reviews": 40,
        "reviews": [
            {"rating": 5, "comment": "Always fresh and reliable."}
        ]
    },
    {
        "name": "Organic Whole Milk - 1 Gallon",
        "image": "/uploads/products/whole-milk.png",
        "price": 28.50,
        "stock": 60,
        "category": "Dairy & Eggs",
        "rating": 4.6,
        "num_reviews": 75,
        "reviews": [
            {"rating": 5, "comment": "Rich, creamy, and pasture-raised."}
        ]
    },
    {
        "name": "Chobani Plain Greek Yogurt - 32oz",
        "image": "/uploads/products/greek-yogurt.png",
        "price": 34.99,
        "stock": 70,
        "category": "Dairy & Eggs",
        "rating": 4.8,
        "num_reviews": 110,
        "reviews": [
            {"rating": 5, "comment": "High protein and super smooth!"}
        ]
    },
    {
        "name": "Organic Salted Butter - 16oz",
        "image": "/uploads/products/butter.png",
        "price": 22.99,
        "stock": 50,
        "category": "Dairy & Eggs",
        "rating": 4.7,
        "num_reviews": 60,
        "reviews": [
            {"rating": 5, "comment": "Perfect for baking and toast!"}
        ]
    },
    {
        "name": "Aged Sharp Cheddar Block",
        "image": "/uploads/products/cheddar.png",
        "price": 26.50,
        "stock": 45,
        "category": "Dairy & Eggs",
        "rating": 4.9,
        "num_reviews": 50,
        "reviews": [
            {"rating": 5, "comment": "Bold, sharp, and melts perfectly!"}
        ]
    },
    {
        "name": "Organic Low-Fat Cottage Cheese",
        "image": "/uploads/products/cottage-cheese.png",
        "price": 19.99,
        "stock": 55,
        "category": "Dairy & Eggs",
        "rating": 4.4,
        "num_reviews": 40,
        "reviews": [
            {"rating": 5, "comment": "Great for high-protein meals."}
        ]
    },
    {
        "name": "Organic Sour Cream - 16oz",
        "image": "/uploads/products/sour-cream.png",
        "price": 15.50,
        "stock": 65,
        "category": "Dairy & Eggs",
        "rating": 4.6,
        "num_reviews": 35,
        "reviews": [
            {"rating": 5, "comment": "Perfect for tacos and baked potatoes."}
        ]
    },
    {
        "name": "Farm Fresh Large White Eggs - Dozen",
        "image": "/uploads/products/eggs-dozen.jpg",
        "price": 29.99,
        "stock": 75,
        "category": "Dairy & Eggs",
        "rating": 4.8,
        "num_reviews": 80,
        "reviews": [
            {"rating": 5, "comment": "Bright yolks and strong shells!"}
        ]
    },
    {
        "name": "Philadelphia Original Cream Cheese",
        "image": "/uploads/products/cream-cheese.png",
        "price": 24.99,
        "stock": 90,
        "category": "Dairy & Eggs",
        "rating": 4.7,
        "num_reviews": 95,
        "reviews": [
            {"rating": 5, "comment": "Classic for bagels and cheesecake!"}
        ]
    },
    {
        "name": "Organic Heavy Whipping Cream",
        "image": "/uploads/products/whipping-cream.png",
        "price": 21.50,
        "stock": 50,
        "category": "Dairy & Eggs",
        "rating": 4.8,
        "num_reviews": 45,
        "reviews": [
            {"rating": 5, "comment": "Whips perfectly every time!"}
        ]
    },
    {
        "name": "Fresh Mozzarella Ball",
        "image": "/uploads/products/mozzarella.png",
        "price": 18.99,
        "stock": 40,
        "category": "Dairy & Eggs",
        "rating": 4.9,
        "num_reviews": 30,
        "reviews": [
            {"rating": 5, "comment": "Perfect caprese salad essential!"}
        ]
    },
    {
        "name": "Yoplait Original Strawberry Yogurt - 8 Pack",
        "image": "/uploads/products/yogurt-pack.png",
        "price": 36.99,
        "stock": 80,
        "category": "Dairy & Eggs",
        "rating": 4.5,
        "num_reviews": 70,
        "reviews": [
            {"rating": 5, "comment": "Kid favorite lunchbox staple!"}
        ]
    },
    {
        "name": "Delicious white baked fresh bread and toast",
        "image": "/uploads/products/fresh-bread.png",
        "price": 20.00,
        "stock": 100,
        "category": "Bakery",
        "rating": 5.0,
        "num_reviews": 50,
        "reviews": [
            {"rating": 5, "comment": "Soft and buttery — amazing toasted!"}
        ]
    },
    {
        "name": "Pepperidge Farm Farmhouse Hearty White Bread",
        "image": "/uploads/products/pepperidge-bread.png",
        "price": 32.85,
        "stock": 60,
        "category": "Bakery",
        "rating": 4.0,
        "num_reviews": 40,
        "reviews": [
            {"rating": 4, "comment": "Classic taste, great for sandwiches."}
        ]
    },
    {
        "name": "Oroweat Country Buttermilk Bread",
        "image": "/uploads/products/oroweat-bread.png",
        "price": 32.85,
        "stock": 60,
        "category": "Bakery",
        "rating": 4.0,
        "num_reviews": 40,
        "reviews": [
            {"rating": 5, "comment": "Soft, buttery, and slightly sweet."}
        ]
    },
    {
        "name": "Thomas' Plain Bagels - 6 Pack",
        "image": "/uploads/products/bagels.png",
        "price": 26.99,
        "stock": 70,
        "category": "Bakery",
        "rating": 4.8,
        "num_reviews": 90,
        "reviews": [
            {"rating": 5, "comment": "Chewy, classic, and perfect with cream cheese!"}
        ]
    },
    {
        "name": "Freshly Baked Butter Croissants",
        "image": "/uploads/products/croissants.png",
        "price": 29.99,
        "stock": 40,
        "category": "Bakery",
        "rating": 4.9,
        "num_reviews": 60,
        "reviews": [
            {"rating": 5, "comment": "Flaky, buttery, and heavenly!"}
        ]
    },
    {
        "name": "Blueberry Muffins - 4 Pack",
        "image": "/uploads/products/muffins.png",
        "price": 24.50,
        "stock": 50,
        "category": "Bakery",
        "rating": 4.7,
        "num_reviews": 55,
        "reviews": [
            {"rating": 5, "comment": "Moist with bursting blueberries!"}
        ]
    },
    {
        "name": "Artisan Sourdough Loaf",
        "image": "/uploads/products/sourdough.png",
        "price": 34.99,
        "stock": 30,
        "category": "Bakery",
        "rating": 4.9,
        "num_reviews": 40,
        "reviews": [
            {"rating": 5, "comment": "Tangy crust, chewy inside — bakery quality!"}
        ]
    },
    {
        "name": "100% Whole Wheat Bread",
        "image": "/uploads/products/whole-wheat.png",
        "price": 22.99,
        "stock": 60,
        "category": "Bakery",
        "rating": 4.5,
        "num_reviews": 50,
        "reviews": [
            {"rating": 4, "comment": "Healthy, hearty, and great for sandwiches."}
        ]
    },
    {
        "name": "Pillsbury Cinnamon Rolls with Icing",
        "image": "/uploads/products/cinnamon-rolls.png",
        "price": 28.50,
        "stock": 80,
        "category": "Bakery",
        "rating": 4.8,
        "num_reviews": 100,
        "reviews": [
            {"rating": 5, "comment": "Warm, gooey, and perfect for breakfast!"}
        ]
    },
    {
        "name": "Assorted Glazed Donuts - 6 Pack",
        "image": "/uploads/products/donuts.png",
        "price": 19.99,
        "stock": 45,
        "category": "Bakery",
        "rating": 4.6,
        "num_reviews": 70,
        "reviews": [
            {"rating": 5, "comment": "Fresh and delicious — kids love them!"}
        ]
    },
    {
        "name": "Tandoori Plain Naan Bread - 8 Pack",
        "image": "/uploads/products/naan.png",
        "price": 31.50,
        "stock": 50,
        "category": "Bakery",
        "rating": 4.7,
        "num_reviews": 40,
        "reviews": [
            {"rating": 5, "comment": "Soft and perfect with curries!"}
        ]
    },
    {
        "name": "Fresh Whole Wheat Pita Bread - 10 Pack",
        "image": "/uploads/products/pita.png",
        "price": 25.99,
        "stock": 65,
        "category": "Bakery",
        "rating": 4.6,
        "num_reviews": 35,
        "reviews": [
            {"rating": 5, "comment": "Great for sandwiches and hummus!"}
        ]
    },
    {
        "name": "Canada Dry Ginger Ale - 2L Bottle",
        "image": "/uploads/products/canada-dry-ginger-ale.png",
        "price": 32.85,
        "stock": 90,
        "category": "Beverages",
        "rating": 4.4,
        "num_reviews": 55,
        "reviews": [
            {"rating": 5, "comment": "Classic ginger flavor!"}
        ]
    },
    {
        "name": "Canada Dry - 2L Bottle",
        "image": "/uploads/products/canada-dry.jpg",
        "price": 42.95,
        "stock": 80,
        "category": "Beverages",
        "rating": 3.9,
        "num_reviews": 55,
        "reviews": [
            {"rating": 5, "comment": "Hits the spot for me."}
        ]
    },
    {
        "name": "Nestle Original Coffee-Mate Coffee Creamer",
        "image": "/uploads/products/coffee-creamer.png",
        "price": 32.85,
        "stock": 100,
        "category": "Beverages",
        "rating": 4.0,
        "num_reviews": 40,
        "reviews": [
            {"rating": 4, "comment": "Smooths out my coffee perfectly."}
        ]
    },
    {
        "name": "Naturally Flavored Cinnamon Vanilla Light Roast Coffee",
        "image": "/uploads/products/cinnamon-coffee.png",
        "price": 32.85,
        "stock": 50,
        "category": "Beverages",
        "rating": 4.0,
        "num_reviews": 40,
        "reviews": [
            {"rating": 4, "comment": "Warm and comforting flavor."}
        ]
    },
    {
        "name": "Tropicana Pure Premium Orange Juice - 64oz",
        "image": "/uploads/products/orange-juice.png",
        "price": 38.99,
        "stock": 70,
        "category": "Beverages",
        "rating": 4.8,
        "num_reviews": 90,
        "reviews": [
            {"rating": 5, "comment": "Fresh-squeezed taste every time!"}
        ]
    },
    {
        "name": "Sprite Lemon-Lime Soda - 2L",
        "image": "/uploads/products/sprite.png",
        "price": 29.99,
        "stock": 100,
        "category": "Beverages",
        "rating": 4.5,
        "num_reviews": 80,
        "reviews": [
            {"rating": 5, "comment": "Crisp, clean, and refreshing!"}
        ]
    },
    {
        "name": "Coca-Cola Classic - 2L",
        "image": "/uploads/products/coca-cola.png",
        "price": 29.99,
        "stock": 120,
        "category": "Beverages",
        "rating": 4.9,
        "num_reviews": 200,
        "reviews": [
            {"rating": 5, "comment": "Timeless classic — ice cold perfection!"}
        ]
    },
    {
        "name": "Pepsi Cola - 2L",
        "image": "/uploads/products/pepsi.png",
        "price": 29.50,
        "stock": 110,
        "category": "Beverages",
        "rating": 4.6,
        "num_reviews": 180,
        "reviews": [
            {"rating": 5, "comment": "Bold and refreshing!"}
        ]
    },
    {
        "name": "Essentia Ionized Alkaline Water - 33.8oz",
        "image": "/uploads/products/bottled-water.png",
        "price": 24.99,
        "stock": 150,
        "category": "Beverages",
        "rating": 4.7,
        "num_reviews": 120,
        "reviews": [
            {"rating": 5, "comment": "Smooth, clean, and hydrating!"}
        ]
    },
    {
        "name": "Gatorade Thirst Quencher - Cool Blue - 32oz",
        "image": "/uploads/products/gatorade.png",
        "price": 21.99,
        "stock": 90,
        "category": "Beverages",
        "rating": 4.6,
        "num_reviews": 100,
        "reviews": [
            {"rating": 5, "comment": "Great for rehydration after workouts!"}
        ]
    },
    {
        "name": "Lipton Iced Tea - Lemon - 64oz",
        "image": "/uploads/products/iced-tea.png",
        "price": 32.50,
        "stock": 80,
        "category": "Beverages",
        "rating": 4.4,
        "num_reviews": 70,
        "reviews": [
            {"rating": 4, "comment": "Refreshing and not too sweet."}
        ]
    },
    {
        "name": "Almond Breeze Unsweetened Almond Milk",
        "image": "/uploads/products/almond-milk.png",
        "price": 26.99,
        "stock": 60,
        "category": "Beverages",
        "rating": 4.5,
        "num_reviews": 85,
        "reviews": [
            {"rating": 5, "comment": "Creamy and dairy-free!"}
        ]
    },
    {
        "name": "Gorton's Beer Battered Fish Fillets with soft paper",
        "image": "/uploads/products/gortons-fish.png",
        "price": 25.85,
        "stock": 40,
        "category": "Frozen",
        "rating": 4.2,
        "num_reviews": 35,
        "reviews": [
            {"rating": 4, "comment": "Crispy outside, tender inside!"}
        ]
    },
    {
        "name": "Organic Frozen Triple Berry Blend",
        "image": "/uploads/products/triple-berry.png",
        "price": 32.85,
        "stock": 70,
        "category": "Frozen",
        "rating": 4.0,
        "num_reviews": 40,
        "reviews": [
            {"rating": 5, "comment": "Great for smoothies!"}
        ]
    },
    {
        "name": "Ben & Jerry's Chocolate Fudge Brownie Ice Cream",
        "image": "/uploads/products/ice-cream.png",
        "price": 42.99,
        "stock": 50,
        "category": "Frozen",
        "rating": 4.9,
        "num_reviews": 150,
        "reviews": [
            {"rating": 5, "comment": "Rich, fudgy, and indulgent!"}
        ]
    },
    {
        "name": "DiGiorno Rising Crust Pepperoni Pizza",
        "image": "/uploads/products/frozen-pizza.png",
        "price": 36.50,
        "stock": 60,
        "category": "Frozen",
        "rating": 4.7,
        "num_reviews": 120,
        "reviews": [
            {"rating": 5, "comment": "Tastes like delivery — easy and tasty!"}
        ]
    },
    {
        "name": "Birds Eye Steamfresh Vegetable Medley",
        "image": "/uploads/products/vegetable-mix.png",
        "price": 18.99,
        "stock": 80,
        "category": "Frozen",
        "rating": 4.5,
        "num_reviews": 90,
        "reviews": [
            {"rating": 5, "comment": "Quick, healthy, and tasty!"}
        ]
    },
    {
        "name": "Tyson Fully Cooked Chicken Nuggets",
        "image": "/uploads/products/frozen-chicken-nuggets.png",
        "price": 28.50,
        "stock": 70,
        "category": "Frozen",
        "rating": 4.6,
        "num_reviews": 100,
        "reviews": [
            {"rating": 5, "comment": "Kid-approved and ready in minutes!"}
        ]
    },
    {
        "name": "Eggo Homestyle Waffles - 10 Pack",
        "image": "/uploads/products/frozen-waffles.png",
        "price": 22.99,
        "stock": 90,
        "category": "Frozen",
        "rating": 4.8,
        "num_reviews": 110,
        "reviews": [
            {"rating": 5, "comment": "Perfect crispy breakfast in minutes!"}
        ]
    },
    {
        "name": "Frozen Raw Jumbo Shrimp - 1lb",
        "image": "/uploads/products/frozen-shrimp.png",
        "price": 45.99,
        "stock": 40,
        "category": "Frozen",
        "rating": 4.7,
        "num_reviews": 60,
        "reviews": [
            {"rating": 5, "comment": "Restaurant quality at home!"}
        ]
    },
    {
        "name": "Amy's Bean & Cheese Burrito - 4 Pack",
        "image": "/uploads/products/frozen-burritos.png",
        "price": 34.50,
        "stock": 50,
        "category": "Frozen",
        "rating": 4.6,
        "num_reviews": 75,
        "reviews": [
            {"rating": 4, "comment": "Healthy, organic, and tasty!"}
        ]
    },
    {
        "name": "Organic Frozen Strawberries - 32oz",
        "image": "/uploads/products/frozen-berries.png",
        "price": 26.99,
        "stock": 65,
        "category": "Frozen",
        "rating": 4.8,
        "num_reviews": 80,
        "reviews": [
            {"rating": 5, "comment": "Perfect for smoothies and desserts!"}
        ]
    },
    {
        "name": "Ore-Ida Golden Crinkles French Fries",
        "image": "/uploads/products/frozen-french-fries.png",
        "price": 19.50,
        "stock": 100,
        "category": "Frozen",
        "rating": 4.5,
        "num_reviews": 95,
        "reviews": [
            {"rating": 5, "comment": "Crispy, salty, and delicious!"}
        ]
    },
    {
        "name": "Johnsonville Fully Cooked Sausage Links",
        "image": "/uploads/products/frozen-sausage-links.png",
        "price": 31.99,
        "stock": 55,
        "category": "Frozen",
        "rating": 4.7,
        "num_reviews": 70,
        "reviews": [
            {"rating": 5, "comment": "Hearty breakfast in minutes!"}
        ]
    }
]


def get_or_create_category(db: Session, name: str) -> Category:
    category = db.query(Category).filter(Category.name == name).first()
    if not category:
        category = Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category


def seed_products():
    db = SessionLocal()
    try:
        # Ensure all unique categories exist
        unique_categories = {item["category"] for item in products}
        category_map = {}
        for cat_name in unique_categories:
            category = get_or_create_category(db, cat_name)
            category_map[cat_name] = category.id

        # Insert products and reviews
        for item in products:
            product = Product(
                name=item["name"],
                image=item["image"],
                price=item["price"],
                stock=item["stock"],
                rating=item["rating"],
                num_reviews=item["num_reviews"],
                category_id=category_map[item["category"]]
            )
            db.add(product)
            db.flush()  # Get product.id without full commit

            # Add reviews
            for rev in item["reviews"]:
                review = Review(
                    product_id=product.id,
                    rating=rev["rating"],
                    comment=rev["comment"],
                    created_at=datetime.utcnow()
                )
                db.add(review)

        db.commit()
        print(f"✅ Successfully seeded {len(products)} products with reviews.")
    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    # Optional: Create tables if not exists
    Base.metadata.create_all(bind=engine)
    seed_products()
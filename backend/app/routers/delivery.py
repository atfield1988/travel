"""Delivery service integration with partner links"""
from fastapi import APIRouter, Query
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter(prefix="/api/delivery", tags=["delivery"])


class RestaurantInfo(BaseModel):
    id: str
    name: str
    category: str
    cuisine_type: str
    min_order: int
    delivery_fee: int
    delivery_time: str
    rating: float
    image_url: str
    shuttle_link: Optional[str] = None
    baemin_link: Optional[str] = None
    coupang_link: Optional[str] = None


@router.get("/restaurants")
async def get_restaurants(
    category: Optional[str] = Query(None, description="chicken, pizza, korean, western, chinese, japanese"),
    location: Optional[str] = Query("Seoul", description="Delivery location"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50)
):
    """Get restaurant list with delivery partner links"""
    
    # Sample restaurant data with partner links
    restaurants = [
        {
            "id": "kyochon-hongdae",
            "name": "Kyochon Chicken (교촌치킨)",
            "category": "chicken",
            "cuisine_type": "Korean Fried Chicken",
            "min_order": 17000,
            "delivery_fee": 3000,
            "delivery_time": "30-45 min",
            "rating": 4.7,
            "image_url": "https://via.placeholder.com/300x200?text=Kyochon",
            "shuttle_link": "https://www.shuttledelivery.co.kr/",
            "baemin_link": "baemin://restaurant/kyochon",
            "coupang_link": None,
            "popular_items": ["Honey Combo", "Red Combo", "Soy Garlic"],
            "payment_methods": ["card", "paypal", "ultimate_coin"]
        },
        {
            "id": "bbq-gangnam",
            "name": "BBQ Chicken",
            "category": "chicken",
            "cuisine_type": "Korean Fried Chicken",
            "min_order": 18000,
            "delivery_fee": 3000,
            "delivery_time": "35-50 min",
            "rating": 4.6,
            "image_url": "https://via.placeholder.com/300x200?text=BBQ",
            "shuttle_link": "https://www.shuttledelivery.co.kr/",
            "baemin_link": "baemin://restaurant/bbq",
            "coupang_link": "coupangeats://restaurant/bbq",
            "popular_items": ["Golden Olive", "Cheese Ball", "Hot Wing"],
            "payment_methods": ["card", "paypal", "ultimate_coin"]
        },
        {
            "id": "pizzahut-seoul",
            "name": "Pizza Hut Korea",
            "category": "pizza",
            "cuisine_type": "Western Pizza",
            "min_order": 15000,
            "delivery_fee": 2000,
            "delivery_time": "40-55 min",
            "rating": 4.4,
            "image_url": "https://via.placeholder.com/300x200?text=PizzaHut",
            "shuttle_link": "https://www.shuttledelivery.co.kr/",
            "baemin_link": "baemin://restaurant/pizzahut",
            "coupang_link": "coupangeats://restaurant/pizzahut",
            "popular_items": ["Super Supreme", "Cheese Lover", "Pepperoni"],
            "payment_methods": ["card", "paypal", "ultimate_coin"]
        },
        {
            "id": "dominos-myeongdong",
            "name": "Domino's Pizza",
            "category": "pizza",
            "cuisine_type": "Western Pizza",
            "min_order": 14000,
            "delivery_fee": 2000,
            "delivery_time": "30-45 min",
            "rating": 4.5,
            "image_url": "https://via.placeholder.com/300x200?text=Dominos",
            "shuttle_link": "https://www.shuttledelivery.co.kr/",
            "baemin_link": "baemin://restaurant/dominos",
            "coupang_link": None,
            "popular_items": ["New York Pizza", "Potato Pizza", "Bulgogi Pizza"],
            "payment_methods": ["card", "paypal", "ultimate_coin"]
        },
        {
            "id": "mcdonalds-gangnam",
            "name": "McDonald's",
            "category": "western",
            "cuisine_type": "Fast Food",
            "min_order": 10000,
            "delivery_fee": 2000,
            "delivery_time": "25-35 min",
            "rating": 4.3,
            "image_url": "https://via.placeholder.com/300x200?text=McDonalds",
            "shuttle_link": "https://www.shuttledelivery.co.kr/",
            "baemin_link": "baemin://restaurant/mcdonalds",
            "coupang_link": "coupangeats://restaurant/mcdonalds",
            "popular_items": ["Big Mac", "Bulgogi Burger", "McNuggets"],
            "payment_methods": ["card", "paypal", "ultimate_coin"]
        },
        {
            "id": "burgerking-hongdae",
            "name": "Burger King",
            "category": "western",
            "cuisine_type": "Fast Food",
            "min_order": 9000,
            "delivery_fee": 2000,
            "delivery_time": "30-40 min",
            "rating": 4.4,
            "image_url": "https://via.placeholder.com/300x200?text=BurgerKing",
            "shuttle_link": "https://www.shuttledelivery.co.kr/",
            "baemin_link": "baemin://restaurant/burgerking",
            "coupang_link": "coupangeats://restaurant/burgerking",
            "popular_items": ["Whopper", "Cheese Whopper", "Onion Rings"],
            "payment_methods": ["card", "paypal", "ultimate_coin"]
        }
    ]
    
    # Filter by category if provided
    if category:
        filtered = [r for r in restaurants if r["category"] == category]
    else:
        filtered = restaurants
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated = filtered[start:end]
    
    return {
        "total": len(filtered),
        "page": page,
        "limit": limit,
        "restaurants": paginated
    }


@router.get("/categories")
async def get_categories():
    """Get available restaurant categories"""
    return {
        "categories": [
            {
                "id": "chicken",
                "name": "Korean Fried Chicken",
                "icon": "🍗",
                "description": "Famous Korean Fried Chicken chains"
            },
            {
                "id": "pizza",
                "name": "Pizza & Italian",
                "icon": "🍕",
                "description": "Pizza and Italian cuisine"
            },
            {
                "id": "western",
                "name": "Western Fast Food",
                "icon": "🍔",
                "description": "McDonald's, Burger King, etc."
            },
            {
                "id": "korean",
                "name": "Korean Traditional",
                "icon": "🍜",
                "description": "Korean traditional dishes"
            },
            {
                "id": "chinese",
                "name": "Chinese Food",
                "icon": "🥡",
                "description": "Chinese restaurants"
            },
            {
                "id": "japanese",
                "name": "Japanese Food",
                "icon": "🍱",
                "description": "Sushi, Ramen, etc."
            }
        ]
    }


@router.get("/partners")
async def get_delivery_partners():
    """Get delivery partner information"""
    return {
        "partners": [
            {
                "id": "shuttle",
                "name": "Shuttle Delivery",
                "logo": "🚀",
                "description": "Foreign-friendly delivery service",
                "features": [
                    "No Korean phone number required",
                    "International cards accepted",
                    "English support",
                    "Hotel delivery"
                ],
                "website": "https://www.shuttledelivery.co.kr/",
                "app_ios": "https://apps.apple.com/app/shuttle-delivery",
                "app_android": "https://play.google.com/store/apps/details?id=com.shuttle"
            },
            {
                "id": "baemin",
                "name": "Baemin (배달의민족)",
                "logo": "🛵",
                "description": "Korea's #1 delivery app (57.6% market share)",
                "features": [
                    "Largest restaurant selection",
                    "Foreign phone numbers supported (2024+)",
                    "Korean language only"
                ],
                "website": "https://www.baemin.com/",
                "app_ios": "https://apps.apple.com/app/baemin",
                "app_android": "https://play.google.com/store/apps/details?id=com.sampleapp"
            },
            {
                "id": "coupang",
                "name": "Coupang Eats",
                "logo": "🚚",
                "description": "Fast delivery with English interface",
                "features": [
                    "35.3% market share",
                    "English interface available",
                    "Fast delivery"
                ],
                "website": "https://www.coupangeats.com/",
                "app_ios": "https://apps.apple.com/app/coupang-eats",
                "app_android": "https://play.google.com/store/apps/details?id=com.coupang.eats"
            }
        ]
    }


@router.get("/payment-methods")
async def get_payment_methods():
    """Get supported payment methods"""
    return {
        "methods": [
            {
                "id": "card",
                "name": "Credit/Debit Card",
                "supported_cards": ["Visa", "Mastercard", "Amex"],
                "fee": "0%",
                "description": "International cards accepted"
            },
            {
                "id": "paypal",
                "name": "PayPal",
                "fee": "3.4% + fixed fee",
                "description": "Secure PayPal payment"
            },
            {
                "id": "ultimate_coin",
                "name": "UltimateCoin",
                "icon": "🪙",
                "fee": "0%",
                "description": "Platform virtual currency with 5% bonus on purchase",
                "benefits": [
                    "5% bonus coins on purchase",
                    "No transaction fees",
                    "Instant payment",
                    "Exclusive discounts"
                ]
            }
        ]
    }


@router.get("/restaurant/{restaurant_id}")
async def get_restaurant_detail(restaurant_id: str):
    """Get detailed restaurant information"""
    
    # Sample detailed info
    return {
        "id": restaurant_id,
        "name": "Kyochon Chicken (교촌치킨)",
        "category": "chicken",
        "description": "Korea's premium fried chicken chain, famous for crispy coating and flavorful sauces",
        "rating": 4.7,
        "review_count": 2847,
        "min_order": 17000,
        "delivery_fee": 3000,
        "delivery_time": "30-45 min",
        "menu": [
            {
                "id": "honey-combo",
                "name": "Honey Combo",
                "name_kr": "허니콤보",
                "price": 19000,
                "description": "Half & Half: Honey and Original flavors",
                "image": "https://via.placeholder.com/200"
            },
            {
                "id": "red-combo",
                "name": "Red Combo",
                "name_kr": "레드콤보",
                "price": 19000,
                "description": "Spicy red sauce chicken",
                "image": "https://via.placeholder.com/200"
            },
            {
                "id": "soy-garlic",
                "name": "Soy Garlic",
                "name_kr": "간장마늘",
                "price": 18000,
                "description": "Classic soy garlic flavor",
                "image": "https://via.placeholder.com/200"
            }
        ],
        "delivery_info": {
            "shuttle_link": "https://www.shuttledelivery.co.kr/restaurant/kyochon",
            "baemin_link": "baemin://restaurant/kyochon",
            "coupang_link": None
        },
        "payment_methods": ["card", "paypal", "ultimate_coin"]
    }

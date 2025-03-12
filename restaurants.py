import json
from typing import Any, Dict, List, Optional


def get_restaurants_data() -> List[Dict[str, Any]]:
    with open("restaurants.json", "r") as f:
        return json.load(f)


def get_restaurant_by_id(restaurant_id: int) -> Optional[Dict[str, Any]]:
    restaurants = get_restaurants_data()
    for restaurant in restaurants:
        if restaurant["id"] == restaurant_id:
            return restaurant
    return None
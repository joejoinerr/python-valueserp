__all__ = ["SearchType"]

import enum


class SearchType(enum.Enum):
    """Types of searches that can be made using the API."""

    NEWS = "news"
    IMAGES = "images"
    VIDEOS = "videos"
    PLACES = "places"
    PLACE_DETAILS = "place_details"
    SHOPPING = "shopping"
    PRODUCT = "product"

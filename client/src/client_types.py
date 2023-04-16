"""all types for client"""

from typing import TypedDict


class DownloadItem(TypedDict):
    """describes a single download item"""

    youtube_id: str
    status: str


class DownloadPostType(TypedDict):
    """describes download post object"""

    data: list[DownloadItem]

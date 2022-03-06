import datetime
from dataclasses import dataclass


@dataclass
class DataBrosur:
    title: str
    date_create: str
    file_url: str
    size: str
    hits: str

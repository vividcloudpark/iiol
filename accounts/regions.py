import json
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def region_data():
    path = Path(__file__).resolve().parent.parent / "catalog" / "regions.json"
    return json.loads(path.read_text(encoding="utf-8"))


def region_choices():
    choices = []
    data = region_data()
    for province_code, province_name in data["big"].items():
        for region_code, region_name in data["small"].get(province_code, {}).items():
            choices.append((region_code, f"{province_name} {region_name}"))
    return choices


def valid_region(region_code):
    return any(code == region_code for code, _ in region_choices())


def region_name(region_code):
    return dict(region_choices()).get(region_code, "")

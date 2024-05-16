import base64

import requests
from apis.menu import schemas
from db.models import MenuItem
from fastapi import HTTPException
from urllib.parse import urlparse

def _image_url_to_base64(image_url: str):

    # Parse the URL to analyse it
    urlInfo = urlparse(image_url)
    if not urlInfo.scheme in ["http", "https"]:
        raise HTTPException(status_code=403, detail="Only HTTP and HTTPS URLs are allowed")
    
    # verify that the domain is whitelisted
    whitelist = ["localhost"] # and any other domains you want to allow (in real-world scenarios, this should be a configuation setting)
    if not urlInfo.netloc in whitelist:
        raise HTTPException(status_code=403, detail="Invalid image URL")

    # verify most common image formats by looking at the path part of the URL (to prevent urls like http://example.com/evil.php?image=evil.jpg)
    if not urlInfo.path.endswith((".jpg", ".jpeg", ".png", ".gif", "svg", "webp")):
        raise HTTPException(status_code=403, detail="Only images are allowed")

    response = requests.get(image_url)
    return base64.b64encode(response.content).decode()


def create_menu_item(
    db,
    menu_item: schemas.MenuItemCreate,
):
    menu_item_dict = menu_item.dict()
    image_url = menu_item_dict.pop("image_url", None)
    db_item = MenuItem(**menu_item_dict)

    if image_url:
        db_item.image_base64 = _image_url_to_base64(image_url)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def update_menu_item(
    db,
    item_id: int,
    menu_item: schemas.MenuItemCreate,
):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Menu Item not found")

    menu_item_dict = menu_item.dict()
    image_url = menu_item_dict.pop("image_url", None)

    for key, value in menu_item_dict.items():
        setattr(db_item, key, value)

    if image_url:
        db_item.image_base64 = _image_url_to_base64(image_url)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_menu_item(db, item_id: int):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="MenuItem not found")

    db.delete(db_item)
    db.commit()

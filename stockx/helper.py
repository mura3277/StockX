import base64
from PIL import Image
from io import BytesIO
from flask import session

from stockx.models import Shoe

"""
Converts a passed image file to a specified size, while also maintaining
the existing aspect ratio

(file, size) -> none
"""
def to_img64(file, size):
    #Create image and resize to smaller size if over the threshold
    try:
        image = Image.open(file)
    except IOError:
        print("Do not have permission to access image file")

    #Defualt to the original image size if argument is -1
    if size == -1:
        size = image.size[0]

    #Resize image if dimensions are bigger than the passed size
    if image.size[0] > size and image.size[1] > size:
        image.thumbnail((size, size), Image.ANTIALIAS)

    #Create memory buffer to store the image binary data
    buf = BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)

    #Convery bytes to base64
    img64 = base64.b64encode(buf.read())

    #Return bytes as base64 ascii
    return img64.decode("ascii")

"""
Check the session dictionary is valid by making sure the passed key exists
and if not, assign it with the passed object

(key, obj) -> none
"""
def check_session(key, obj):
    #Make sure a key value pair exists in session for the passed key
    if key not in session:
        session[key] = obj

"""
Update an item in the cart by querying the session dictionary by the items id.
if the item does not exist, add it, or increment its value if it does accordingly

(item, quantity, existing) -> none
"""
def update_cart(item, quantity, existing=False):
    #Check if our cart key is in the session
    check_session("cart", {})

    #Make sure quantity is passed as an integer
    quantity = int(quantity)

    #If exists, increment it, otherwise, assign it
    if str(item.id) in session["cart"] and not existing:
        session["cart"][str(item.id)] += 1
    else:
        #If the new quantity is less than 1, then remove it as we're effectively deleting the entry
        if quantity < 1:
            del session["cart"][str(item.id)]
        else:
            session["cart"][str(item.id)] = int(quantity)

    #Mark the session as modified so it updates for the user
    session.modified = True

"""
Builds a item list from the cart in the session by querying the database with the stored IDs
This way the objects that are returned are "live" and can be manipulated directly

(None) -> item{}
"""
def get_cart():
    check_session("cart", {})
    items = []
    #Build live list of database objects
    for id in session["cart"]:
        items.append({"item": Shoe.query.get_or_404(id), "quantity": session["cart"][id]})
    return items

"""
Clear the cart by assinging an emtpy object and marking it as modified to force flask to update

(None) -> None
"""
def purge_cart():
    session["cart"] = {}
    session.modified = True
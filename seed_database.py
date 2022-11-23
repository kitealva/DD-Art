import os
import json
import crud
import model
import server

os.system('dropdb art')
os.system('createdb art')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/art.json') as f:
    art_data = json.loads(f.read())
    
art_in_db = []
for art in art_data:
    art_name, image_path, description,price = (
        art['art_name'],
        art['image_path'],
        art['description'],
        art['price'],
    )
    
    db_art = crud.create_item(art_name, image_path, description, price)
    art_in_db.append(db_art)

model.db.session.add_all(art_in_db)
model.db.session.commit()
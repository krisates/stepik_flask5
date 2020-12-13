from app import db
from models import Category, Dish

# заполняем БД
for cat in ['Суши', 'Стритфуд', 'Пицца', 'Паста', 'Новинки']:
    c = Category(title=cat)
    db.session.add(c)

db.session.commit()

f = open("data.csv", "r")
for line in f:
    if line is not '':
        dish = line.split(';')
        if dish[0] is not '':
            d = Dish(
                id=dish[0],
                title=dish[1],
                price=dish[2],
                description=dish[3],
                picture=dish[4],
                category_id=dish[5]
            )
            db.session.add(d)
f.close()

db.session.commit()
# заполняем БД - окончание
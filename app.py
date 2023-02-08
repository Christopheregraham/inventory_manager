import datetime
import csv

from models import (Base, session, Product, engine)



def clean_date(date):
    try:
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        date_list = date.split('/')
        month = int(date_list[0])
        day = int(date_list[1])
        year = int(date_list[2])
        new_date = datetime.date(year, month, day)
    except ValueError:
        input('''
              \rThe price format is invalid
              \r Price should be dollar and cents
              \r Example: 29.99
              \r Please exclude currency symbols
              \r Hit Enter key to continue
              ''')
        return
    return new_date

def clean_price(price):
    try:
        cleaned = price.split('$')
        converted = float(cleaned[1])
        new_price = int(converted * 100)
    except ValueError:
        input('''
              \rThe price format is invalid
              \r Price should be dollar and cents
              \r Example: 29.99
              \r Please exclude currency symbols
              \r Hit Enter key to continue
              ''')
        return
    return new_price

def check_quant(quantity):
    try:
        new_quantity = int(quantity)
    except ValueError:
        input('''
              \rThe quantity format is invalid
              \r Quantity should be numeric 
              \r Example: 22
              \r Please exclude commas or symbols
              \r Hit Enter key to continue
              ''')
        return
    return new_quantity
        

def add_csv():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        header_skipped = False
        for row in data:
            if not header_skipped:
                header_skipped = True
                continue
            db_item = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
            if db_item == None:
                product_name = row[0]
                product_price = clean_price(row[1])
                product_quantity = check_quant(row[2])
                date_updated = clean_date(row[3])
                new_item = Product(product_name = product_name, product_price = product_price, product_quantity = product_quantity, date_updated = date_updated)
                session.add(new_item)
                session.commit()
                
def get_product_by_id(product_id):
    product = session.query(Product).filter(Product.product_id == product_id).one_or_none()
    if product:
        return (f'{product.product_id} | {product.product_name} | {product.product_price} | {product.product_quantity}| {product.date_updated}')
    else:
        return 'Product not found'
    
def view_item():
    try:
        item_id = input("Please enter the product's id number ")
        product = int(item_id)
        value = get_product_by_id(product)
    except ValueError:
        print('\r invalud id format, press enter to cont...')
        return
    return value

def menu():
    while True:
        print('''
            \nMain Menu
            \rtype v to View Product Details 
            \rtype a to Add Product
            \rtype b to Generate Backup.csv
            \rtype e to Exit''')
        choice = input('What would you like to do? ')
        if choice in ['a', 'v', 'b', 'e']:
            return choice
        else:
            input('''
              \rPlease choose one of the options above
              \rSelect an option v, a, b, or e
              \rPress enter to continue''')

def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice.lower() == 'v':
            view_item()
        elif choice.lower() == 'a':
            pass
        elif choice.lower() == 'b':
            pass
        elif choice.lower() == 'e':
            print('goodbye')
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    #app()
    view_item()
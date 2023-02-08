import datetime
import csv
import time


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
              \rThe Date format is invalid
              \rPlease input the date in MM/DD/YYYY
              \rExample: 10/26/2019
              \rPlease hit enter and try again
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
              \r Example: $29.99
              \r Please exclude non USD currency symbols
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
                
def get_product_by_id(productid):
    product = session.query(Product).filter(Product.product_id == productid).one_or_none()
    if product:
        price = price_format(product.product_price)
        print(f'{product.product_id} | Name: {product.product_name} | Price: {price} | Quantity: {product.product_quantity}| Last Updated: {product.date_updated}')
        time.sleep(2)
    else:
        print('Product not found')
        time.sleep(2)
    
def view_item():
    while True:
        try:
            item_id = input("Please enter the product's id number ")
            product = int(item_id)
            value = get_product_by_id(product)
            break
        except ValueError:
            print('\r invalid id format, press try again...')
            time.sleep(2)
    return value

def price_format(price):
    dollars = price // 100
    cents = price % 100
    return "${}.{:02}".format(dollars, cents)

def backup():
    products = []
    for product in session.query(Product):
        products.append(product)
    with open('backup.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        headers = ['product_name', 'product_price', 'product_quantity', 'date_updated']
        writer.writerow(headers)
        for item in products:
            price = price_format(item.product_price)
            row = [item.product_name, price, item.product_quantity, item.date_updated.strftime('%m/%d/%Y')]
            writer.writerow(row)
        print('Operation Successful')
        time.sleep(2)

def product_exists(product_name):
    existing_product = session.query(Product).filter_by(product_name=product_name).first()
    return existing_product is not None
    
def add_product():
    name = input('Name: ')
    quant_error = True
    while quant_error:
        quantity = input('Quantity: ')
        fixed_quant = check_quant(quantity)
        if type(fixed_quant) == int:
            quant_error = False
    date_fixed = datetime.datetime.now().date()
    price_error = True
    while price_error:
        price = input('Price (Ex. $9.99): ')
        fixed_price = clean_price(price)
        if type(fixed_price) == int:
            price_error = False
    if not product_exists(name)
        new_item = Product(product_name = name, product_price = fixed_price, product_quantity = fixed_quant, date_updated = date_fixed)
        session.add(new_item)
        session.commit()
        print(f'{name} was successfully added!')
        time.sleep(2)
    else:
        print(f'{name} already exists!')
        time.sleep(2)
     
    
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
            add_product()
        elif choice.lower() == 'b':
            backup()
        elif choice.lower() == 'e':
            print('Thanks for using Invetory Manager, Goodbye')
            app_running = False

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app()
   
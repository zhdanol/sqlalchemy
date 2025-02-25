import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from table import create_tables, Publisher, Shop, Book, Stock, Sale

SQLsystem = 'postgresql'
login = 'postgres'
password = '1589'
host = 'localhost'
port = '5432'
db_name = 'postgres'

DSN = f'{SQLsystem}://{login}:{password}@{host}:{port}/{db_name}'
engine = sq.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

def sell_list():
    search = input('Введите фамилию или идентификатор издателя: ')
    if search.isnumeric():
        results = session.query(Book.name, Shop.name, Sale.price, Sale.data_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id) \
            .join(Shop, Stock.id_shop == Shop.id) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.id == int(search)).all()
        for book, shop, price, date in results:
            print(f'{book:<40} | {shop:<10} | {price:<10} | {date}')
    else:
        results = session.query(Book.name, Shop.name, Sale.price, Sale.data_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id) \
            .join(Shop, Stock.id_shop == Shop.id) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.name.like(f'%{search}%')).all()
        for book, shop, price, date in results:
            print(f'{book:<40} | {shop:<10} | {price:<10} | {date}')
            
session.close()
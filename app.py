from models import (Base, session, Inventory, engine)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
import logging
import sqlite3
import random
import shutil
from pathlib import Path
from sqlite3 import Connection

logger = logging.getLogger(__name__)

DAIRY = 'dairy'
VEGETABLE = 'vegetable'
BAKERY = 'bakery'
FRUIT = 'fruit'
ITEMS = [
    {
        "title": "Brown eggs",
        "type": DAIRY,
        "price": 28.1,
    },
    {
        "title": "Sweet fresh stawberry",
        "type": FRUIT,
        "price": 29.45,
    },
    {
        "title": "Asparagus",
        "type": VEGETABLE,
        "price": 18.95,
    },
    {
        "title": "Green smoothie",
        "type": DAIRY,
        "price": 17.68,
    },
    {
        "title": "Raw legums",
        "type": VEGETABLE,
        "price": 17.11,
    },
    {
        "title": "Cake",
        "type": DAIRY,
        "price": 11.14,
    },
    {
        "title": "Pesto with basil",
        "type": VEGETABLE,
        "price": 18.19,
    },
    {
        "title": "Hazelnut",
        "type": VEGETABLE,
        "price": 27.35,
    },
    {
        "title": "Lemon",
        "type": FRUIT,
        "price": 15.79,
    },
    {
        "title": "Bread",
        "type": BAKERY,
        "price": 17.48,
    },
    {
        "title": "Legums",
        "type": VEGETABLE,
        "price": 14.77,
    },
    {
        "title": "Fresh tomato",
        "type": VEGETABLE,
        "price": 16.3,
    },
    {
        "title": "Oatmeal",
        "type": FRUIT,
        "price": 13.02,
    },
    {
        "title": "Green beans",
        "type": VEGETABLE,
        "price": 28.79,
    },
    {
        "title": "Portabello mushrooms",
        "type": BAKERY,
        "price": 20.31,
    },
    {
        "title": "Strawberry jelly",
        "type": FRUIT,
        "price": 14.18,
    },
    {
        "title": "Pear juice",
        "type": FRUIT,
        "price": 19.49,
    },
    {
        "title": "Fresh pears",
        "type": FRUIT,
        "price": 15.12,
    },
    {
        "title": "Salad",
        "type": VEGETABLE,
        "price": 16.76,
    },
    {
        "title": "Oranges",
        "type": FRUIT,
        "price": 21.48,
    },
    {
        "title": "Cremini Mushrooms",
        "type": DAIRY,
        "price": 22.7,
    },
    {
        "title": "Honey",
        "type": BAKERY,
        "price": 17.01,
    },
    {
        "title": "Cottage Cheese",
        "type": FRUIT,
        "price": 14.05,
    },
    {
        "title": "Mint",
        "type": FRUIT,
        "price": 26.21,
    },
    {
        "title": "Ricotta",
        "type": DAIRY,
        "price": 27.81,
    },
    {
        "title": "Granola",
        "type": DAIRY,
        "price": 29.97,
    },
    {
        "title": "Chia seeds",
        "type": FRUIT,
        "price": 25.26,
    },
    {
        "title": "Yogurt",
        "type": DAIRY,
        "price": 27.61,
    },
    {
        "title": "Sandwich",
        "type": VEGETABLE,
        "price": 22.48,
    },
    {
        "title": "Cherry",
        "type": FRUIT,
        "price": 14.35,
    },
]

#####################################################
################### DATABASES #######################
#####################################################
DB_DIR = f"{Path(__file__).parent.resolve()}/databases"


def connect(db: str):
    """create a database connection to a SQLite database"""
    Path(DB_DIR).mkdir(exist_ok=True)
    fq_path = Path(DB_DIR, f"{db}.sqlite3")
    if fq_path.exists():
        logger.debug(f"Connecting to DB @ {fq_path}")
    else:
        logger.debug(f"Creating DB @ {fq_path}")
    conn = sqlite3.connect(fq_path)
    return conn


def populate(conn: Connection):
    """Populates a db with some name"""
    table_name = "transactions"
    sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id integer PRIMARY KEY,
            items text NOT NULL,
            price number
        );
    """
    conn.execute(sql)

    # Generate 20 random samples and save as a transaction
    num_transactions = 20
    for _ in range(num_transactions):
        sample = random.sample(ITEMS, random.randint(2,6))
        items = ",".join([x["title"] for x in sample])
        price = sum([x["price"] for x in sample])
        insert = f"""
            INSERT INTO {table_name}(items,price)
            VALUES(?,?)
        """
        cur = conn.cursor()
        cur.execute(insert, (items, price))
        conn.commit()

def reset_db():
    # Reset the DBs every time
    shutil.rmtree(DB_DIR, ignore_errors=True)

    for i in range(1, 6):
        # Create 5 transaction dbs
        db_name = f"transactions_{i}"
        conn = connect(db_name)
        populate(conn)
        logger.debug(f"Populated {db_name} with random transaction data\n")

    logger.info("Databases Reset :)\nReady to being Apriori...")

if __name__ == "__main__":
    reset_db()

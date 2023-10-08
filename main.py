import db
from apriori import Apriori
import timeit

if __name__=="__main__":

    # Reset the DB
    db.reset_db()
    print("--------------------------------------")
    print("--------- DATABASE RESET -------------")
    print("--------------------------------------")

    start = timeit.default_timer()
    for i in range(1, 6):
        print("--------------------------------------")
        print(f"--------- APRIORI FOR DB {i}------------")
        print("--------------------------------------")
        db_name = f"transactions_{i}"

        cursor = db.connect(db_name).cursor()
        cursor.execute("SELECT * FROM transactions;")
        data = cursor.fetchall()

        # Convert to a dictionary
        transactions = []
        for row in data:
            transactions.append(
                {
                    "id": row[0],
                    "items": row[1].split(","),
                    "price": row[2],
                }
            )
        print("First transaction sample:", transactions[0])

        ap = Apriori(
            transactions=transactions,
            support=3,
            confidence=0.60
        )
        apriori_rules = ap.get_association_rules()

    apriori_time = timeit.default_timer()-start

    # Now brute force method
    start = timeit.default_timer()
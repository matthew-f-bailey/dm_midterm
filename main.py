import db
import argparse
import logging
from apriori import Apriori
from brute import Brute
import timeit
import json

logging.basicConfig(level=logging.INFO, format="%(name)s - %(message)s")
logger = logging.getLogger("main")

# Set low support since only 30 transactions
SUPPORT = None
CONFIDENCE = None

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--support',
        type=int,
        help='The support threshold used by Apriori Algo'
    )
    parser.add_argument(
        '--confidence',
        type=float,
        help='The confidence threshold used by Apriori Algo'
    )
    parser.add_argument(
        '--reset_db',
        type=bool,
        help='Turn on/off the resetting of the databases with new data.'
    )
    args = parser.parse_args()
    if args.confidence:
        CONFIDENCE = args.confidence
        logger.info(f"Using user supplied confidence of {CONFIDENCE}")
    if args.support:
        SUPPORT = args.support
        logger.info(f"Using user supplied support of {SUPPORT}")

    # Reset the DB
    if args.reset_db:
        db.reset_db()
        logger.info("--------------------------------------")
        logger.info("--------- DATABASE RESET -------------")
        logger.info("--------------------------------------")

    # Fetch all the data before timer
    db_data = [
        db.connect(f"transactions_{i}").cursor().execute("SELECT * FROM transactions;").fetchall()
        for i
        in range(1, 6)
    ]
    # Convert to a dict
    all_transactions = []
    for data in db_data:
        db_transactions = []
        for row in data:
            db_transactions.append(
                {
                    "id": row[0],
                    "items": row[1].split(","),
                    "price": row[2],
                }
            )
        all_transactions.append(db_transactions)

    # APRIORI LOOP
    start = timeit.default_timer()
    all_ap_rules = {}
    for i in range(5):
        transactions = all_transactions[i]
        logger.info("--------------------------------------")
        logger.info(f"--------- APRIORI FOR DB {i+1}------------")
        logger.info("--------------------------------------")
        logger.info(f"Printing only first transcation for brevity: {json.dumps(transactions[0], indent=4)}")

        ap = Apriori(
            transactions=transactions,
            support=SUPPORT,
            confidence=CONFIDENCE
        )
        apriori_rules = ap.get_association_rules()
        all_ap_rules[f"database_{i+1}"] = apriori_rules


    apriori_time = timeit.default_timer()-start
    logger.info(f"Apriori Algo Time: {apriori_time}")


    # BRUTE LOOP
    start = timeit.default_timer()
    all_brute_rules = {}
    for i in range(5):
        transactions = all_transactions[i]
        logger.info("--------------------------------------")
        logger.info(f"--------- BRUTE FOR DB {i+1}------------")
        logger.info("--------------------------------------")
        logger.info(f"Printing only first transcation for brevity: {json.dumps(transactions[0], indent=4)}")

        brute = Brute(
            transactions=transactions,
            support=SUPPORT,
            confidence=CONFIDENCE
        )
        brute_rules = brute.get_association_rules()
        all_brute_rules[f"database_{i+1}"] = brute_rules


    # Sort both rules

    brute_time = timeit.default_timer()-start
    logger.info(f"Brute Force Time: {brute_time}")

    # Sort rules to make sure they are the same
    for i in range(1, 6):
        db_ap_rules = {x["rule"] for x in all_ap_rules[f"database_{i}"]}
        db_brute_rules = {x["rule"] for x in all_brute_rules[f"database_{i}"]}

        # Quick check to bail out if not same
        if db_brute_rules!=db_ap_rules:
            raise AssertionError("Rules not of same length...")
        else:
            logger.info(f"Rules exactly Matched for DB {i}")

        
    logger.info(f"Over entire execution Apriori was {round((-1)*(apriori_time-brute_time),5)} seconds faster")


# How to run the repo/midterm project

0. Create env and install deps (Or not, no packages used. Pure builtins)
1. Populate databases (Can turn this on/off using arg of ``--reset_db true/false``)
2. Run Apriori (Set arg of ``--support [int] as well as --confidence [float]``)
3. Run Brute Force (Set arg of ``--support [int] as well as --confidence [float]``)
4. Compare results (In notebook script, some cells will output results to a file)

Running the main.py file will do all of this for you.

# Requirements:
1. Values Read in from db
    - Using sqlite3 databases and resetting them every run. Populating the dbs with random transactions prior to starting any processing, then reading in from them via a SELECT * query.
    The cli version and notebook also offer ways to avoid resetting the db as well and offer it as a convenience to turn on/off.

2. Support & Confidence are user defined at runtime.
    - Both this notebook and script version take user input in the form of the ``input`` function or using ``argparse`` respectively. No hardcoding.

3. Brute force stops early when no frequent itemsets found.
    - See lines 57-59 in ``brute.py`` for the cli version or the cell below in the ``Brute.get_association_rules()`` function for reference of this. Output will also confirm no more supersets/itemsets are calculated once none are found.

4. Brute force and Apriori both calculate same rules.
    - Checks at the end compare if output rules match exactly. Errors out if not

5. Timing is calculated.
    - Time is shown for both the implementations as well as the difference where apriori is faster in almost every iteration.

# ToC
- databases/
    - This directory stores the sqllite databases. Creating DBs manually is supported assuming they adhear to the following schema. 
        - id: primary_key -- Auto Incremented
        - items: varchar -- Comma delimited list of items (eg. eggs,milk,butter...)
        - price: number -- Cost of entire transaction

- rules/
    - This directory store the rules when run via notebook. These will be the output of all databases across both implementations. While both the ``database_n_rules_[brute/apriori].json`` will be identical, they will still be created for completeness. (Only generated when run via notebook)

- tests/
    - Just a couple of sanity checks as I was developing, can most likely ignore.

- apriori.py
    - The Apriori association rule implementation.
    
- brute.py
    - The Brute Force association rule implementation.
        
- db.py
    - All code related to the database resetting, reading and writing to them

- main.py
    - The main entrypoint that takes in arguments, potentially resets db, and runs both algos with timing and comparison.

- submission.ipynb
    - Interactive Notebook which will serve to show some outputs as well as export to a pdf for the submission. Contains the source code, execution as well as some notes.
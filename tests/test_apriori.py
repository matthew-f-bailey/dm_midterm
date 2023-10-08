from unittest import TestCase

from apriori import Apriori, SPLIT_CHAR


class TestApriori(TestCase):

    def test_sanity_check1(self):
        """ do the thing """
        transactions = [
            {
                "id": "1",
                "items": ["hot_dog", "buns", "ketchup"],
                "price": 1.00
            },
            {
                "id": "2",
                "items": ["hot_dog", "buns"],
                "price": 1.00
            },
            {
                "id": "3",
                "items": ["hot_dog", "coke", "chips"],
                "price": 1.00
            },
            {
                "id": "4",
                "items": ["chips", "coke"],
                "price": 1.00
            },
            {
                "id": "5",
                "items": ["chips", "ketchup"],
                "price": 1.00
            },
            {
                "id": "6",
                "items": ["hot_dog", "coke", "chips"],
                "price": 1.00
            },
        ]
        apriori = Apriori(
            transactions=transactions,
            support=2,
            confidence=0.60
        )
        rules = apriori.get_association_rules()
        self.assertEqual(apriori.initial_counts["hot_dog"], 4)
        self.assertEqual(apriori.initial_counts["buns"], 2)
        self.assertEqual(apriori.initial_counts["ketchup"], 2)
        self.assertEqual(apriori.initial_counts["coke"], 3)
        self.assertEqual(apriori.initial_counts["chips"], 4)
        freq_set = apriori.freq_itemsets.keys()
        self.assertEqual(len(freq_set), 1)
        self.assertEqual(
            sorted(list(freq_set)[0].split(SPLIT_CHAR)),
            ["chips", "coke", "hot_dog"]
        )

    def test_sanity_check2(self):
        """ do the thing """
        transactions = [
            {
                "id": "1",
                "items": ["hot_dog", "buns", "ketchup"],
                "price": 1.00
            },
            {
                "id": "2",
                "items": ["hot_dog", "buns"],
                "price": 1.00
            },
            {
                "id": "3",
                "items": ["hot_dog", "coke", "chips"],
                "price": 1.00
            },
            {
                "id": "4",
                "items": ["chips", "coke"],
                "price": 1.00
            },
            {
                "id": "5",
                "items": ["chips", "ketchup"],
                "price": 1.00
            },
            {
                "id": "6",
                "items": ["hot_dog", "coke", "chips"],
                "price": 1.00
            },
        ]
        apriori = Apriori(
            transactions=transactions,
            support=3,
            confidence=0.60
        )
        rules = apriori.get_association_rules()
        self.assertEqual(apriori.initial_counts["hot_dog"], 4)
        self.assertEqual(apriori.initial_counts["buns"], 2)
        self.assertEqual(apriori.initial_counts["ketchup"], 2)
        self.assertEqual(apriori.initial_counts["coke"], 3)
        self.assertEqual(apriori.initial_counts["chips"], 4)
        freq_set = apriori.freq_itemsets.keys()
        self.assertEqual(len(freq_set), 1)
        self.assertEqual(
            sorted(list(freq_set)[0].split(SPLIT_CHAR)),
            ["chips", "coke"]
        )

from itertools import combinations
from typing import Union
import json

# Quick and dirty hashing
SPLIT_CHAR = "|"

class Apriori:

    def __init__(
        self,
        transactions: list,
        support: Union[int, float],
        confidence: float
    ) -> None:

        # If % support given, calculate it, else use int
        if isinstance(support, float):
            support = len(transactions) * support
        self.min_support_count = support
        self.confidence = confidence

        # Hold initial transactions
        self.transactions = [set(x["items"]) for x in transactions]
        # [["apples", "oranges"], ["oranges", ..., "kiwi"], [...], ...]

        # Get initial counts of all items (first step)
        initial_counts = {}
        for transaction in self.transactions:
            for item in transaction:
                if item in initial_counts:
                    initial_counts[item] += 1
                else:
                    initial_counts[item] = 1
        self.initial_counts = initial_counts

        # Store the freq itemsets
        self.freq_itemsets = None

    def calc_support(self, itemset):
        count = 0
        itemset = set(itemset)
        for transaction in self.transactions:
            # If this itemset is not in a transaction, skip
            if not itemset.issubset(transaction):
                continue
            count+=1
        return count

    def get_association_rules(self):

        self.freq_itemsets = self.get_freq_itemsets()
        items = [list(x.split(SPLIT_CHAR)) for x in self.freq_itemsets.keys()]

        # Calculate all subsets for each itemset
        all_subsets = {}
        for itemset in items:
            subsets = []
            for i in range(len(itemset)-1, 0, -1):
                combs = list(combinations(itemset, i))
                subsets.extend(combs)
            all_subsets[SPLIT_CHAR.join(itemset)] = {
                "subsets": subsets,
                "items": itemset,
            }

        print("\nSubsets of freq itemsets:", all_subsets)
        # Apply rules and use the confidence
        rules = []
        for itemset_string, itemset_vals in all_subsets.items():
            subs = itemset_vals["subsets"]
            ind_items = set(itemset_vals["items"])
            for sub in subs:
                sub = set(sub)
                left = ind_items.difference(sub)
                rule = f"[{'^'.join(sub)}]=>[{'^'.join(left)}]"
                conf = self.calc_support(ind_items)/self.calc_support(sub)
                if conf>=self.confidence:
                    rules.append({
                        "rule": rule,
                        "items_bought": list(sub),
                        "implies": list(left),
                        "confidence": f"{round(conf*100,2)}%"
                    })
        print("\nRules Found:\n", json.dumps(rules, indent=4))

    def get_freq_itemsets(self):

        # Prune initial counts
        pruned = {
            item: count
            for item, count
            in self.initial_counts.items()
            if count >= self.min_support_count
        }

        # This will hold most recent pruned and only update if more itemsets found
        last_pruned = pruned
        k = 2
        while True:
            last_pruned = pruned
            pruned = self._step(k=k, pruned=pruned)
            k+=1
            if not pruned:
                break
        print("\nFound frequent itemsets:", last_pruned)
        return last_pruned

    def _step(self, k: int, pruned: dict):
        """The iteritive step of joining and pruning where k is the k-th itemset

        Args:
            k (int): Value of k-itemset
        """
        print("\nPruned", pruned)
        # Form new itemset from pruned
        items_left = []
        for items in pruned.keys():
            items_left.extend(items.split(SPLIT_CHAR))
        items_left = set(items_left)

        # Form k-itemset
        combs = [set(x) for x  in combinations(items_left, k)]

        # Count if itemsets are in transactions
        counts = {}
        for itemset in combs:
            itemset_name = SPLIT_CHAR.join(itemset)
            for transaction in self.transactions:
                # If this itemset is not in a transaction, skip
                if not itemset.issubset(transaction):
                    continue

                # Add the support count if found
                if itemset_name in counts:
                    counts[itemset_name] += 1
                else:
                    counts[itemset_name] = 1

        # Remove those under support count
        pruned = {
            itemset: count
            for itemset, count
            in counts.items()
            if count >= self.min_support_count
        }
        return pruned
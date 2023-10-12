import logging
import json
from typing import Union
from db import ITEMS
from itertools import combinations

logger = logging.getLogger(__name__)

class Brute:

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

        # Largest possible itemset
        self.max_k = max([len(x) for x in self.transactions])

                # Get initial counts of all items (first step)
        initial_counts = {}
        for transaction in self.transactions:
            for item in transaction:
                if item in initial_counts:
                    initial_counts[item] += 1
                else:
                    initial_counts[item] = 1
        self.initial_counts = initial_counts

    def get_association_rules(self):
        """ Start by finid """

        all_items = [x["title"] for x in ITEMS]
        logger.debug(f"Len of items: {len(all_items)}")
        # Start by generating all possible itemsets
        all_frequent = []
        for k in range(2, self.max_k+1):
            # Get all itemsets for k
            k_combs = {x for x in combinations(all_items, k)}
            
            # Sanity check
            if k==2:
                assert len(k_combs)==435

            frequent = [itemset for itemset in k_combs if self.is_frequent(itemset)]
            logger.info(f"Found {len(frequent)} of {len(k_combs)} {k}-itemsets total combinations to be frequent")
            if len(frequent)==0:
                logger.info(f"No frequent {k}-itemsets found, not going higher")
                break

            all_frequent.extend(list(frequent))
        
        # Caclulate confidence of each potential rule
        all_subsets = {}
        for itemset in all_frequent:
            subsets = []
            for i in range(len(itemset)-1, 0, -1):
                subsets.extend(list(combinations(itemset, i)))
            all_subsets["|".join(itemset)] = {
                "subsets": subsets,
                "items": itemset,
            }

        logger.debug(f"\nSubsets of freq itemsets: {all_subsets}")
        rules = []
        for itemset_string, itemset_vals in all_subsets.items():
            subs = itemset_vals["subsets"]
            ind_items = set(itemset_vals["items"])
            for sub in subs:
                sub = set(sub)
                left = ind_items.difference(sub)
                rule = f"[{'^'.join(sorted(sub))}]=>[{'^'.join(sorted(left))}]"
                conf = self.calc_support(ind_items)/self.calc_support(sub)
                if conf>=self.confidence:
                    rules.append({
                        "rule": rule,
                        "items_bought": list(sub),
                        "implies": list(left),
                        "confidence": f"{round(conf*100,2)}%"
                    })
        logger.info(f"Number of Rules Found: {len(rules)}")
        
        return rules

    def is_frequent(self, itemset: set) -> bool:
        if self.calc_support(itemset)>=self.min_support_count:
            return True
        return False
    
    def calc_support(self, itemset: set):
        count = 0
        itemset = set(itemset)
        for transaction in self.transactions:
            # If this itemset is not in a transaction, skip
            if not itemset.issubset(transaction):
                continue
            count+=1
        return count

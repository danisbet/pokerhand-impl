import itertools

class pokercard():
    def __init__(self, val, suit):
        self.value = val
        self.suit = suit
    
    def __str__(self):
        strval = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
        if self.value > 10:
            value = strval[self.value]
        else:
            value = self.value
        return '{} of {}'.format(value, self.suit)

    def __lt__(self, other):
        # Always assumes ace high

        # Self's ace is larger than other's ace
        if self.value == 1 and other.value != 1:
            return False
        # Other's ace is large than our non-ace
        if self.value != 1 and other.value == 1:
            return True

        # If neither's an ace, or both's an ace then normal counting rules apply
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        # Always assumes ace high

        # Self's ace is larger than other's ace
        if self.value == 1 and other.value != 1:
            return True
        # Other's ace is large than our non-ace
        if self.value != 1 and other.value == 1:
            return False

        # If neither's an ace, or both's an ace then normal counting rules apply
        return self.value > other.value

class pokerhand():
    def __init__(self):
        self.cards = []
        self.possible_hands = []
        self.best_hand = []

    def deal(self, cards = []):
        self.cards += cards

        if len(self.cards) > 5:
            raise Exception('Error, this poker hand has more than should be allowed')

    def get_best_hand(self):
        self.best_hand = self.get_best_hand_helper(self.cards)
        return self.best_hand

    def get_best_hand_helper(self, cards = None):
        if len(cards) <= 0:
            return []

        if royal_flush.is_valid(cards):
            return [royal_flush()]
        if straight_flush.is_valid(cards):
            return [straight_flush()]
        
        if len(cards) == 5:
            for combo in itertools.combinations(cards, 4):
                if four_of_a_kind.is_valid(combo):
                    return [four_of_a_kind()]

        if flush.is_valid(cards):
            return [flush()]
        if straight.is_valid(cards):
            return [straight()]
        if full_house.is_valid(cards):
            return [full_house()]

        for combo in itertools.combinations(cards, 3):
            if three_of_a_kind.is_valid(combo):
                return [three_of_a_kind()]

        if pair.is_valid(cards):
            return [pair()]

        if len(cards) == 2:
            return []

        pairs = []
        for combo in itertools.combinations(cards, 2):
            if pair.is_valid(combo):
                pairs.append(pair())
        return pairs

class scoredhand():
    @classmethod
    def are_all_the_same(cls, cards):
        card_value = cards[0].value
        for card in cards:
            if card.value != card_value:
                return False
        return True

class pair(scoredhand):
    @classmethod
    def is_valid(cls,cards):
        if len(cards) != 2:
            return False
        return scoredhand.are_all_the_same(cards)

class three_of_a_kind(scoredhand):
    @classmethod
    def is_valid(cls,cards):
        if len(cards) != 3:
            return False
        return scoredhand.are_all_the_same(cards)

class full_house(pair, three_of_a_kind):
    @classmethod
    def is_valid(cls,cards):
        if len(cards) != 5:
            return False

        # Get every possible set of 2 cards and 3 cards
        for perm in itertools.permutations(cards):
            if pair.is_valid(perm[0:2]) and three_of_a_kind.is_valid(perm[2:]):
                return True
        return False


class four_of_a_kind(scoredhand):
    @classmethod
    def is_valid(cls,cards):
        if len(cards) != 4:
            return False
        return scoredhand.are_all_the_same(cards)

class flush(scoredhand):
    @classmethod
    def is_valid(cls,cards):
        if len(cards) != 5:
            return False

        card_suit = cards[0].suit
        for card in cards:
            if card.suit != card_suit:
                return False

        return True

    
class straight(scoredhand):
    @classmethod
    def is_valid(cls,cards):
        if len(cards) != 5:
            return False

        # We can sort because we have 
        # TODO: Test to make sure we're not changing the order of cards outside of this
        _cards = sorted(cards)

        has_wraparound = False
        for card in _cards:
            if card.value == 14:
                has_wraparound = True
        
        if not has_wraparound:
            # Base case: no wraparounds
            prev_val = _cards[0].value
            for card in _cards[1:]:
                if card.value != prev_val + 1:
                    prev_val = card.value
                    return False

        #TODO: Handle Wraparounds




class straight_flush(flush, straight):
    @classmethod
    def is_valid(cls,cards):
        if not straight.is_valid(cards):
            return False
        if not flush.is_valid(cards):
            return False

        return True

class royal_flush(straight_flush):
    @classmethod
    def is_valid(cls,cards):
        if not straight_flush.is_valid(cards):
            return False

        ace_found = False
        ten_found = False
        for card in cards:
            if card.value == 1:
                ace_found = True
            if card.value == 10:
                ten_found = True
        if ace_found and ten_found:
            return True

        return False

import random
class deck():
    def __init__(self):
        self.cards = []
        self.makedeck()
        self.shuffle()

    def makedeck(self):
        for i in range (1, 14):
            for suit in ['clubs', 'hearts', 'diamonds', 'spades']:
                card = pokercard(i, suit)
                self.cards.append(card)
    
    def drawcard(self):
        card_drawn = self.cards[0]
        self.cards = self.cards[1:]

        return card_drawn


    def shuffle(self):
        random.shuffle(self.cards)


if __name__ == "__main__":
    d = deck()
    h = pokerhand()

    for i in range(5):
        c = d.drawcard()
        h.deal([c])

    for c in h.cards:
        print(c)

    print( h.get_best_hand() )

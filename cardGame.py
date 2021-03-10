import random


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def show(self):
        print(f"{self.value} of {self.suit}")


class Deck:
    def __init__(self):
        self.cards = []
        f = open("deck_file")
        for line in f:
            l_split = line.split(": ")
            suit = l_split[0]
            c_split = l_split[1].split(",")
            for val in c_split:
                val = val.strip('\n')
                self.cards.append(Card(suit, int(val)))
        f.close()

    def shuffle(self):
        # shuffle cards
        for i in range(len(self.cards)-1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def deal(self, num):
        deal_cards = []
        for i in range(num):
            deal_cards.append(self.cards.pop())
        return deal_cards

    def show(self):
        for card in self.cards:
            print(f"{card.value}:{card.suit[0]}")


class Hand:
    def __init__(self, cards):
        self.cards = cards

    def add(self, cards):
        for card in cards:
            self.cards.append(card)

    def shuffle(self):
        # shuffle cards
        for i in range(len(self.cards)-1, 0, -1):
            r = random.randint(0, i)
            self.cards[i], self.cards[r] = self.cards[r], self.cards[i]

    def to_string(self):
        string = "["
        for card in self.cards:
            string += f"{card.value}:{card.suit[0]}, "
        return string.strip(", ") + "]"


class War:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.p1 = Hand(self.deck.deal(26))
        self.p2 = Hand(self.deck.deal(26))
        self.p1_won_cards = Hand([])
        self.p2_won_cards = Hand([])
        self.winner = None
        self.play_game()

    def check_win(self):
        if len(self.p1.cards) == 0 and len(self.p1_won_cards.cards) == 0:
            self.winner = "player 2"
            self.p2.add(self.p2_won_cards.cards)
            self.p2_won_cards = Hand([])
            self.p2.shuffle()
        elif len(self.p2.cards) == 0 and len(self.p2_won_cards.cards) == 0:
            self.winner = "Player 1"
            self.p1.add(self.p1_won_cards.cards)
            self.p1_won_cards = Hand([])
            self.p1.shuffle()

    def compare(self, card1, card2):
        if card1.value > card2.value:
            return 1
        elif card2.value > card1.value:
            return 2
        else:
            return 0

    def play_round(self):
        tie = True
        pool = []
        while tie:
            if len(self.p1.cards) < 1:
                print("shuffling p1")
                self.p1.add(self.p1_won_cards.cards)
                self.p1_won_cards = Hand([])
                self.p1.shuffle()
            if len(self.p2.cards) < 1:
                print("shuffling p2")
                self.p2.add(self.p2_won_cards.cards)
                self.p2_won_cards = Hand([])
                self.p2.shuffle()
            p1_card = self.p1.cards.pop()
            p2_card = self.p2.cards.pop()

            print(f"{p1_card.value} of {p1_card.suit[0]} vs {p2_card.value} of {p2_card.suit[0]}")

            compare = self.compare(p1_card, p2_card)
            if compare == 1:
                # player 1 won
                print("Player1 wins round")
                tie = False
                self.p1_won_cards.cards.append(p1_card)
                self.p1_won_cards.cards.append(p2_card)
                for i in pool:
                    print(i.value, " ", i.suit)
                    self.p1_won_cards.cards.append(i)
            elif compare == 2:
                # player 2 won
                print("Player2 wins round")
                tie = False
                self.p2_won_cards.cards.append(p1_card)
                self.p2_won_cards.cards.append(p2_card)
                for i in pool:
                    print(i.value, " ", i.suit)
                    self.p2_won_cards.cards.append(i)
            else:
                # tie
                print("Tie!")
                tie = True
                flip_num = 3
                pool.append(p1_card)
                pool.append(p2_card)
                if len(self.p1.cards) < 4:
                    print("shuffling p1")
                    self.p1.add(self.p1_won_cards.cards)
                    self.p1_won_cards = Hand([])
                    self.p1.shuffle()
                if len(self.p2.cards) < 4:
                    print("shuffling p2")
                    self.p2.add(self.p2_won_cards.cards)
                    self.p2_won_cards = Hand([])
                    self.p2.shuffle()
                if len(self.p1.cards) < 4 or len(self.p2.cards) < 4:
                    flip_num = min(len(self.p1.cards), len(self.p2.cards)) - 1
                if flip_num < 0:
                    tie = False
                    random_winner = random.randint(1, 2)
                    print("Tie decided by random draw-breaker: player", random_winner, "won")
                    if random_winner == 1:
                        for i in pool:
                            print(i.value, " ", i.suit)
                            self.p1_won_cards.cards.append(i)
                    else:
                        for i in pool:
                            print(i.value, " ", i.suit)
                            self.p2_won_cards.cards.append(i)

                for i in range(flip_num):
                    pool.append(self.p1.cards.pop())
                    pool.append(self.p2.cards.pop())

        print("player1 cards: ", self.p1.to_string(), "\tplayer 1's won cards: ", self.p1_won_cards.to_string())
        print("player2 cards: ", self.p2.to_string(), "\tplayer 2's, won cards: ", self.p2_won_cards.to_string())

    def play_game(self):
        num = 0
        cap = 100
        while self.winner is None and cap > num:
            self.play_round()
            self.check_win()
            num += 1
        print("The winner is ", self.winner)
        print(f"length: {len(self.p1.cards)} p1 cards: {self.p1.to_string()}")
        print(f"length: {len(self.p2.cards)} p2 cards: {self.p2.to_string()}")


if __name__ == "__main__":
    for game_num in range(100):
        print("\nStarting game number: ", game_num, "\n")
        game = War()


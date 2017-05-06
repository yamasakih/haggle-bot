# -*- coding: utf-8 -*-
from random import shuffle

all_suit = {'s': ' :spades: ',
            'h': ' :heart: ',
            'c': ' :clubs: ',
            'd': ' :diamonds: ',
            'j': '',
            }

"""
all_suit = {'spades': ' :spades: ',
            'heart': ' :heart: ',
            'clubs': ' :clubs: ',
            'diamonds': ' :diamonds: ',
            'joker': '',
            }
"""

all_numbers = {1: '1 ',
               2: '2 ',
               3: '3 ',
               4: '4 ',
               5: '5 ',
               6: '6 ',
               7: '7 ',
               8: '8 ',
               9: '9 ',
               10: '10 ',
               11: 'J ',
               12: 'Q ',
               13: 'K ',
               0: ' :black_joker: '
               #-1: ' :black_joker: ',
               }

"""
all_numbers = {1: ' :one: ',
               2: ' :two: ',
               3: ' :three: ',
               4: ' :four: ',
               5: ' :five: ',
               6: ' :six: ',
               7: ' :seven: ',
               8: ' :eight: ',
               9: ' :nine: ',
               10: ' :keycap_ten: ',
               11: ' :one: :one: ',
               12: ' :one: :two: ',
               13: ' :one: :three: ',
               #-1: ' :black_joker: ',
               }
"""


class Item:
    pass


class Rule(Item):

    def __init__(self, number, text):
        self.number = number
        self.text = text

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '```ルール%s: %s```' % (self.number, self.text, )

    def __eq__(self, other):
        if isinstance(other, Rule):
            return self.number == other.number and self.text == other.text
        else:
            return False

    def is_match_by_number(self, number):
        return self.number == number

    def __lt__(self, other):
        if isinstance(other, Rule):
            return self.number < other.number
        else:
            return False


class Rules:

    def __init__(self, rules):
        self._rules = rules

    def __str__(self):
        return ' '.join([str(rule) for rule in self._rules])

    def search(self, other):
        for rule in self._rules:
            if rule == other:
                return rule
        else:
            return None

    def search_by_number(self, number):
        for rule in self._rules:
            if rule.is_match_by_number(number):
                return rule
        else:
            return None

    def add(self, rule):
        self._rules.append(rule)

    def remove(self, rule):
        self._rules.remove(rule)

    def get_rules(self):
        return self._rules

    def sort(self):
        self._rules.sort()


class Token(Item):

    def __eq__(self, other):
        pass


class Card(Token):

    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def __str__(self):
        return ''.join([all_suit[self.suit], all_numbers[self.number]])

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.suit == other.suit and self.number == other.number
        else:
            return False

    def is_equal(self, **kwargs):
        suit = kwargs.get('suit')
        number = kwargs.get('number')
        return self.suit == all_suit[suit] and self.number == all_numbers[number]

    def __lt__(self, other):
        if isinstance(other, Card):
            suit_lt_dic = {'s': 0,
                           'h': 1,
                           'c': 2,
                           'd': 3,}
            if self.suit == other.suit:
                return self.number < other.number
            else:
                return suit_lt_dic[self.suit] < suit_lt_dic[self.suit]
        else:
            return False


class Hand:

    def __init__(self, tokens):
        self._tokens = tokens

    def __str__(self):
        return '  '.join([str(token) for token in self._tokens])

    def search(self, other):
        for token in self._tokens:
            if token == other:
                return token
        else:
            return None

    def add(self, token):
        self._tokens.append(token)

    def remove(self, token):
        self._tokens.remove(token)

    def sort(self):
        self._tokens.sort()


class NotHasTokenException(Exception):
    pass


class NotHasRuleException(Exception):
    pass


class Player:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.hand = kwargs.get('hand')
        self.rules = kwargs.get('rules')

    def __str__(self):
        return '<%s %s: %s>' % (self.id, self.name, str(self.hand))

    def __repr__(self):
        return self.__str__()

    def give_token(self, token, other_player):
        token = self.hand.search(token)
        if token:
            other_player.add_token(token)
            self.remove_token(token)
        else:
            raise NotHasTokenException

    def add_token(self, token):
        self.hand.add(token)

    def remove_token(self, token):
        self.hand.remove(token)

    def give_rule(self, other_player, rule=None, number=None):
        if rule:
            my_rule = self.rules.search(rule)
        else:
            my_rule = self.rules.search_by_number(number)
        if my_rule:
            other_player.add_rule(my_rule)
            self.remove_rule(my_rule)
        else:
            raise NotHasRuleException

    def add_rule(self, token):
        self.rules.add(token)

    def remove_rule(self, token):
        self.rules.remove(token)

    def is_matched_by_name(self, name):
        return self.name == name

    def is_matched_by_id(self, id):
        return self.id == id

    def sort_hand(self):
        self.hand.sort()

    def sort_rules(self):
        self.rules.sort()


class NoPlayerException(Exception):
    pass


class Players:

    def __init__(self):
        self.players = []

    def append(self, player):
        self.players.append(player)

    def search_by_id(self, id):
        for player in self.players:
            if player.is_matched_by_id(id):
                return player
        else:
            raise NoPlayerException

    def search_by_name(self, name):
        for player in self.players:
            if player.is_matched_by_name(name):
                return player
        else:
            raise NoPlayerException

    def __str__(self):
        return self.players.__str__()


class Deck:

    def __init__(self):
        self.tokens = []
        self.make()

    def make(self):
        for suit in all_suit.keys():
            #for key, value in all_numbers.items():
            for key in all_numbers.keys():
                #if key > 0:
                #    self.tokens.append(Card(suit, value))
                self.tokens.append(Card(suit, key))

        #self.tokens.append(Card(all_suit['j'], all_numbers[-1]))

        shuffle(self.tokens)

    def draw_card(self):
        return self.tokens.pop()


def change_card_number(number):
    number = number.lower()
    if number == 'k':
        return 13
    elif number == 'q':
        return 12
    elif number == 'j':
        return 11
    else:
        return int(number)


class GameSettingReader:

    def __init__(self, path):
        self.path = path

    def read(self):
        print('foo')
        rules = []
        with open(self.path, 'r') as f:
            lines = f.readlines()

            num_players = -1
            line = lines.pop(0)
            num_players_line = line.strip().split('=')
            if num_players_line[0].lower() in ['num_players', 'num_player']:
                if num_players_line[1].isdigit():
                    num_players = int(num_players_line[1])
                else:
                    raise Exception
            else:
                raise Exception

            player_names = []
            i = num_players
            while i > 0:
                line = lines.pop(0)
                name = line.strip()
                player_names.append(name)
                i -= 1

            token_type = 'foo'
            line = lines.pop(0)
            token_types = line.strip().split('=')
            if token_types[0].lower() == 'token':
                if token_types[1].lower() == 'card':
                    token_type = 'card'
                elif token_types[1].lower() == 'coin':
                    token_type = 'coin'
                    pass
                else:
                    raise Exception

            num_rules = -1
            line = lines.pop(0)
            num_rules_line = line.strip().split('=')
            if num_rules_line[0].lower() in ['rule', 'rules']:
                if num_rules_line[1].isdigit():
                    num_rules = int(num_rules_line[1])
                else:
                    raise Exception
            else:
                raise Exception

            separate_character = ','
            line = lines.pop(0)
            separate_character_line = line.strip().split('=')
            if separate_character_line[0].lower() == 'separate_character':
                separate_character = separate_character_line[1]
            else:
                raise Exception

            while num_rules > 0:
                line = lines.pop(0)
                number, text = line.strip().split(separate_character)
                rules.append(Rule(int(number), text))
                num_rules -= 1

            rules = Rules(rules)

            players = []
            for name in player_names:
                line = lines.pop(0)
                numbers = line.strip().split(separate_character)
                someone_rules = [rules.search_by_number(int(number)) for number in numbers]
                someone_rules = Rules(someone_rules)
                player = Player(name=name, rules=someone_rules)
                players.append(player)

            for player in players:
                line = lines.pop(0)
                tmp_tokens = line.strip().split(separate_character)

                tokens = []
                if token_type == 'card':
                    for token in tmp_tokens:
                        if token_type == 'card':
                            suit, number = token[0], token[1:]
                            number = change_card_number(number)
                            tokens.append(Card(suit, int(number)))
                hand = Hand(tokens)
                player.hand = hand

        return players
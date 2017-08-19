# -*- coding: utf-8 -*-
from random import shuffle
from itertools import repeat
import codecs

all_suit = {'s': ':spades:',
            'h': ':heart:',
            'c': ':clubs:',
            'd': ':diamonds:',
            'j': '',
            }

all_numbers = {1: 'A',
               2: '2',
               3: '3',
               4: '4',
               5: '5',
               6: '6',
               7: '7',
               8: '8',
               9: '9',
               10: '10',
               11: 'J',
               12: 'Q',
               13: 'K',
               0: ':black_joker:'
               }

all_color = {
                'g': ':green_heart:',
                'b': ':blue_heart:',
                'r': ':heart:',
                'y': ':yellow_heart:',
                'p': ':purple_heart:',
}

color_lt_dic = {
    'r': 0,
    'b': 1,
    'g': 2,
    'y': 3,
    'p': 4,
}


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
        self._rules = sorted(self._rules, key=lambda rule: rule.number)


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
            if self.suit == other.suit:
                numbers_li_dic = {  1: 14,
                                    2: 2,
                                    3: 3,
                                    4: 4,
                                    5: 5,
                                    6: 6,
                                    7: 7,
                                    8: 8,
                                    9: 9,
                                    10: 10,
                                    11: 11,
                                    12: 12,
                                    13: 13,
                                    0: 15,
                                }
                return numbers_li_dic[self.number] < numbers_li_dic[other.number]
            else:
                suit_lt_dic = {'s': 0,
                               'h': 1,
                               'c': 2,
                               'd': 3,
                               'j': 4, }
                return suit_lt_dic[self.suit] < suit_lt_dic[other.suit]
        else:
            return False


class Coin(Token):

    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return all_color[self.color]

    def __eq__(self, other):
        if isinstance(other, Coin):
            return self.color == other.color
        else:
            return False

    def is_equal(self, **kwargs):
        color = kwargs.get('color')
        return self.color == color

    def __lt__(self, other):
        if isinstance(other, Coin):
            return color_lt_dic[self.color] < color_lt_dic[other.color]
        else:
            return False


class Tokens:

    def __init__(self, **kwargs):
        tokens = kwargs.get('tokens')
        if tokens:
            self._tokens = tokens
        else:
            self._tokens = []

    def search(self, other):
        for token in self._tokens:
            if token == other:
                return token
        else:
            return None

    def __str__(self):
        return repr(self)

    def add(self, token):
        self._tokens.append(token)

    def remove(self, token):
        self._tokens.remove(token)

    def sort(self):
        self._tokens = sorted(self._tokens)

    def get_tokens(self):
        return self._tokens


class Cards(Tokens):

    def __init__(self, **kwargs):
        tokens = kwargs.get('cards')
        if tokens:
            self._tokens = tokens
        else:
            self._tokens = []

    def __repr__(self):
        return ' '.join([str(token) for token in self._tokens])


class Coins(Tokens):

    def __init__(self, **kwargs):
        tokens = kwargs.get('coins')
        if tokens:
            self._tokens = tokens
        else:
            self._tokens = []

    def __repr__(self):
        color_count = self._get_color_count()
        color_count = ['%s×%d' % (all_color[count[0]], count[1]) for count in color_count if count]
        return ' '.join(color_count)

    def get_num_color_coins(self, color):
        color_count = self._get_color_count()
        if color_count[color_lt_dic[color]]:
            return color_count[color_lt_dic[color]][1]
        else:
            return 0

    def _get_color_count(self):
        color_count = list(repeat([], len(color_lt_dic)))
        for coin in self._tokens:
            coin_idx = color_lt_dic[coin.color]
            if not color_count[coin_idx]:
                color_count[coin_idx] = [coin.color, 1]
            else:
                color_count[coin_idx][1] += 1
        return color_count


class NotHasTokenException(Exception):
    pass


class NotHasRuleException(Exception):
    pass


class Player:

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.tokens = kwargs.get('tokens')
        self.rules = kwargs.get('rules')

    def __str__(self):
        return '<%s %s: %s>' % (self.id, self.name, str(self.tokens))

    def __repr__(self):
        return self.__str__()

    def give_token(self, token, other_player):
        token = self.tokens.search(token)
        if token:
            other_player.add_token(token)
            self.remove_token(token)
        else:
            raise NotHasTokenException

    def add_token(self, token):
        self.tokens.add(token)

    def remove_token(self, token):
        self.tokens.remove(token)

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

    def sort_tokens(self):
        self.tokens.sort()

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
    if number == 'a':
        return 1
    elif number == 'k':
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
        rules = []
        with codecs.open(self.path, 'r', 'utf-8') as f:
            lines = f.readlines()

            #最初の１行はコメント行なのでとりのぞく
            lines.pop(0)

            num_players = -1
            line = lines.pop(0)
            num_players_line = line.strip().split('=')
            if num_players_line[0].lower() in ['num_players', 'num_player']:
                if num_players_line[1].isdigit():
                    num_players = int(num_players_line[1])
                else:
                    raise Exception('num_playersが正しく入力されていません')
            else:
                raise Exception('num_playersが正しく入力されていません')

            player_names = []
            i = num_players
            while i > 0:
                line = lines.pop(0)
                name = line.strip()
                player_names.append(name)
                i -= 1

            self.token_type = 'foo'
            line = lines.pop(0)
            token_types = line.strip().lower().split('=')
            if token_types[0] == 'token':
                if token_types[1] == 'card':
                    self.token_type = 'card'
                elif token_types[1] == 'coin':
                    self.token_type = 'coin'
                    pass
                else:
                    raise Exception('tokenが正しく入力されていません')

            num_rules = -1
            line = lines.pop(0)
            num_rules_line = line.strip().lower().split('=')
            if num_rules_line[0] in ['rule', 'rules']:
                if num_rules_line[1].isdigit():
                    num_rules = int(num_rules_line[1])
                else:
                    raise Exception('num_rulesが正しく入力されていません')
            else:
                raise Exception('num_rulesが正しく入力されていません')

            separate_character = ','
            line = lines.pop(0)
            separate_character_line = line.strip().lower().split('=')
            if separate_character_line[0] == 'separate_character':
                separate_character = separate_character_line[1]
            else:
                raise Exception('separate_characterが正しく入力されていません')

            while num_rules > 0:
                line = lines.pop(0)
                number, text = line.strip().split(separate_character)
                rules.append(Rule(int(number), text))
                num_rules -= 1

            rules = Rules(rules)

            self.players = []
            for name in player_names:
                line = lines.pop(0)
                numbers = line.strip().split(separate_character)
                someone_rules = [rules.search_by_number(int(number)) for number in numbers]
                someone_rules = Rules(someone_rules)
                player = Player(name=name, rules=someone_rules)
                self.players.append(player)

            for player in self.players:
                line = lines.pop(0)
                tmp_tokens = line.strip().split(separate_character)

                tokens = 'foo'
                if self.token_type == 'card':
                    cards = []
                    for card in tmp_tokens:
                        suit, number = card[0], card[1:]
                        number = change_card_number(number)
                        cards.append(Card(suit, int(number)))
                    tokens = Cards(cards=cards)
                elif self.token_type == 'coin':
                    coins = []
                    for coin in tmp_tokens:
                        color = coin[0]
                        coins.append(Coin(color))
                    tokens = Coins(coins=coins)
                player.tokens = tokens

    def get_players(self):
        return self.players

    def get_token_type(self):
        return self.token_type


class GameManager:

    def __init__(self):
        self.does_start = False
        self.token_type = None

    def set_token_type(self, token_type):
        self.token_type = token_type


class Vote:

    def __init__(self, player, content):
        self.player = player
        self.content = content

    def __repr__(self):
        return '@%s %s' % (self.player.name, self.content)

    def is_matched_by_player_name(self, name):
        return self.player.name == name


class NoVoteException(Exception):
    pass


class Votes:

    def __init__(self, votes):
        self._votes = votes

    def append(self, vote):
        try:
            _vote = self.search_player_vote_by_player_name(vote.player.name)
            _vote.content = vote.content
        except NoPlayerException:
            self._votes.append(vote)

    def search_player_vote_by_player_name(self, name):
        for vote in self._votes:
            if vote.is_matched_by_player_name(name):
                return vote
        else:
            raise NoPlayerException

    def __repr__(self):
        return '  '.join([repr(vote) for vote in self._votes])

    def clear(self):
        self._votes = []

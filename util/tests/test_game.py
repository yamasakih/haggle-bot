import unittest
from util.game import Rule, Card, Player, Cards, NotHasTokenException, Token, Players, \
                    NoPlayerException, Rules, Coin, Coins, Vote, Votes


class TestSample(unittest.TestCase):

    def test_add(self):
        self.assertEqual(3, 3)


class TestRule(unittest.TestCase):

    def setUp(self):
        self.rule1 = Rule(1, 'test')
        self.rule2 = Rule(1, 'test')
        self.rule3 = Rule(2, 'test')
        self.rule4 = Rule(1, 'foo')

    def test_numberとtextが一致していたら等しいとみなされる(self):
        self.assertEqual(self.rule1, self.rule2)
        self.assertNotEqual(self.rule1, self.rule3)
        self.assertNotEqual(self.rule1, self.rule4)

        self.assertNotEqual(self.rule2, self.rule3)
        self.assertNotEqual(self.rule2, self.rule4)

        self.assertNotEqual(self.rule3, self.rule4)

    def test_is_match_by_number_でnumberが一致していたらTrueを返す(self):
        self.assertTrue(self.rule1.is_match_by_number(self.rule2.number))

    def test_strでルール番号text部分と表示される(self):
        self.assertEqual(str(self.rule1), '```ルール1: test```')
        self.assertEqual(str(self.rule2), '```ルール1: test```')


class TestRules(unittest.TestCase):

    def setUp(self):
        rules = []
        rules.append(Rule(1, 'test'))
        rules.append(Rule(1, 'test'))
        self.rule2 = Rule(2, 'test')
        rules.append(self.rule2)
        rules.append(Rule(1, 'foo'))
        self.rules = Rules(rules)

    def test_strで_rulesリストの中を表示する(self):
        print(self.rules)
        self.assertEqual(str(self.rules), '```ルール1: test``` ```ルール1: test``` ```ルール2: test``` ```ルール1: foo```')

    def test_search_by_numberでnumberで検索をする(self):
        #TestCaseでは同じnumberのものがあるが、ゲームでは同じnumberのものはないという仕様で作っている。
        rule = self.rules.search_by_number(2)
        self.assertEqual(self.rule2, rule)

    def test_search_by_numberでnumberで検索をしてみつからなければNoneを返す(self):
        rule = self.rules.search_by_number(10)
        self.assertIsNone(rule)

    def test_searchで引数のruleオブジェクトと同じオブジェクトを検索する(self):
        rule = self.rules.search(self.rule2)
        self.assertEqual(rule.number, 2)
        self.assertEqual(rule.text, 'test')

    def test_searchで引数のruleオブジェクトと同じオブジェクトを検索してみつからなければNoneを返す(self):
        rule = self.rules.search(Rule(10, 'foo'))
        self.assertIsNone(rule)

    def test_sortでルールが番号順に並ぶ(self):
        rules = []
        rules.append(Rule(3, 'test3'))
        rules.append(Rule(1, 'test1'))
        rules.append(Rule(6, 'test6'))
        rules.append(Rule(2, 'test2'))
        rules.append(Rule(4, 'test4'))
        rules.append(Rule(10, 'test10'))
        rules = Rules(rules)


class TestCard(unittest.TestCase):

    def test_strでspades_1と表示される(self):
        card = Card('s', 1)
        self.assertEqual(card.__str__(), ':spades:A')

    def test_strでdiamonds_10と表示される(self):
        card = Card('d', 10)
        self.assertEqual(card.__str__(), ':diamonds:10')

    def test_numberとsuitが一致していたら等しいとみなされる(self):
        card1 = Card('s', 1)
        card2 = Card('s', 1)
        card3 = Card('d', 1)
        card4 = Card('s', 10)

        self.assertTrue(card1 == card2)
        self.assertFalse(card1 == card3)
        self.assertFalse(card1 == card4)
        self.assertFalse(card3 == card4)

    def test_スペードの10とダイヤの10を比較するとスペードの10の方が小さい(self):
        card1 = Card('s', 10)
        card2 = Card('d', 10)

        self.assertLess(card1, card2)

    def test_ハートの5とクラブの9を比較するとハートの5の方が小さい(self):
        card1 = Card('h', 5)
        card2 = Card('c', 9)

        self.assertLess(card1, card2)

    def test_スペードの2とクラブの7を比較するとスペードの2の方が小さい(self):
        card1 = Card('s', 2)
        card2 = Card('c', 7)

        self.assertLess(card1, card2)

    def test_ハートの7とダイヤの3を比較するとハートの7の方が小さい(self):
        card1 = Card('h', 7)
        card2 = Card('d', 3)

        self.assertLess(card1, card2)

    def test_クラブの10とJOKERを比較するとクラブの10の方が小さい(self):
        card1 = Card('c', 10)
        card2 = Card('j', 0)

        self.assertLess(card1, card2)


class TestCards(unittest.TestCase):

    def setUp(self):
        cards = []
        cards.append(Card('d', 12))
        cards.append(Card('s', 3))
        cards.append(Card('h', 12))
        cards.append(Card('s', 10))
        cards.append(Card('c', 2))
        cards.append(Card('s', 5))
        cards.append(Card('d', 13))
        cards.append(Card('d', 5))
        cards.append(Card('h', 1))
        cards.append(Card('c', 1))
        cards.append(Card('d', 1))
        self.cards = Cards(cards=cards)

    def test_reprで手札が表示される(self):
        self.assertEqual(repr(self.cards), ':diamonds:Q :spades:3 :heart:Q :spades:10 :clubs:2 :spades:5 :diamonds:K :diamonds:5 :heart:A :clubs:A :diamonds:A')

    def test_searchでスペードの3を探すと見つかる(self):
        card = self.cards.search(Card('s', 3))
        self.assertEqual(card.number, 3)
        self.assertEqual(card.suit, 's')

    def test_sortで最初スートがスペード_ハート_クラブ_ダイアを優先にして次にA_K_Q_J_10_9から2へとソートされる(self):
        self.cards.sort()
        sorted_tokens = self.cards.get_tokens()
        print(sorted_tokens)
        self.assertEqual(sorted_tokens[0].suit, 's')
        self.assertEqual(sorted_tokens[0].number, 3)
        self.assertEqual(sorted_tokens[1].suit, 's')
        self.assertEqual(sorted_tokens[1].number, 5)
        self.assertEqual(sorted_tokens[2].suit, 's')
        self.assertEqual(sorted_tokens[2].number, 10)
        self.assertEqual(sorted_tokens[3].suit, 'h')
        self.assertEqual(sorted_tokens[3].number, 12)
        self.assertEqual(sorted_tokens[4].suit, 'h')
        self.assertEqual(sorted_tokens[4].number, 1)
        self.assertEqual(sorted_tokens[5].suit, 'c')
        self.assertEqual(sorted_tokens[5].number, 2)
        self.assertEqual(sorted_tokens[6].suit, 'c')
        self.assertEqual(sorted_tokens[6].number, 1)
        self.assertEqual(sorted_tokens[7].suit, 'd')
        self.assertEqual(sorted_tokens[7].number, 5)
        self.assertEqual(sorted_tokens[8].suit, 'd')
        self.assertEqual(sorted_tokens[8].number, 12)
        self.assertEqual(sorted_tokens[9].suit, 'd')
        self.assertEqual(sorted_tokens[9].number, 13)
        self.assertEqual(sorted_tokens[10].suit, 'd')
        self.assertEqual(sorted_tokens[10].number, 1)


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.rule1 = Rule(1, 'foo')
        self.rule2 = Rule(2, 'baz')
        self.rule3 = Rule(3, 'bar')
        self.rules1 = Rules([self.rule1, self.rule2])
        self.rules2 = Rules([self.rule3])
        self.player = Player(id='001', name='foo', tokens=Cards(), rules=self.rules1)
        self.other_player = Player(id='002', name='baz', tokens=Cards(), rules=self.rules2)

    def test_give_tokenするトークンを持っていないとNotHasTokenExceptionを出す(self):
        self.assertRaises(NotHasTokenException, lambda: self.player.give_token(Card('s', 1), self.other_player))

    def test_give_ruleでnumberが1のルールをわたす(self):
        self.player.give_rule(self.other_player, number=1)
        self.assertEqual(len(self.player.rules._rules), 1)
        self.assertEqual(len(self.other_player.rules._rules), 2)


class TestCoin(unittest.TestCase):

    def test_reprで表示すると_heart_と表示される(self):
        coin = Coin(color='r')
        self.assertEqual(repr(coin), ':heart:')

    def test_色が同じなら等しい(self):
        coin1 = Coin(color='r')
        coin2 = Coin(color='b')
        coin3 = Coin(color='r')

        self.assertNotEqual(coin1, coin2)
        self.assertEqual(coin1, coin3)
        self.assertNotEqual(coin2, coin3)

    def test_is_equalで特定の色のcolorオブジェクトを見つけられる(self):
        coin1 = Coin(color='r')
        coin2 = Coin(color='b')
        coin3 = Coin(color='r')

        self.assertFalse(coin1.is_equal(color='b'))
        self.assertTrue(coin2.is_equal(color='b'))
        self.assertFalse(coin3.is_equal(color='b'))

        self.assertTrue(coin1.is_equal(color='r'))
        self.assertFalse(coin2.is_equal(color='r'))
        self.assertTrue(coin3.is_equal(color='r'))

    """
    def test_色の比較は赤青緑黄色紫の順に大きくなっていく(self):
        coin1 = Coin(color='r')
        coin2 = Coin(color='b')
        coin3 = Coin(color='g')
        coin4 = Coin(color='y')
        coin5 = Coin(color='p')

        self.assertTrue(coin1 < coin2)
        self.assertLess(coin2, coin3)
        self.assertLess(coin3, coin4)
        self.assertLess(coin4, coin5)
    """


class TestCoins(unittest.TestCase):

    def setUp(self):
        coins = list()
        coins.append(Coin('r'))
        coins.append(Coin('b'))
        coins.append(Coin('r'))
        coins.append(Coin('g'))
        self.coins = Coins(coins=coins)

    def test_reprで各コインの枚数を表示する(self):
        self.assertEqual(repr(self.coins), ':heart:×2 :blue_heart:×1 :green_heart:×1')

    def test_赤の色のコインが何枚あるか調べると2が返ってくる(self):
        self.assertEqual(self.coins.get_num_color_coins('r'), 2)

    def test_青の色のコインが何枚あるか調べると1が返ってくる(self):
        self.assertEqual(self.coins.get_num_color_coins('b'), 1)

    def test_黄色のコインが何枚あるか調べると0が返ってくる(self):
        self.assertEqual(self.coins.get_num_color_coins('y'), 0)

    def test_sortで赤青緑黄色紫の順に並ぶ(self):
        self.coins.sort()
        sorted_tokens = self.coins.get_tokens()
        print(sorted_tokens)
        self.assertEqual(sorted_tokens[0].color, 'r')
        self.assertEqual(sorted_tokens[1].color, 'r')
        self.assertEqual(sorted_tokens[2].color, 'b')
        self.assertEqual(sorted_tokens[3].color, 'g')


class TestPlayers(unittest.TestCase):

    def setUp(self):
        self.player1 = Player(id='001', name='foo')
        self.player2 = Player(id='002', name='baz')
        self.players = Players()
        self.players.append(self.player1)
        self.players.append(self.player2)

    def test_search_by_nameで検索するとplayer1と同じオブジェクトがみつかる(self):
        self.assertEqual(self.players.search_by_name('foo'), self.player1)

    def test_id_de_search_site_mitsukerareru(self):
        self.assertEqual(self.players.search_by_id('002'), self.player2)

    def test_name_de_search_sitemo_inaito_exception(self):
        self.assertRaises(NoPlayerException, lambda: self.players.search_by_name('bar'))

    def test_id_de_search_sitemo_inaito_exception(self):
        self.assertRaises(NoPlayerException, lambda: self.players.search_by_id('000'))


class TestVote(unittest.TestCase):

    def setUp(self):
        self.player1 = Player(id='001', name='foo')
        self.player2 = Player(id='002', name='baz')
        self.vote1 = Vote(player=self.player1, content='morning')
        self.vote2 = Vote(player=self.player2, content='noon')

    def test_reprでvote1の投票者と投票内容を表示する(self):
        self.assertEqual(repr(self.vote1), '@foo morning')

    def test_reprでvote2の投票者と投票内容を表示する(self):
        self.assertEqual(repr(self.vote2), '@baz noon')


class TestVotes(unittest.TestCase):

    def setUp(self):
        self.player1 = Player(id='001', name='foo')
        self.player2 = Player(id='002', name='baz')
        self.player3 = Player(id='003', name='bar')
        self.players = Players()
        self.players.append(self.player1)
        self.players.append(self.player2)
        self.players.append(self.player3)
        self.vote1 = Vote(player=self.player1, content='morning')
        self.vote2 = Vote(player=self.player2, content='noon')
        self.vote3 = Vote(player=self.player3, content='evening')
        self.votes = Votes([self.vote1, self.vote2])

    def test_appendでvoteを追加することができる(self):
        self.votes.append(self.vote3)
        self.assertEqual(len(self.votes._votes), 3)

    def test_reprで投票内容全てを表示する(self):
        self.assertEqual(repr(self.votes), '@foo morning  @baz noon')


if __name__ == "__main__":
    unittest.main()


from slackbot.bot import respond_to
from slacker import Slacker
import re
import os
from haggle.slackbot_settings import API_TOKEN
from util.game import *

#haggle_bot_name = "ri"
haggle_bot_name = "boss"

players = Players()
game_manager = GameManager()
game_has_started_message = 'ゲームのための準備はすでにされています。'
game_staring_message = 'ゲーム%sのための準備をしました！'
game_setting_not_found_exception_message = '%sという名前のゲーム設定ファイルがありません。'
no_player_exception_message = 'あなたはゲームに正しく参加できていないようです。GMに問い合わせてください。'
give_card_message = 'カード%sを%sにわたしました！'
give_coin_message = '%sを%sにわたしました！'
give_rule_message = 'ルール%sを%sにわたしました！'
not_has_card_exception_message = 'カード%sはもっていないようです。'
not_has_coin_exception_message = 'ハート%sはもっていないようです。'
not_has_rule_exception_message = 'ルール%dはもっていないようです。'
no_other_player_exception_message = 'プレイヤー%sはゲームに参加していません。'
not_valid_number_exception_message = '数字の指定が正しくありません。'
coin_info_error_message = 'ハートの色と数が正しく入力されていません'
show_one_card_example_message = '例えばスペードの10なら . hand s10 と書いてください。'
show_one_coin_example_message = '例えば赤のハート1つなら . hand r1 と書いてください。'
show_one_rule_example_message = '例えばルール5なら . rule 5 と書いてください。'
give_one_card_example_message = '例えばスペードの10なら . hand s10 他のプレイヤー と書いてください。'
give_one_coin_example_message = '例えば赤のハート1つ青のハート2つなら . hand r1,b2 他のプレイヤー と書いてください。'
give_one_rule_example_message = '例えばルール5なら . rule 5 他のプレイヤー と書いてください。'
card_index_error_message = 'カード名とわたす相手が正しく入力されていません'
coin_index_error_message = 'ハートの色と数が正しく入力されていません'
rule_index_error_message = 'ルール番号とわたす相手が正しく入力されていません'
card_sort_message = 'カードを並びかえました！'
coin_sort_message = 'ハートを並びかえました！'
rule_sort_message = 'ルールを並びかえました！'
before_game_start_message = 'ゲームはまだ開始されていません。もうしばらくお待ち下さい。'
low_coin_message = '%sは%d枚しか持っていません。'
other_exception_message = '入力が正しくありません。わからない場合はGMに問い合わせてください。'


def get_name_by_id(users, id):
    for _name, _id in users:
        if _id == id:
            return _name
    return None


def get_id_by_name(users, name):
    for _name, _id in users:
        if _name == name:
            return _id


@respond_to('make (.*)')
def make_game(message, game_name):
    if not game_manager.does_start:
        try:
            reader = GameSettingReader(os.path.join('game_settings', game_name))
            reader.read()
            _players = reader.get_players()

            slack = Slacker(API_TOKEN)
            users = slack.users.list().body['members']
            users = [[user['name'], user['id']] for user in users]

            for player in _players:
                player.id = get_id_by_name(users, player.name)
                players.append(player)

            game_manager.set_token_type(reader.get_token_type())
            game_manager.does_start = True
            message.reply(game_staring_message % game_name)

        except FileNotFoundError:
            message.reply(game_setting_not_found_exception_message % game_name)
    else:
        message.reply(game_has_started_message)


def get_player_by_message(message):
    user = message.body['user']
    player = players.search_by_id(user)
    return player


def get_tokens_by_message(message):
    player = get_player_by_message(message)
    return player.tokens


def get_rules_by_message(message):
    player = get_player_by_message(message)
    return player.rules


@respond_to('^hand$', re.IGNORECASE)
def show_hand(message):
    if game_manager.does_start:
        try:
            message.reply(str(get_tokens_by_message(message)))
        except NoPlayerException:
            message.reply(no_player_exception_message)
    else:
        message.reply(before_game_start_message)


@respond_to('^heart ((?:[r,b,g,y,p][1-9])+) (.+)', re.IGNORECASE)
def show_hand(message, hearts, other_player):
    if game_manager.does_start:
        print(hearts, other_player)
        try:
            message.reply(str(get_tokens_by_message(message)))
        except NoPlayerException:
            message.reply(no_player_exception_message)
    else:
        message.reply(before_game_start_message)


@respond_to('^rule$', re.IGNORECASE)
def show_rules(message):
    if game_manager.does_start:
        try:
            rules = get_rules_by_message(message)
            message.reply(str(rules))
        except NoPlayerException:
            message.reply(no_player_exception_message)
    else:
        message.reply(before_game_start_message)


@respond_to('^hand ([s,h,c,d][a,j,q,k]|[j]|[s,h,c,d][1-9][0-3]*)$', re.IGNORECASE)
def show_one_card(message, card):
    if game_manager.does_start:
        if game_manager.token_type == 'card':
            try:
                tokens = get_tokens_by_message(message)
                card = card.lower()
                if card != 'j':
                    suit, number = card[0], card[1:]
                    number = change_card_number(number)
                else:
                    suit, number = 'j', 0
                card = tokens.search(Card(suit=suit, number=number))
                if card:
                    message.reply(str(card))
                else:
                    message.reply(not_has_card_exception_message % card)
            except ValueError:
                message.reply(not_valid_number_exception_message)
                message.reply(show_one_card_example_message)
            except NoPlayerException:
                message.reply(no_player_exception_message)
        else:
            message.reply(other_exception_message)
    else:
        message.reply(before_game_start_message)


@respond_to('^hand ((?:[r,b,g,y,p][1-9][0-9]*,?)+)$', re.IGNORECASE)
def show_coins(message, coin_info):
    if game_manager.does_start:
        if game_manager.token_type == 'coin':
            try:
                coin_info_list = coin_info.strip().split(',')
                coins = get_tokens_by_message(message)
                show_coins = []
                for coin_info in coin_info_list:
                    coin_info = coin_info.lower()
                    color, num = coin_info[0], int(coin_info[1:])
                    num_color_coins = coins.get_num_color_coins(color)
                    if num_color_coins < num:
                        coin_emoji = all_color[color]
                        message.reply(low_coin_message % (coin_emoji, num_color_coins))
                        break
                    else:
                        one_color_show_coins = [Coin(color=color) for i in range(num)]
                        show_coins.extend(one_color_show_coins)
                else:
                    message.reply(repr(Coins(coins=show_coins)))
            except ValueError:
                message.reply(not_valid_number_exception_message)
                message.reply(show_one_coin_example_message)
            except IndexError:
                message.reply(coin_index_error_message)
                message.reply(show_one_coin_example_message)
            except NoPlayerException:
                message.reply(no_player_exception_message)
        else:
            message.reply(other_exception_message)
    else:
        message.reply(before_game_start_message)


@respond_to('^rule ([1-9][0-9]*)$', re.IGNORECASE)
def show_one_rule(message, number):
    if game_manager.does_start:
        try:
            rules = get_rules_by_message(message)
            rule = rules.search_by_number(int(number))
            message.reply(str(rule))
        except NotHasRuleException:
            message.reply(not_has_rule_exception_message % number)
        except ValueError:
            message.reply(not_valid_number_exception_message)
            message.reply(show_one_rule_example_message)
        except NoPlayerException:
            message.reply(no_player_exception_message)
    else:
        message.reply(before_game_start_message)


@respond_to('^hand ([s,h,c,d][a,j,q,k]|[j]|[s,h,c,d][1-9][0-3]*) (.+)', re.IGNORECASE)
def give_card(message, card, other_user):
    if game_manager.does_start:
        if game_manager.token_type == 'card':
            user = message.body['user']
            try:
                player = players.search_by_id(user)

                try:
                    if card.lower() != 'j':
                        suit, number = card.lower()[0], card.lower()[1:]
                        number = change_card_number(number)
                    else:
                        suit, number = 'j', 0

                    other_player = players.search_by_name(other_user)

                    card_emoji = all_suit[suit] + all_numbers[int(number)]

                    player.give_token(Card(suit, number), other_player)

                    message.reply(give_card_message % (card_emoji, other_user,))

                except NoPlayerException:
                    message.reply(no_other_player_exception_message % other_user)
                except NotHasTokenException:
                    message.reply(not_has_card_exception_message % card)
                except ValueError:
                    message.reply(not_valid_number_exception_message)
                    message.reply(give_one_card_example_message)
                except IndexError:
                    message.reply(card_index_error_message)
                    message.reply(give_one_card_example_message)

            except NoPlayerException:
                message.reply(no_player_exception_message)
        else:
            message.reply(other_exception_message)
    else:
        message.reply(before_game_start_message)


#@respond_to('^hand ([r,b,g,y,p][1-9][0-9]*) (.+)', re.IGNORECASE)
#@respond_to('^hand ([r,b,g,y,p][1-9][0-9]*) (.+)$', re.IGNORECASE)
@respond_to('^hand ((?:[r,b,g,y,p][1-9][0-9]*,?)+) (.+)$', re.IGNORECASE)
def give_coins(message, coin_info, other_user):
    if game_manager.does_start:
        if game_manager.token_type == 'coin':
            user = message.body['user']
            try:
                player = players.search_by_id(user)

                try:
                    give_coins = []
                    coin_info_list = coin_info.strip().split(',')
                    coins = get_tokens_by_message(message)
                    other_player = players.search_by_name(other_user)
                    for coin_info in coin_info_list:
                        coin_info = coin_info.lower()
                        color, num = coin_info[0], int(coin_info[1:])
                        num_color_coins = coins.get_num_color_coins(color)
                        if num_color_coins < num:
                            coin_emoji = all_color[color]
                            message.reply(low_coin_message % (coin_emoji, num_color_coins))
                            break
                        else:
                            one_color_give_coins = [Coin(color=color) for i in range(num)]
                            give_coins.extend(one_color_give_coins)
                    else:
                        for coin in give_coins:
                            player.give_token(coin, other_player)

                        coin_emoji = repr(Coins(coins=give_coins))

                        message.reply(give_coin_message % (coin_emoji, other_user))

                except NoPlayerException:
                    message.reply(no_other_player_exception_message % other_user)
                except NotHasTokenException:
                    message.reply(not_has_coin_exception_message % coin_info)
                except ValueError:
                    message.reply(not_valid_number_exception_message)
                    message.reply(give_one_coin_example_message)
                except IndexError:
                    message.reply(coin_index_error_message)
                    message.reply(give_one_coin_example_message)

            except NoPlayerException:
                message.reply(no_player_exception_message)
        else:
            message.reply(other_exception_message)
    else:
        message.reply(before_game_start_message)


@respond_to('^rule ([1-9][0-9]*) (.+)', re.IGNORECASE)
def give_rule(message, number, other_user):
    if game_manager.does_start:
        user = message.body['user']
        try:
            player = players.search_by_id(user)

            try:
                other_player = players.search_by_name(other_user)

                player.give_rule(other_player=other_player, number=int(number))

                message.reply(give_rule_message % (number, other_user))

            except NoPlayerException:
                message.reply(no_other_player_exception_message % other_user)
            except NotHasRuleException:
                message.reply(not_has_rule_exception_message % number)
            except ValueError:
                message.reply(not_valid_number_exception_message)
                message.reply(give_one_rule_example_message)
            except IndexError:
                message.reply(rule_index_error_message)
                message.reply(give_one_rule_example_message)
        except NoPlayerException:
            message.reply(no_player_exception_message)
    else:
        message.reply(before_game_start_message)


@respond_to('^hand sort$')
def sort_hands(message):
    if game_manager.does_start:
        user = message.body['user']
        try:
            player = players.search_by_id(user)
            player.sort_tokens()
            message.reply(card_sort_message)
        except NoPlayerException:
            message.reply(no_player_exception_message)
    else:
        message.reply(before_game_start_message)


@respond_to('^rule sort$')
def sort_rule(message):
    if game_manager.does_start:
        user = message.body['user']
        try:
            player = players.search_by_id(user)
            player.sort_rules()
            message.reply(rule_sort_message)
        except NoPlayerException:
            message.reply(no_player_exception_message)
    else:
        message.reply(before_game_start_message)

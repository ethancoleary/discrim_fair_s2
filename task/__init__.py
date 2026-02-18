from otree.api import *
import random
import math
from common import MyBasePage

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'task'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1



class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

def check3_choices(player):
    # Base text for options 2 and 3 is the same for all treatments
    option2 = 'According to who belongs to the group which, on average, invested more in a previous study.'
    option3 = 'According to a real participant with past group data on investment who has an incentive to maximise their commission from investments made.'

    if player.participant.treatment < 4:
        option1 = 'According to who selected a randomly chosen painting.'
    else:
        option1 = 'According to who identified with a randomly selected gender.'

    return [
        [1, option1],
        [2, option2],
        [3, option3],
    ]
class Player(BasePlayer):
    investment300 = models.IntegerField(min=0,max=300)
    investment100 = models.IntegerField(min=0, max=100)
    slider_value = models.IntegerField(min=0, max=200, blank=True)
    check1 = models.IntegerField()
    check2 = models.IntegerField(
        choices=[
            [1, '1/6'],
            [2, '2/6'],
            [3, '3/6'],
            [4, '4/6'],
            [5, '5/6']
        ],
        widget=widgets.RadioSelect
    )
    check3 = models.IntegerField(
        widget=widgets.RadioSelect
    )
    check4 = models.IntegerField(
        choices= [
            [1, 'It will be added to your investment budget in the form of 50 tokens.'],
            [2, 'It will be added as an extra participation fee and cannot be affected by later decisions.'],
            [3, 'It will be added as an extra participation fee but may be affected by later decisions.']
        ],
        widget=widgets.RadioSelect
    )
    computer = models.IntegerField()
    chosen = models.IntegerField()
    incorrect1 = models.IntegerField(initial=0)
    incorrect2 = models.IntegerField(initial=0)
    incorrect3 = models.IntegerField(initial=0)
    incorrect4 = models.IntegerField(initial=0)
    transfer = models.IntegerField(initial=0)
    group_treatment_id = models.IntegerField(initial=0)
    treatment = models.IntegerField(initial=0)

    blur_log = models.LongStringField(blank=True)
    blur_count = models.IntegerField(initial=0, blank=True)
    blur_warned = models.IntegerField(initial=0, blank=True)




# PAGES
class TaskIntro1(MyBasePage):
    # add extra fields on top of base tracking fields
    @property
    def form_fields(self):
        return MyBasePage.form_fields + ['slider_value']


    @staticmethod
    def vars_for_template(player):
        ctx = MyBasePage.vars_for_template(player)

        treatment = player.participant.treatment
        player.treatment = player.participant.treatment

        if treatment < 4:
            player.participant.group = player.participant.painting
        elif treatment > 3:
            player.participant.group = player.participant.gender

        return ctx

class TaskIntro2(MyBasePage):
    @property
    def form_fields(self):
        return MyBasePage.form_fields + ['slider_value']

    @staticmethod
    def vars_for_template(player: Player):
        ctx = MyBasePage.vars_for_template(player)
        # add any page-specific vars here, then return
        # ctx.update({...})
        return ctx

class CompCheck(Page):
    form_model = 'player'
    form_fields = ['check1', 'check2', 'check3', 'check4']

    @staticmethod
    def error_message(player, values):
        if player.treatment == 1 or player.treatment == 4:
            correct_answer3 = 1
        elif player.treatment == 2:
            correct_answer3 = 2
        else:
            correct_answer3 = 3

        if values['check1'] != 300:
            player.incorrect1 = 1
            return ('Your answer to question 1 is wrong. One of you or your match will receive 300 tokens and the other 100.')

        elif values['check2'] != 2:
            player.incorrect2 = 1
            return (
                'Your answer to question 2 is wrong. The lottery is successful with a probability of 2/6.')

        elif values['check3'] != correct_answer3:
            player.incorrect3 = 1
            if player.treatment == 1:
                return (
                'Your answer to question 3 is wrong. A painting is chosen at random and the individual who chose that painting in the match receives 300 tokens, the other 100.')
            elif player.treatment == 2:
                return (
                    'Your answer to question 3 is wrong. A 300 token budget will be allocated to the individual from the group which, on average, invested more in a previous study.')
            elif player.treatment == 3:
                return (
                    'Your answer to question 3 is wrong. A decision maker will use data from a previous study to allocate a 300 token budget to the individual from the group it believes will invest more in the lottery.')
            elif player.treatment == 4:
                return (
                    'Your answer to question 3 is wrong. A gender group is chosen at random and the individual who belongs to that group in the match receives 300 tokens, the other 100.')
            elif player.treatment == 5:
                return (
                    'Your answer to question 3 is wrong. A decision maker will use data from a previous study to allocate a 300 token budget to the individual from the group it believes will invest more in the lottery.')

        elif values['check4'] != 3:
            player.incorrect4 = 1
            return (
                'Your answer to question 4 is wrong. The amount is added to the participation fee but may be affected by later decisions.')

    @staticmethod
    def before_next_page(player, timeout_happened):


        if player.treatment == 1:
            if player.participant.painting==1:
                player.group_treatment_id = 11
            else:
                player.group_treatment_id = 21

        elif player.treatment == 2:
            if player.participant.painting==1:
                player.group_treatment_id = 12
            else:
                player.group_treatment_id = 22

        elif player.treatment == 3:
            if player.participant.painting == 1:
                player.group_treatment_id = 13
            else:
                player.group_treatment_id = 23

        elif player.treatment == 4:
            if player.participant.gender == 1: #female
                player.group_treatment_id = 14
            else: #male
                player.group_treatment_id = 24

        elif player.treatment == 5:
            if player.participant.gender == 1: #female
                player.group_treatment_id = 15
            else: #male
                player.group_treatment_id = 25

        #temporarily assign chosen

        if player.treatment == 1 or player.treatment == 4:
            coin_flip = random.randint(0, 1)
            player.participant.chosen = coin_flip

            my_group = getattr(player.participant, 'group', None)
            my_chosen = getattr(player.participant, 'chosen', None)
            my_treatment = player.treatment
            my_index = player.participant._index_in_pages

            # opposite group, opposite chosen
            opp_group_treatment_chosen = [
                p for p in player.subsession.get_players()
                if p.id_in_subsession != player.id_in_subsession
                   and getattr(p, 'treatment', None) == my_treatment
                   and getattr(p.participant, 'group', None) is not None
                   and getattr(p.participant, 'chosen', None) is not None
                   and p.participant.group != my_group
                   and p.participant.chosen != my_chosen
            ]

            already_moved_on_opp = [
                p for p in opp_group_treatment_chosen
                if getattr(p.participant, '_index_in_pages', 0) > my_index
            ]
            n_moved_on_opp = len(already_moved_on_opp)

            # same group, same chosen
            same_group_treatment_chosen = [
                p for p in player.subsession.get_players()
                if p.id_in_subsession != player.id_in_subsession
                   and getattr(p, 'treatment', None) == my_treatment
                   and getattr(p.participant, 'group', None) is not None
                   and getattr(p.participant, 'chosen', None) is not None
                   and p.participant.group == my_group
                   and p.participant.chosen == my_chosen
            ]

            already_moved_on_same = [
                p for p in same_group_treatment_chosen
                if getattr(p.participant, '_index_in_pages', 0) > my_index
            ]
            n_moved_on_same = len(already_moved_on_same)

            # flip if imbalance > 20
            if n_moved_on_same > n_moved_on_opp + 20:
                player.participant.chosen = 1 - coin_flip

            player.chosen = player.participant.chosen


        ## COMPUTER
        elif player.treatment == 2:
            if player.participant.painting == 1:
                player.participant.chosen = 1
            else:
                player.participant.chosen = 0

        ## HUMAN PAINTING
        elif player.treatment == 3:
            if player.participant.painting == 1:
                player.participant.chosen = 1
            else:
                player.participant.chosen = 0

        ## HUMAN GENDER
        elif player.treatment == 5:
            if player.participant.gender == 1:
                player.participant.chosen = 0
            else:
                player.participant.chosen = 1

        player.chosen = player.participant.chosen

class TaskIntro3(Page):
    form_model = 'player'
    form_fields = ['blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def vars_for_template(player):

        # Chosen painting
        if player.treatment == 1:
            if player.participant.chosen == 1:
                if player.participant.painting==1:
                    chosenpainting = "A"
                else:
                    chosenpainting = "B"
            else:
                if player.participant.painting == 1:
                    chosenpainting = "B"
                else:
                    chosenpainting = "A"
        else:
            chosenpainting = ""

        # Chosen gender
        if player.treatment == 4:
            if player.participant.chosen == 1:
                if player.participant.gender == 1:
                    chosengender = "female"
                else:
                    chosengender = "male"
            else:
                if player.participant.gender == 1:
                    chosengender = "male"
                else:
                    chosengender = "female"
        else:
            chosengender = ""

        # DM chosen group
        if player.treatment == 3:
            chosen = "A"
        elif player.treatment == 5:
            chosen = "male"
        else:
            chosen = ""

        if player.treatment < 4:
            if player.participant.painting == 1:
                yourpainting = "A"
                matchpainting = "B"
            else:
                yourpainting = "B"
                matchpainting = "A"
        else:
            yourpainting = ""
            matchpainting = ""

        if player.participant.gender == 1:
            yourgender = "female"
            matchgender = "male"
        else:
            matchgender = "female"
            yourgender = "male"

        if player.participant.chosen == 1:
            yourbudget = 300
            matchbudget = 100
        else:
            yourbudget = 100
            matchbudget = 300




        return {
            'chosenpainting': chosenpainting,
            'chosen': chosen,
            'chosengender': chosengender,

            'yourpainting': yourpainting,
            'yourbudget': yourbudget,
            'yourgender': yourgender,

            'matchpainting': matchpainting,
            'matchbudget': matchbudget,
            'matchgender': matchgender,
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }


class Decision(Page):
    form_model = 'player'
    form_fields = ['transfer', 'blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def is_displayed(player):
        return player.chosen == 0

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.steal = player.transfer

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }

class InvestmentDecision300(Page):
    form_model = 'player'
    form_fields = ['investment300', 'blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def is_displayed(player):
        return player.chosen == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        die = random.randint(1, 6)
        participant.die = die
        participant.investment = player.investment300

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }

class InvestmentDecision100(Page):
    form_model = 'player'
    form_fields = ['investment100', 'blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def is_displayed(player):
        return player.chosen == 0

    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        die = random.randint(1, 6)
        participant.die = die
        participant.investment = player.investment100

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }


page_sequence = [
                TaskIntro1,
                TaskIntro2,
                CompCheck,
                TaskIntro3,
                Decision,
                InvestmentDecision300,
                InvestmentDecision100
                ]

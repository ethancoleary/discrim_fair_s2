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
        choices = [
            [1, 'According to who identified with a randomly selected gender.'],
            [2, 'According to who belongs to the group which, on average, invested more in a previous study.'],
            [3, 'According to a real participant with past group data on investment who wishes to maximize their commission from investments.']
        ],
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
class TaskIntro(MyBasePage):
    # add extra fields on top of base tracking fields
    @property
    def form_fields(self):
        return MyBasePage.form_fields + ['slider_value']


    @staticmethod
    def vars_for_template(player):
        ctx = MyBasePage.vars_for_template(player)

        treatment = player.participant.treatment

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
        if values['check1'] != 300:
            player.incorrect1 = 1
            return ('Your answer to question 1 is wrong. One of you or your match will receive 300 tokens and the other 100.')

        elif values['check2'] != 2:
            player.incorrect2 = 1
            return (
                'Your answer to question 2 is wrong. The lottery is successful with a probability of 2/6.')

        elif values['check3'] != player.treatment:
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


        elif values['check4'] != 3:
            player.incorrect4 = 1
            return (
                'Your answer to question 4 is wrong. The amount is added to the participation fee but may be affected by later decisions.')

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Identify others with same group_treatment_id and treatment, NOT counting current player
        same_group_treatment = [
            p for p in player.subsession.get_players()
            if p != player and
               p.group_treatment_id == player.group_treatment_id and
               p.treatment == player.treatment
        ]
        # Count those who have gone past CompCheck (i.e., their page index > this page index)
        # We can check participant._index_in_pages; oTree increases this with each page.
        # Alternatively, you might use p.participant.vars or a flag set after CompCheck.
        my_index = player.participant._index_in_pages
        already_moved_on = [
            p for p in same_group_treatment
            if p.participant._index_in_pages > my_index
        ]
        n_moved_on = len(already_moved_on)

        # Set chosen based on parity
        if n_moved_on % 2 == 0:
            player.chosen = 1
        else:
            player.chosen = 0

class TaskIntro3(Page):
    form_model = 'player'
    form_fields = ['blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def vars_for_template(player):

        if player.participant.group == 1:
            if player.chosen == 1:
                chosen = "male"
            else:
                chosen = "female"
        else:
            if player.chosen == 1:
                chosen = "female"
            else:
                chosen = "male"


        if player.participant.group == 1:
            yourgender = "male"
            partnergender = "female"
        else:
            yourgender = "female"
            partnergender = "male"

        if player.chosen == 1:
            yourbudget = "300"
            partnerbudget = "100"
        else:
            yourbudget = "100"
            partnerbudget = "300"

        return {
            'chosen': chosen,
            'yourgender': yourgender,
            'partnergender': partnergender,
            'yourbudget': yourbudget,
            'partnerbudget': partnerbudget,
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

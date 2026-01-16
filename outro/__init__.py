from otree.api import *
import random
import math

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'outro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ethnicity = models.IntegerField(
        choices=[
            [1, 'Asian'],
            [2, 'Black'],
            [3, 'Latino/a'],
            [4, 'Mixed/ Multiple Ethnicity'],
            [5, 'Native American'],
            [6, 'White'],
            [7, 'Other']
        ],
        widget=widgets.RadioSelect
    )
    political_affil = models.IntegerField(
        choices=[
            [1, 'Independent, left leaning'],
            [2, 'Democrat'],
            [3, 'Independent, centre'],
            [4, 'Republican'],
            [5, 'Independent, right leaning']
        ],
        widget=widgets.RadioSelect
    )
    education = models.IntegerField(
        choices=[
            [1, 'Less than high school'],
            [2, 'High school diploma'],
            [3, 'Some college'],
            [4, 'Bachelor\'s degree or equivalent (e.g. Associate\'s degree)'],
            [5, 'Master\'s degree or higher (e.g. Professional or Doctoral degree)']
        ],
        widget=widgets.RadioSelect
    )
    education_economics = models.IntegerField(
        choices=[
            [1, 'Yes'],
            [2, 'No']
        ],
        widget=widgets.RadioSelect
    )
    work_status = models.IntegerField(
        choices=[
            [1, 'Full-time employed'],
            [2, 'Part-time employed'],
            [3, 'Unemployed'],
            [4, 'Student'],
            [5, 'Retired'],
            [6, 'Other']
        ],
        widget=widgets.RadioSelect
    )
    children = models.IntegerField(
        choices=[
            [0, '0'],
            [1, '1'],
            [2, '2'],
            [3, '3'],
            [4, '4+']
        ],
        widget=widgets.RadioSelect
    )
    income = models.IntegerField(
        choices=[
            [1, 'Under $15,000'],
            [2, '$15,000 to $24,999'],
            [3, '$25,000 to $34,999'],
            [4, '$35,000 to $49,999'],
            [5, '$50,000 to $74,999'],
            [6, '$75,000 to $99,999'],
            [7, '$100,000 to $149,999'],
            [8, '$150,000 to $199,999'],
            [9, '$200,000 and over']
        ],
        widget=widgets.RadioSelect
    )
    political_social = models.IntegerField(
        choices=[
            [1, 'Very liberal'],
            [2, 'Somewhat liberal'],
            [3, 'Neutral'],
            [4, 'Somewhat conservative'],
            [5, 'Very conservative']
        ],
        widget=widgets.RadioSelect
    )
    political_economic = models.IntegerField(
        choices=[
            [1, 'Very liberal'],
            [2, 'Somewhat liberal'],
            [3, 'Neutral'],
            [4, 'Somewhat conservative'],
            [5, 'Very conservative']
        ],
        widget=widgets.RadioSelect
    )
    inequality = models.IntegerField(
        choices = [
            [1, 'Too little'],
            [2, 'Acceptable'],
            [3, 'Too much']
        ],
        widget=widgets.RadioSelect
    )
    representation = models.IntegerField(
        choices=[
            [1, 'Too little'],
            [2, 'Acceptable'],
            [3, 'Too much']
        ],
    widget = widgets.RadioSelect
    )
    discrim_work = models.IntegerField(
        choices = [
            [1, 'Yes'],
            [2, 'No'],
            [3, 'Not sure']
        ],
        widget=widgets.RadioSelect
    )
    discrim_work_identity_age = models.IntegerField(
        initial = 0,
        choices = [
            [0, 'No'],
            [1, 'Yes']
        ],
        blank=True,
    )
    discrim_work_identity_gender = models.IntegerField(
        initial=0,
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ],
        blank=True,

    )
    discrim_work_identity_race = models.IntegerField(
        initial=0,
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ],
        blank=True,
    )
    discrim_work_identity_disability = models.IntegerField(
        initial=0,
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ],
        widget=widgets.RadioSelect,
        blank=True,
    )
    discrim_work_identity_religion = models.IntegerField(
        initial=0,
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ],
        blank=True,
    )
    discrim_work_identity_sex = models.IntegerField(
        initial=0,
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ],
        blank=True,
    )
    discrim_work_identity_other = models.IntegerField(
        initial=0,
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ],
        blank=True,
    )
    discrim_work_pref = models.IntegerField(
        choices=[
            [0, 'Worse'],
            [1, 'Better']
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    discrim_educ = models.IntegerField(
        choices=[
            [1, 'Yes'],
            [2, 'No'],
            [3, 'Not sure']
        ],
        widget=widgets.RadioSelect
    )
    discrim_educ_identity_age = models.IntegerField(
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ],
        blank=True,
        initial=0
    )
    discrim_educ_identity_gender = models.IntegerField(
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ],
        blank=True,
        initial=0
    )
    discrim_educ_identity_race = models.IntegerField(
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ],
        blank=True,
        initial=0
    )
    discrim_educ_identity_disability = models.IntegerField(
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ],
        widget=widgets.RadioSelect,
        blank=True,
        initial=0
    )
    discrim_educ_identity_religion = models.IntegerField(
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ],
        blank=True,
        initial=0
    )
    discrim_educ_identity_sex = models.IntegerField(
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ],
        blank=True,
        initial=0
    )
    discrim_educ_identity_other = models.IntegerField(
        choices=[
            [0, 'No'],
            [1, 'Yes']
        ],
        blank=True,
        initial=0
    )
    discrim_educ_pref = models.IntegerField(
        choices=[
            [1, 'Worse'],
            [2, 'Better']
        ],
        widget=widgets.RadioSelect,
        blank=True
    )
    reason = models.LongStringField(blank=False)
    allocation_fair = models.IntegerField(
        choices = [
            [1, 'Extremely Unfair'],
            [2, 'Rather Unfair'],
            [3, 'Neither Unfair nor Fair'],
            [4, 'Rather Fair'],
            [5, 'Extremely Fair']
        ],
        widget=widgets.RadioSelect
    )
    allocation_eff = models.IntegerField(
        choices = [
            [1, 'Extremely Unjustified'],
            [2, 'Rather Unjustified'],
            [3, 'Neither Unjustified nor Justified'],
            [4, 'Rather Justified'],
            [5, 'Extremely Justified']
        ],
        widget=widgets.RadioSelect
    )
    invest_if_300 = models.IntegerField(
        blank=False,
        min=0,
        max=300
    )
    invest_if_100 = models.IntegerField(
        blank=False,
        min=0,
        max=100
    )
    invest_match_300 = models.IntegerField(
        blank=False,
        min=0,
        max=300
    )
    invest_match_100 = models.IntegerField(
        blank=False,
        min=0,
        max=100
    )
    lottery = models.IntegerField()
    feedback = models.LongStringField(blank=True)
    earning = models.FloatField()
    participation_fee = models.FloatField()
    invest_ch = models.IntegerField()

class Personal(Page):
    form_model = 'player'
    form_fields = [
        'education',
        'work_status',
        'children',
        'income',
        'ethnicity',
        'political_affil'
    ]

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=92  # You can calculate this as (page_number/total_pages)*100
        )

    def error_message(self, values):
        if values.get('children') != 1:
            return "To proceed, please select 1 for the number of children."


class Personal2(Page):
    form_model = 'player'
    form_fields = ['education_economics']

    @staticmethod
    def is_displayed(player):
        return player.education > 2

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=96  # You can calculate this as (page_number/total_pages)*100
        )


class PoliticalSocial(Page):
    form_model = 'player'
    form_fields = [
        'political_social'
    ]

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=60  # You can calculate this as (page_number/total_pages)*100
        )

class PoliticalEconomic(Page):
    form_model = 'player'
    form_fields = [
        'political_economic'
    ]

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=68  # You can calculate this as (page_number/total_pages)*100
        )

class DWork1(Page):
    form_model = 'player'
    form_fields= [
        'discrim_work',
        'discrim_work_identity_age',
        'discrim_work_identity_gender',
        'discrim_work_identity_race',
        'discrim_work_identity_disability',
        'discrim_work_identity_religion',
        'discrim_work_identity_sex',
        'discrim_work_identity_other',
        'discrim_work_pref'
    ]

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=44  # You can calculate this as (page_number/total_pages)*100
        )


class DEduc1(Page):
    form_model = 'player'
    form_fields = [
        'discrim_educ',
        'discrim_educ_identity_age',
        'discrim_educ_identity_gender',
        'discrim_educ_identity_race',
        'discrim_educ_identity_disability',
        'discrim_educ_identity_religion',
        'discrim_educ_identity_sex',
        'discrim_educ_identity_other',
        'discrim_educ_pref'
    ]

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=52  # You can calculate this as (page_number/total_pages)*100
        )


class Recall(Page):
    form_model = 'player'
    form_fields = [
        'reason'
    ]
    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=1  # You can calculate this as (page_number/total_pages)*100
        )


class Fair(Page):
    form_model = 'player'
    form_fields = [
        'allocation_fair'
    ]

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=9  # You can calculate this as (page_number/total_pages)*100
        )

class Eff(Page):
    form_model = 'player'
    form_fields = [
        'allocation_eff'
    ]

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=18  # You can calculate this as (page_number/total_pages)*100
        )

class Invest_Other_Budget300(Page):
    form_model = 'player'
    form_fields = [
        'invest_if_300'
    ]

    @staticmethod
    def is_displayed(player):
        return player.participant.receive == 0

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=28  # You can calculate this as (page_number/total_pages)*100
        )


class Invest_Other_Budget100(Page):
    form_model = 'player'
    form_fields = [
        'invest_if_100'
    ]

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=28  # You can calculate this as (page_number/total_pages)*100
        )

    @staticmethod
    def is_displayed(player):
        return player.participant.receive == 1

class Invest_Ch(Page):
    form_model = 'player'
    form_fields = ['invest_ch']

    @staticmethod
    def vars_for_template(player):
        participant = player.participant

        if participant.receive == 1:
            budget = 300
            otherbudget=100
        else:
            budget = 100
            otherbudget=300


        # If you have 10 survey pages, and this is page 3:
        return {
            'budget': budget,
            'otherbudget': otherbudget,
            'progress':32  # You can calculate this as (page_number/total_pages)*100
        }

    def error_message(self, values):
        if values.get('invest_ch') != 47:
            return "You must enter 47 to proceed."

class Invest_Match_Budget300(Page):
    form_model = 'player'
    form_fields = [
        'invest_match_300'
    ]

    @staticmethod
    def is_displayed(player):
        return player.participant.receive == 0

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=36  # You can calculate this as (page_number/total_pages)*100
        )


class Invest_Match_Budget100(Page):
    form_model = 'player'
    form_fields = [
        'invest_match_100'
    ]

    @staticmethod
    def is_displayed(player):
        return player.participant.receive == 1

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=36  # You can calculate this as (page_number/total_pages)*100
        )


class Inequality(Page):
    form_model = 'player'
    form_fields = [
        'inequality'
    ]

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=72  # You can calculate this as (page_number/total_pages)*100
        )

class Representation(Page):
    form_model = 'player'
    form_fields = [
        'representation'
    ]

    @staticmethod
    def vars_for_template(self):
        # If you have 10 survey pages, and this is page 3:
        return dict(
            progress=84  # You can calculate this as (page_number/total_pages)*100
        )


class Results(Page):
    form_model = 'player'
    form_fields = [
        'feedback'
    ]

    @staticmethod
    def vars_for_template(player):
        participant = player.participant

        inv = participant.investment
        die = participant.die

        if participant.receive == 1:
            kept = 300 - participant.investment
        else:
            kept = 100 - participant.investment

        if die < 3 :
            player.lottery = 1
            earning = math.ceil(2.5 * inv) + kept
            player.earning = earning
        else:
            player.lottery = 0
            earning = kept
            player.earning = earning

        if earning % 10 == 0:
            bonus = f"{earning / 100}0"
        else:
            bonus = f"{earning / 100}"

        if participant.receive == 1:
            participation_fee = 0
        elif participant.receive == 0:
            if participant.steal == 1:
                participation_fee = 0.75
            else:
                participation_fee = 0.5



        player.participation_fee = participation_fee

        if participation_fee == 0.5:
            participation_fee = f"{participation_fee}0"
        elif participation_fee == 1:
            participation_fee = f"{participation_fee}.00"
        else:
            participation_fee = f"{participation_fee}"

        return {
            'kept': kept,
            'inv': inv,
            'die': die,
            'earning': earning,
            'bonus': bonus,
            'participation_fee': participation_fee,
            'progress':100,

        }
class Redirect(Page):
        @staticmethod
        def js_vars(player):
            return dict(
                completionlinkfull=
                player.subsession.session.config['completionlinkfull']
            )




page_sequence = [
    Recall,
    Fair,
    Eff,
    Invest_Other_Budget300,
    Invest_Other_Budget100,
    Invest_Ch,
    Invest_Match_Budget300,
    Invest_Match_Budget100,
    DWork1,
    DEduc1,
    PoliticalSocial,
    PoliticalEconomic,
    Inequality,
    Representation,
    Personal,
    Personal2,
    Results,
    Redirect
]

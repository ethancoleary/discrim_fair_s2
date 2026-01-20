from otree.api import *
import random
import copy
from common import *

doc = """
Stage 1 Pilot
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    Quotas = {
        'T1_Klee': 1,
        'T1_Kand': 1,
        'T2_Klee': 1,
        'T2_Kand': 1,
        'T3_Klee': 1,
        'T3_Kand': 1,
        'T4_Male': 1,
        'T4_Female': 1,
        'T5_Male': 1,
        'T5_Female': 1
    }


class Subsession(BaseSubsession):
    pass

def creating_session(subsession):
    # Make a mutable copy of quotas in session.vars so we can decrement. [web:14]
    if 'quotas' not in subsession.session.vars:
        subsession.session.vars['quotas'] = copy.deepcopy(C.Quotas)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.IntegerField(initial=0)
    gender = models.IntegerField(
        choices=[
            [1, 'Female'],
            [2, 'Male'],
            [3, 'Other'],
            [4, 'Prefer not to say']
        ],
        widget=widgets.RadioSelect
    )
    age = models.IntegerField(min=0, max=100)
    KK = models.IntegerField(
        choices=[
            [1, 'Klee'],
            [2, 'Kandinsky'],
        ],
    )
    accepted = models.IntegerField()
    treatment = models.IntegerField(initial=0)
    temp_treatment = models.IntegerField(initial=0)
    die = models.IntegerField()
    invest = models.IntegerField()
    earnings = models.IntegerField()
    lottery = models.IntegerField()

    blur_log = models.LongStringField(blank=True)
    blur_count = models.IntegerField(initial=0, blank=True)
    blur_warned = models.IntegerField(initial=0, blank=True)

def decrement_quota(session, key):
    quotas = session.vars['quotas']
    if quotas.get(key, 0) <= 0:
        return False
    quotas[key] -= 1
    return True

# PAGES
class Intro(Page):
    form_model = 'player'
    form_fields = ['consent', 'blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def error_message(player, values):
        solutions = dict(consent=1)
        if values != solutions:
            return "Please consent to participation or withdraw from the experiment by closing your browser."

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }

class PDetails(Page):
    form_model = 'player'
    form_fields = ['gender', 'age', 'blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def before_next_page(player, timeout_happened):
        session = player.session
        quotas = session.vars['quotas']

        # Screen out non-binary / prefer not to say
        if player.gender > 2:
            player.accepted = 0
            player.treatment = 0
            return

        player.participant.gender  = player.gender

        # Gender-specific keys
        if player.gender == 2:
            gender_key_T4 = 'T4_Male'
            gender_key_T5 = 'T5_Male'
        else:
            gender_key_T4 = 'T4_Female'
            gender_key_T5 = 'T5_Female'

        # Build list of candidate temp treatments
        candidate_treatments = []

        # T4/T5 based on gender quotas
        if quotas.get(gender_key_T4, 0) > 0:
            candidate_treatments.append(4)
        if quotas.get(gender_key_T5, 0) > 0:
            candidate_treatments.append(5)

        # T1–T3: We check if there is *any* remaining capacity in that treatment
        # (regardless of painting) for now. Painting-specific quotas will be enforced in KK.
        for t in [1, 2, 3]:
            # if either Klee or Kand quota is positive, keep this treatment as candidate
            if quotas.get(f'T{t}_Klee', 0) > 0 or quotas.get(f'T{t}_Kand', 0) > 0:
                candidate_treatments.append(t)

        if not candidate_treatments:
            # no available quota anywhere -> screen out
            player.accepted = 0
            player.treatment = 0
            return

        # Randomly choose a temp treatment from feasible ones
        temp_treat = random.choice(candidate_treatments)
        player.temp_treatment = temp_treat

        # If temp_treatment is T4 or T5, finalize immediately and decrement gender quota
        if temp_treat == 4:
            key = gender_key_T4
            if not decrement_quota(session, key):
                # no quota after all -> screen out
                player.accepted = 0
                player.treatment = 0
            else:
                player.treatment = 4
                player.accepted = 1
                player.participant.treatment = 4
        elif temp_treat == 5:
            key = gender_key_T5
            if not decrement_quota(session, key):
                player.accepted = 0
                player.treatment = 0
            else:
                player.treatment = 5
                player.accepted = 1
                player.participant.treatment = 5
        else:
            # T1–T3: treatment only finalized after KK (painting choice).
            player.accepted = 1  # still “in” for now

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }


class KK(Page):
    form_model = 'player'
    form_fields = ['KK', 'blur_count', 'blur_log', 'blur_warned']

    @staticmethod
    def is_displayed(player):
        # Show only if: not screened out, and temp_treatment in {1,2,3}
        return player.accepted == 1 and player.treatment == 0 and player.temp_treatment in [1, 2, 3]

    @staticmethod
    def before_next_page(player, timeout_happened):
        session = player.session
        quotas = session.vars['quotas']

        player.participant.painting = player.KK

        # Determine painting key for quotas
        if player.KK == 1:
            painting_suffix = 'Klee'
        else:
            painting_suffix = 'Kand'

        # Find which of T1–T3 still have capacity for this painting
        available_treatments = []
        for t in [1, 2, 3]:
            key = f'T{t}_{painting_suffix}'
            if quotas.get(key, 0) > 0:
                available_treatments.append((t, key))

        if not available_treatments:
            # No quota left for this painting in T1–T3 -> screen out
            player.accepted = 0
            player.treatment = 0
            return

        # Randomly select one of the treatments that has quota for this painting
        t, key = random.choice(available_treatments)
        success = decrement_quota(session, key)
        if not success:
            # Extremely rare race condition; just screen out to be safe
            player.accepted = 0
            player.treatment = 0
        else:
            player.treatment = t
            player.accepted = 1
            player.participant.treatment = t

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }

class InvestIntro(Page):

    @staticmethod
    def is_displayed(player):
        return player.accepted == 0 and player.gender > 2

class Invest(Page):
    form_model = 'player'
    form_fields = ['invest']

    @staticmethod
    def is_displayed(player):
        return player.accepted == 0 and player.gender > 2

    @staticmethod
    def before_next_page(player, timeout_happened):
        die = random.randint(1, 6)
        player.die = die

        if die < 3:
            player.lottery = 1
            player.earnings = 2.5 * player.invest + (200 - player.invest)
        elif die > 2:
            player.lottery = 0
            player.earnings = (200 - player.invest)

class Screen(Page):

    @staticmethod
    def is_displayed(player):
        return player.accepted == 0 and player.gender < 3

class Results(Page):

    @staticmethod
    def vars_for_template(player):
        kept = 200 - player.invest
        if player.earnings % 10 == 0:
            bonus = f"{player.earnings / 100}0"
        else:
            bonus = f"{player.earnings / 100}"

        return {
            'kept': kept,
            'bonus': bonus
        }


    @staticmethod
    def is_displayed(player):
        return player.accepted == 0 and player.gender > 2

class Redirect_G(Page):

    @staticmethod
    def is_displayed(player):
        return player.accepted == 0 and player.gender > 2

    @staticmethod
    def js_vars(player):
        return dict(
            completionlinkscreenout_invest=
            player.subsession.session.config['completionlinkscreenout_invest']
        )

class Redirect_S(Page):

    @staticmethod
    def is_displayed(player):
        return player.accepted == 0 and player.gender < 3

    @staticmethod
    def js_vars(player):
        return dict(
            completionlinkscreenout_invest=
            player.subsession.session.config['completionlinkscreenout_invest']
        )


page_sequence = [
                Intro,
                PDetails,
                KK,
                InvestIntro,
                Invest,
                Screen,
                Results,
                Redirect_G,
                Redirect_S
                ]

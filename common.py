# common.py
from otree.api import Page
from otree.api import models
import json


class MyBasePage(Page):
    form_model = 'player'
    form_fields = ['blur_log', 'blur_count', 'blur_warned']

    @staticmethod
    def vars_for_template(player):
        return {
            'hidden_fields': ['blur_log', 'blur_count', 'blur_warned'],
        }

    @staticmethod
    def before_next_page(player, timeout_happened=False):
        blob = player.blur_log or '[]'
        try:
            page_list = json.loads(blob)
        except json.JSONDecodeError:
            page_list = []

        # aggregate into a dict of counts
        page_counts = {}
        for key in page_list:
            page_counts[key] = page_counts.get(key, 0) + 1

        blur_log = player.participant.vars.get('Blur_log', {})
        for page_name, count in page_counts.items():
            blur_log[page_name] = blur_log.get(page_name, 0) + count

        player.participant.vars['Blur_log'] = blur_log
        player.participant.vars['Blur_count'] = (
                player.participant.vars.get('Blur_count', 0)
                + (player.blur_count or 0)
        )

        if player.blur_warned:
            player.participant.vars['Blur_warned'] = 1
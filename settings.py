from os import environ

SESSION_CONFIGS = [
    dict(
        name='Main',
        app_sequence=[
            'intro',
            'task',
            'outro'
        ],
        num_demo_participants=10,
completionlinkfull  =
       'https://app.prolific.com/submissions/complete?cc=CHXPJ2PR',
completionlinkscreenout_invest =
        'https://app.prolific.com/submissions/complete?cc=CE0YPA75',
completionlinkscreenout  =
       'https://app.prolific.com/submissions/complete?cc=CE0YPA75',
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [
    'female',
    'group',
    'gender',
    'treatment',
    'painting',
    'chosen',
    'investment',
    'die',
    'steal',
    'group_treatment_id',
    'male'
]
SESSION_FIELDS = []
ROOMS = [
    dict(
        name='tee',
        display_name='tee',
        # participant_label_file='_rooms/your_study.txt',
        # use_secure_urls=True,
    ),
    dict(
        name='prol_tee',
        display_name='prol_tee',
        # participant_label_file='_rooms/your_study.txt',
        # use_secure_urls=True,
    ),
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'bergen2025'

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5543930954479'

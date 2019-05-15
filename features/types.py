from behave import register_type
import parse
from datetime import timedelta


@parse.with_pattern(r'client|administrateur')
def parse_user_type(text):
    return text


register_type(UserType=parse_user_type)


@parse.with_pattern(r'Consommateur|Producteur|Responsable|Rex|Softozor')
def parse_persona_type(text):
    return text


register_type(PersonaType=parse_persona_type)


@parse.with_pattern(r'valides|invalides')
def parse_user_credentials_validity(validity):
    return validity == 'valides'


register_type(ValidityType=parse_user_credentials_validity)


@parse.with_pattern(r'actif|inactif')
def parse_user_activity(activity):
    return activity == 'actif'


register_type(ActivityType=parse_user_activity)


@parse.with_pattern(r'avec|sans')
def parse_with_or_without(with_or_without):
    return with_or_without == 'avec'


register_type(WithOrWithoutType=parse_with_or_without)


def unit_to_seconds(unit):
    switch = {
        'secondes': 1,
        'seconde': 1,
        'minutes': timedelta(minutes=1),
        'minute': timedelta(minutes=1),
        'heures': timedelta(hours=1),
        'heure': timedelta(hours=1),
        'jours': timedelta(days=1),
        'jour': timedelta(days=1),
        'semaines': timedelta(weeks=1),
        'semaine': timedelta(weeks=1),
        'mois': timedelta(days=30),
        'ans': timedelta(days=360),
        'an': timedelta(days=360)
    }
    return switch[unit].total_seconds()


@parse.with_pattern(r'secondes?|minutes?|heures?|jours?|semaines?|mois|ans?')
def parse_duration_unit(unit):
    return unit_to_seconds(unit)


register_type(DurationInSecondsType=parse_duration_unit)

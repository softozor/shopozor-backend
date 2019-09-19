# Generated by Django 2.2.3 on 2019-09-19 09:46

from django.db import migrations, models
from django.conf import settings
from django_prices_vatlayer import utils


def add_initial_vat_rates(apps, schema_editor):
    if hasattr(settings, 'ACCEPTANCE_TESTING'):
        # in the case of acceptance testing, the permissions are
        # set as fixtures; after every scenario, those permissions
        # are cleared up
        # would we set them here up, they would just be gone after the
        # first test
        return

    rates = {
        'success': True,
        'rates': {
            'CH': {
                'country_name': 'Switzerland',
                'standard_rate': 7.7,
                'reduced_rates': {
                    'reduced': 2.5,
                    'special': 3.7
                }
            }
        }
    }
    utils.create_objects_from_json(rates)


def add_initial_vat_rate_types(apps, schema_editor):
    if hasattr(settings, 'ACCEPTANCE_TESTING'):
        # in the case of acceptance testing, the permissions are
        # set as fixtures; after every scenario, those permissions
        # are cleared up
        # would we set them here up, they would just be gone after the
        # first test
        return

    rate_types = {'success': True, 'types': ['reduced', 'special']}
    utils.save_vat_rate_types(rate_types)


class Migration(migrations.Migration):

    dependencies = [
        ('shopozor', '0009_staff_description'),
    ]

    operations = [
        migrations.RunPython(add_initial_vat_rates),
        migrations.RunPython(add_initial_vat_rate_types)
    ]

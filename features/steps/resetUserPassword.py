from behave import given, then, when
from datetime import datetime
from datetime import timedelta
from saleor.account.models import User


@when(u'il active son compte avec un mot de passe non conforme au plus tard {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    elapsed_time_since_email_reception_in_seconds = (datetime.now() - context.email_reception_time).total_seconds()
    context.test.assertTrue(elapsed_time_since_email_reception_in_seconds < expiration_delta_in_seconds)
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    password = 'abdc'
    activate_account(context, uidb64, token, password)


@then(u'son mot de passe reste inchangé')
def step_impl(context):
    user = User.objects.filter(email=context.unknown['email'])
    context.test.assertEqual(user.password, context.current_encrypted_password)


# probably not needed anymore:
# @then(u'son compte est supprimé')
# def step_impl(context):
#     context.test.assertEqual(User.objects.filter(email=context.unknown['email']).count(), 0)
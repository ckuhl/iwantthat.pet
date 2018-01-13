import os

import requests
import jinja2

from .SECRETS import SECRETS


def render(template, context):
    """
    Render a jinja2 template for an email
    """
    EMAIL_TEMPLATES = os.path.join('templates', 'email')
    return jinja2.Environment(
                    loader=jinja2.FileSystemLoader(EMAIL_TEMPLATES)
                        ).get_template(template).render(context)

def send(to, subject, text):
    """
    Send a parameterized email
    """
    domain = SECRETS.MAIL_DOMAIN
    auth_data = ('api', SECRETS.API_KEY)
    message_data = {
            'from': 'IWantThat.Pet <noreply@mail.iwantthat.pet>',
            'to': [to],
            'subject': subject,
            'text': text
    }
    return requests.post(domain, auth=auth_data, data=message_data)

def send_sub_confirmation(to, pet):
    """
    Send an email to confirm a persons subscription
    """
    subject = 'Your subscription to %s' % pet
    content = render('sub_confirmation.j2',
            {'link': 'https://iwanthatpet.com/api/verify/%s' % to})
    return send(to, subject, content)

def send_unsub_confirmation(to, pet):
    """
    Send an email to confirm a person has unsubscribed
    """
    subject = 'Successful unsubscription'
    content = render('unsub_confirmation.j2', {'email': to})
    return send(to, subject, content)

def send_adoption_notice(to, pet):
    """
    Send a notification that an animal has been delisted (i.e. adopted)
    """
    subject = '%s has been adopted' % pet
    content = render('adoption.j2', {'animal': pet})
    return send(to, subject, content)


# XXX: Send monthly update if an animal _isn't_ adopted?


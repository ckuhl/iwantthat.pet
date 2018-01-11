import requests

from .SECRETS import SECRETS


def send_email(sender, to, subject, text):
    """
    Send a parameterized email
    """
    domain = SECRETS.MAIL_DOMAIN
    auth_data = ('api', SECRETS.API_KEY)
    message_data = {
            "from": sender,
            "to": [to],
            "subject": subject,
            "text": text
    }

    return requests.post(domain, auth=auth_data, data=message_data)


def send_subscribe_email(to, pet):
    """
    Send an email to confirm a persons subscription
    """
    sender = "noreply@mail.iwantthat.pet"
    subject = "Your subscription to " + pet
    content = "To make sure that you get updates, please verify your email"
    content += "by clicking this link:" + '\n\n'
    content += "https://iwantthat.pet/api/verify/" + to + '/'
    return send_email(sender, to, subject, content)


def send_unsubscribe_email(to, pet):
    """
    Send an email to confirm a person has unsubscribed
    """
    sender = "noreply@mail.iwantthat.pet"
    subject = "You have unsubscribed from updates about " + pet
    content = pet + " is sorry to see you go!"
    return send_email(sender, to, subject, content)

def send_adopted_email(to, pet):
    """
    Send a notification that an animal has been delisted (i.e. adopted)
    """
    sender = "noreply@mail.iwantthat.pet"
    subject = pet + " has been adopted"
    content = "Good news! " + pet + " has been adopted!"
    return send_email(sender, to, subject, content)


# XXX: Send monthly update if an animal _isn't_ adopted?


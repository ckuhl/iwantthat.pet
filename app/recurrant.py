import time

from . import models, email, scrape
from .models import Database, Animal, Subscriber, Subscription


def update():
    for i in (Subscription.select()):
        if i.sub_id.verified:
            p = scrape.get_animal_page(i.animal_id.rspca_id)
            if scrape.is_adopted(p):
                email.send_adoption_notice(i.sub_id.email, i.animal_id.name)
                with Database.transaction():
                    i.delete()
            else:
                pass
            # Wait so we don't DDOS them
            time.sleep(0.25)


from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request
from werkzeug.exceptions import abort

from app import mail, recurrant, scrape
from app.models import Database, Subscriber, Animal, Subscription

def create_app():
    app = Flask(__name__)

    Database.create_tables([Subscriber, Animal, Subscription], safe=True)

    scheduler = BackgroundScheduler(timezone='America/Toronto')
    scheduler.add_job(recurrant.update, 'interval', days=1)

    @app.route('/')
    def root():
        return render_template('main.j2')

    @app.route('/animal/<int:animal_id>')
    def animal(animal_id):
        p = scrape.get_animal_page(animal_id)
        p = bytes.decode(p)
        if scrape.is_animal_adopted(p):
            abort(404)
        else:
            name = scrape.get_name(p)
        return render_template('animal.j2', animal_name=name)


    # API ========================================================================

    @app.route('/api/subscribe', methods = ['POST'])
    def subscribe_animal():
        form_data = request.form.to_dict()
        email_addr = form_data['email']
        rspca_num = form_data['ic-current-url'][8:]
        animal_name = form_data['name']

        with Database.transaction():
            s = Subscriber.get_or_create(email=email_addr, verified=False)
            a = Animal.get_or_create(rspca_id=rspca_num, name=animal_name)
            Subscription.get_or_create(
                    sub_id = s[0].sub_id,
                    animal_id = a[0].animal_id)

        mail.send_subscribe_email(email_addr, animal_name)
        return "We'll keep you posted!"


    @app.route('/api/unsubscribe', methods = ['POST'])
    def unsubscribe_email():
        form_data = request.form.to_dict()

        # TODO

        return form_data['email']

    @app.route('/api/verify/<string:email>', methods = ['POST'])
    def verify_email(em):
        Subscriber.update(verified=True).where(Subscriber.email == em)
        return "You're verified!"


    # Error ======================================================================

    @app.errorhandler(404)
    def page_not_found(e):
            return render_template('404.j2'), 404


    # Run ========================================================================

    scheduler.start()

    return app

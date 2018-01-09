from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def root():
    return render_template('main.j2')

@app.route('/animal/<int:animal_id>')
def animal(animal_id):
    return render_template('animal.j2', context={animal_id: animal_id})


# API ========================================================================

@app.route('/api/subscribe', methods = ['POST'])
def subscribe_animal():
    form_data = request.form.to_dict()
    return form_data['email']

@app.route('/api/unsubscribe', methods = ['POST'])
def unsubscribe_email():
    form_data = request.form.to_dict()
    return form_data['email']

@app.route('/api/verify', methods = ['POST'])
def verify_email():
    return "All good"


# Error ======================================================================

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.j2'), 404


# Run ========================================================================

if __name__ == '__main__':
    app.run()


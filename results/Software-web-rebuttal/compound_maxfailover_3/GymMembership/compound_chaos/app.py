from flask import Flask, render_template, redirect, url_for, abort
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

DATA_DIR = 'data'

# --- Data loading helpers ---
def load_memberships():
    '''Load all memberships from memberships.txt.'''
    memberships = []
    path = os.path.join(DATA_DIR, 'memberships.txt')
    if not os.path.exists(path):
        return memberships
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Format: membership_id|plan_name|price|billing_cycle|features|max_classes
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                membership_id_str, plan_name, price_str, billing_cycle, features_str, max_classes_str = parts
                try:
                    membership_id = int(membership_id_str)
                    price = float(price_str)
                    max_classes = int(max_classes_str)
                    features = [feat.strip() for feat in features_str.split(',') if feat.strip()] if features_str else []
                except ValueError:
                    continue
                memberships.append({
                    'membership_id': membership_id,
                    'plan_name': plan_name,
                    'price': price,
                    'billing_cycle': billing_cycle,
                    'features': features,
                    'max_classes': max_classes,
                })
    except Exception:
        # Fail silently and return empty list if reading or parsing fails
        pass
    return memberships


def load_trainers():
    '''Load all trainers from trainers.txt.'''
    trainers = []
    path = os.path.join(DATA_DIR, 'trainers.txt')
    if not os.path.exists(path):
        return trainers
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Format:
                # trainer_id|name|specialty|certifications(comma-separated)|experience_years|bio
                parts = line.split('|')
                if len(parts) != 6:
                    continue
                trainer_id_str, name, specialty, certs_str, exp_years_str, bio = parts
                try:
                    trainer_id = int(trainer_id_str)
                    experience_years = int(exp_years_str)
                    certifications = [cert.strip() for cert in certs_str.split(',') if cert.strip()] if certs_str else []
                except ValueError:
                    continue
                trainers.append({
                    'trainer_id': trainer_id,
                    'name': name,
                    'specialty': specialty,
                    'certifications': certifications,
                    'experience_years': experience_years,
                    'bio': bio,
                })
    except Exception:
        pass
    return trainers


@app.route('/')
def root():
    # Root redirects exactly to dashboard
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    # Show the dashboard page with all memberships and trainers
    memberships = load_memberships()
    trainers = load_trainers()
    # Render 'dashboard.html' with context:
    # - memberships: list of dicts
    # - trainers: list of dicts
    return render_template('dashboard.html', memberships=memberships, trainers=trainers)


@app.route('/memberships')
def memberships():
    # Show memberships listing page
    memberships = load_memberships()
    return render_template('memberships.html', memberships=memberships)


@app.route('/plan/<int:plan_id>')
def plan_details(plan_id):
    # Show details for a single plan with given plan_id
    memberships = load_memberships()
    trainers = load_trainers()

    # Find plan by id
    plan = None
    for m in memberships:
        if m['membership_id'] == plan_id:
            plan = m
            break

    if plan is None:
        abort(404)

    # Compose a comma-separated string of all trainer names
    trainers_names = ', '.join(t['name'] for t in trainers)

    # Render 'plan_details.html' with:
    # - plan: dict of the membership
    # - trainers: comma-separated string of trainer names
    return render_template('plan_details.html', plan=plan, trainers=trainers_names)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

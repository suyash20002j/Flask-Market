from Market import app
from flask import render_template, redirect, url_for, flash, request
from Market.models import Item, User
from Market.forms import RegisterForm,LoginForm, PurchaseItemForm, SellItemForm
from Market import db
from flask_login import login_user, login_required, logout_user, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")

@app.route('/market', methods = ["GET", "POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations You purchased {p_item_object.name} for price {p_item_object.price} Rs.!", category="success")
            else:
                flash(f"Unfortunately you don't have enough money to purchase {p_item_object.name}", category="danger")
        
        # Selling Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations You sold {s_item_object.name} back to Market!", category="success")
            else:
                flash(f"Unfortunately something went wrong with {s_item_object.name}", category="danger")
        
        return redirect(url_for('market_page'))
    
    if request.method == "GET":          
        items = Item.query.filter_by(owner = None)
        owned_items = Item.query.filter_by(owner = current_user.id)
        return render_template("market.html", items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/register', methods = ['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data, 
                              email_address = form.email_address.data,
                              password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account is created succesfully. You have logged in as {user_to_create.username}", category="success")
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors:
            flash(f"There was error in submitting form : {err_msg}", category='danger')
    return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            login_user(attempted_user)
            flash(f"You are logged in with the username {attempted_user.username}",category='success')
            return redirect(url_for('market_page'))
        else:
            flash("Username and Password do not match! Please Try Again.", category='danger')
    return render_template('login.html',form = form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have logged out", category='info')
    return redirect(url_for('home_page'))
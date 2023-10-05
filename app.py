from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\Khushi Sharma\\Desktop\\MovieTicketBooking\\bookmovie.db'
db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(80), nullable=False, primary_key=True)
    password = db.Column(db.String(120), nullable=False)

class Admin(db.Model):
    admin_username = db.Column(db.String(80), nullable=False, primary_key=True)
    admin_password = db.Column(db.String(120), nullable=False)
    
class Venue(db.Model):
    venue_name = db.Column(db.String(80), nullable=False, primary_key=True)
    venue_place = db.Column(db.String(120), nullable=False)
    venue_location = db.Column(db.String(80), nullable=False)
    venue_capacity = db.Column(db.Integer, nullable=False)
    admin_rel = db.Column(db.String(80), db.ForeignKey("admin.admin_username"), nullable=False)
    
class Show(db.Model):
    show_id = db.Column(db.Integer, nullable=False, primary_key=True)
    show_name = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    timing = db.Column(db.String(80), nullable=False)
    tag = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    reserved_seats = db.Column(db.Integer)
    venue_rel = db.Column(db.String(80), db.ForeignKey("venue.venue_name"), nullable=False)
    
class Booking(db.Model):
    booking_id = db.Column(db.Integer, nullable=False, primary_key=True)
    seats = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(80), db.ForeignKey("user.username"), nullable=False)
    show_name = db.Column(db.String(80), nullable=False)
    show_id = db.Column(db.String(80), db.ForeignKey("show.show_id"), nullable=False)
    show_timings = db.Column(db.String(80), nullable=False)
    venue_name = db.Column(db.String(80), db.ForeignKey("venue.venue_name"), nullable=False)

# editing the show

@app.route('/<admin>/<venue_name>/<show_id>/edit_show', methods=['GET', 'POST'])
def Edit_Show(admin, venue_name, show_id):
    show = Show.query.filter_by(show_id=show_id).first()
    if request.method == 'POST':
        show.show_name = request.form['name']
        show.rating = request.form['rating']
        show.timing = request.form['timings']
        show.tag = request.form['tags']
        show.price = request.form['price']
        db.session.commit()
        return redirect(url_for('Show_Venue', admin=admin, venue_name=venue_name))
    return render_template('Edit_Show.html', admin=admin, venue_name=venue_name, show=show)

# deleting the show after the confirmation from the admin

@app.route('/<admin>/<venue_name>/<show_id>/delete_show')
def Delete_Show(admin, venue_name, show_id):
    show = Show.query.filter_by(show_id=show_id).first()
    db.session.delete(show)
    db.session.commit()
    return redirect(url_for('Show_Venue', admin=admin, venue_name=venue_name))

# adding the show

@app.route('/<admin>/<venue_name>/add_show', methods=['GET', 'POST'])
def Add_Show(admin, venue_name):
    if request.method == 'POST':
        name = request.form['name']
        rating = request.form['rating']
        timings = request.form['timings']
        tags = request.form['tags']
        price = request.form['price']
        show = Show(show_name=name, rating=rating, timing=timings, tag=tags, price=price, reserved_seats=0, venue_rel=venue_name)
        db.session.add(show)
        db.session.commit()
        return redirect(url_for('Show_Venue', admin=admin, venue_name=venue_name))
    return render_template('Add_Show.html', admin=admin, venue_name=venue_name)

# Viewing a venue

@app.route('/<admin>/<venue_name>/show_venue')
def Show_Venue(admin, venue_name):
    venue = Venue.query.filter_by(venue_name=venue_name).first()
    shows = Show.query.filter_by(venue_rel=venue_name).all()
    return render_template("Show_Venue.html", admin=admin, venue=venue, shows=shows)

# editing the venue

@app.route('/<admin>/<venue_name>/edit_venue', methods=['GET', 'POST'])
def Edit_Venue(admin, venue_name):
    venue = Venue.query.filter_by(venue_name=venue_name).first()
    if request.method == 'POST':
        venue.venue_name = request.form['name']
        venue.venue_place = request.form['place']
        venue.venue_location = request.form['location']
        venue.venue_capacity = request.form['capacity']
        db.session.commit()
        return redirect(url_for('Admin_Dashboard', admin=admin))
    return render_template('Edit_Venue.html', admin=admin, venue=venue)

# deleting the venue after confirmation from the admin

@app.route('/<admin>/<venue_name>/delete_venue')
def Delete_Venue(admin, venue_name):
    venue = Venue.query.filter_by(venue_name=venue_name).first()
    db.session.delete(venue)
    db.session.commit()
    return redirect(url_for('Admin_Dashboard', admin=admin))

# adding a venue
    
@app.route('/<admin>/add_venue', methods=['GET', 'POST'])
def Add_Venue(admin):
    if request.method == 'POST':
        name = request.form['name']
        place = request.form['place']
        location = request.form['location']
        capacity = request.form['capacity']
        venue = Venue(venue_name=name, venue_place=place, venue_location=location, venue_capacity=capacity, admin_rel=admin)
        db.session.add(venue)
        db.session.commit()
        return redirect(url_for('Admin_Dashboard', admin=admin))
    return render_template('Add_Venue.html', admin=admin)

# search option for the admin

@app.route('/<admin>/admin_search', methods=['POST'])
def Admin_Search(admin):
    parameter = request.form['parameters']
    value = request.form['Value']
    if parameter == 'location':
        venues = Venue.query.filter(Venue.venue_location.like('%{}%'.format(value))).all()
        return render_template("Admin_Dashboard.html", admin=admin, venues=venues)
    elif parameter == 'name':
        venues = Venue.query.filter(Venue.venue_name.like('%{}%'.format(value))).all()
        return render_template("Admin_Dashboard.html", admin=admin, venues=venues)
    else :
        venues = Venue.query.filter(Venue.venue_capacity >= value).all()
        return render_template("Admin_Dashboard.html", admin=admin, venues=venues)

# dashboard for the admin

@app.route('/<admin>/Admin_Dashboard', methods=['GET', 'POST'])
def Admin_Dashboard(admin):
    venues = Venue.query.all()
    return render_template('Admin_Dashboard.html', admin=admin, venues=venues)

# admin login

@app.route('/Admin', methods=['GET', 'POST'])
def Admin_Login():
    if request.method == 'POST':
        admin_username = request.form['Admin']
        admin_password = request.form['Admin_Password']
        query = Admin.query.filter(Admin.admin_username==admin_username, Admin.admin_password==admin_password)
        admin = query.first()
        if admin:
            return redirect(url_for('Admin_Dashboard', admin=admin_username))
        else:
            return render_template('Admin_Login.html', error="Incorrect Username or Password")
    return render_template('Admin_Login.html')

# admin logout

@app.route('/admin_logout')
def Admin_Logout():
    return redirect(url_for('Admin_Login'))

# home view of the venue for the user

@app.route('/<username>/<venue_name>/home_view')
def Home_View(username, venue_name):
    shows = Show.query.filter_by(venue_rel=venue_name).all()
    show_ids=[]
    for i in range(len(shows)):
        show_timings = shows[i].timing
        time_str = show_timings[:5]
        time_object = datetime.strptime(time_str, '%H:%M')
        curr_time = datetime.now()
        curr_time = str(curr_time)
        curr_time = datetime.strptime(curr_time[11:16], "%H:%M")
        if curr_time <= time_object:
            show_ids.append(shows[i].show_id)
        avail_shows = Show.query.filter(Show.show_id.in_(show_ids)).all()
    return render_template("Home_View.html", username=username, venue_name=venue_name, shows=avail_shows)
    

# search option for the user

@app.route('/<username>/user_search', methods=['POST'])
def User_Search(username):
    parameter = request.form['parameters']
    value = request.form['Value']
    if parameter == 'location':
        venues = Venue.query.filter(Venue.venue_location.like('%{}%'.format(value))).all()
        return render_template("User_Search.html", username=username, venues=venues)
    else:
        if parameter == 'show_name':
            shows = Show.query.filter(Show.show_name.like('%{}%'.format(value))).all()
        elif parameter == 'tag':
            shows = Show.query.filter(Show.tag.like('%{}%'.format(value))).all()          
        elif parameter == 'price':
            shows = Show.query.filter(Show.price <= value).all()
        else :
            shows = Show.query.filter(Show.rating >= value).all()
        show_ids=[]
        for i in range(len(shows)):
            show_timings = shows[i].timing
            time_str = show_timings[:5]
            time_object = datetime.strptime(time_str, '%H:%M')
            curr_time = datetime.now()
            curr_time = str(curr_time)
            curr_time = datetime.strptime(curr_time[11:16], "%H:%M")
            if curr_time <= time_object:
                show_ids.append(shows[i].show_id)
            avail_shows = Show.query.filter(Show.show_id.in_(show_ids)).all()
        return render_template("User_Dashboard.html", username=username, shows=avail_shows)
        
    
# previous bookings of the user
           
@app.route('/<username>/bookings')
def Bookings(username):
    bookings = Booking.query.filter_by(username=username).all()
    return render_template("Bookings.html", username=username, bookings=bookings)

# booking tickets
    
@app.route('/<username>/<venue_name>/<show_id>/book_tickets', methods=['GET', 'POST'])
def Book_Tickets(username, venue_name, show_id):
    show = Show.query.filter_by(show_id=show_id).first()
    venue = Venue.query.filter_by(venue_name=venue_name).first()
    available_seats = venue.venue_capacity - show.reserved_seats
    reserved_seats_old = show.reserved_seats
    if request.method == "POST":
        tickets = request.form['tickets']
        if available_seats > int(tickets):
            show.reserved_seats = int(tickets) + reserved_seats_old
            db.session.commit()
            booking = Booking(seats=tickets, username=username, show_id=show_id, show_name=show.show_name, show_timings=show.timing, venue_name=venue_name)
            db.session.add(booking)
            db.session.commit()
            return redirect(url_for("Bookings", username=username))
        else:
            return render_template("Book_Tickets.html", error="Insufficient Available Tickets", username=username)
            
    return render_template("Book_Tickets.html", username=username, show=show, available_seats=available_seats)

#user dashboard

@app.route('/<username>/user_dashboard')
def User_Dashboard(username):
    all_shows = Show.query.all()
    show_ids=[]
    for i in range(len(all_shows)):
        show_timings = all_shows[i].timing
        time_str = show_timings[:5]
        time_object = datetime.strptime(time_str, '%H:%M')
        curr_time = datetime.now()
        curr_time = str(curr_time)
        curr_time = datetime.strptime(curr_time[11:16], "%H:%M")
        if curr_time <= time_object:
            show_ids.append(all_shows[i].show_id)
    shows = Show.query.filter(Show.show_id.in_(show_ids)).all()
    return render_template("User_Dashboard.html", username=username, shows=shows)

# user signup

@app.route('/signup', methods=['GET', 'POST'])
def User_Signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        query = User.query.filter(User.username==username, User.password==password)
        user = query.first()
        if user:
            msg = 'Account already exists !'
        elif not username or not password:
            msg = 'Please fill out the form !'
        elif len(password) < 6:
            msg = 'Password not long enough !'
        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('User_Signup.html', msg = msg)

# user login

@app.route('/', methods=['GET', 'POST'])
def User_Login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = User.query.filter(User.username==username, User.password==password)
        user = query.first()
        if user:
            return redirect(url_for('User_Dashboard', username=username))
        else:
            return render_template('User_Login.html', error="Incorrect Username or Password")
    return render_template('User_Login.html')

# user logout

@app.route('/user_logout')
def User_Logout():
    return redirect(url_for('User_Login'))
   
if __name__ == "__main__":
    app.run(debug=True)
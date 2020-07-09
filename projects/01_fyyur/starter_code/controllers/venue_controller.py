#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import render_template, request, Response, flash, redirect, url_for
from flask_wtf import Form
from forms import *
from db_data_models import *
from datetime import datetime

#----------------------------------------------------------------------------#
#  Venues
#  ----------------------------------------------------------------


@app.route('/venues')
def venues():
    data = []
    venues = Venue.query.all()

    for venue in venues:
        data.append({
            "city": venue.city,
            "state": venue.state,
            "venues": [{
                "id": venue.id,
                "name": venue.name
            }]
        })
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    data = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

    result = []
    for venue in data:
        result.append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(Show.query.filter(Show.venue_id == venue.id).filter(Show.start_time > datetime.now()).all())
        })
    response = {
        "count": len(data),
        "data": result
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_term)


#  Venue Details
#  ----------------------------------------------------------------

@ app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    selected_venue = Venue.query.get(venue_id)
    upcoming_shows = selected_venue.venues_show.filter(
        Show.start_time >= datetime.now()).all()

    past_shows = selected_venue.venues_show.filter(
        Show.start_time < datetime.now()).all()

    data = {
        "id": selected_venue.id,
        "name": selected_venue.name,
        "genres": selected_venue.genres,
        "address": selected_venue.address,
        "city": selected_venue.city,
        "state": selected_venue.state,
        "phone": selected_venue.phone,
        "website": selected_venue.website,
        "facebook_link": selected_venue.facebook_link,
        "seeking_talent": selected_venue.seeking_talent,
        "seeking_description": selected_venue.seeking_description,
        "image_link": selected_venue.image_link,
        "upcoming_shows": upcoming_shows,
        "upcoming_shows_count": len(upcoming_shows),
        "past_shows": past_shows,
        "past_shows_count": len(past_shows),

    }
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    try:
        seeking_talent = False
        seeking_description = ''
        if 'seeking_talent' in request.form:
            seeking_talent = form.seeking_talent.data == 'y'
        if 'seeking_description' in request.form:
            seeking_description = form.seeking_description.data

        venue = Venue(
            name=form.name.data,
            genres=form.genres.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            address=form.address.data,
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data,
            website=form.website.data,
            seeking_talent=seeking_talent,
            seeking_description=seeking_description
        )
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + venue.name + ' was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    selected_venue = Venue.query.get(venue_id)
    form.name.data = selected_venue.name
    form.address.data = selected_venue.address
    form.genres.data = selected_venue.genres
    form.city.data = selected_venue.city
    form.state.data = selected_venue.state
    form.phone.data = selected_venue.phone
    form.facebook_link.data = selected_venue.facebook_link
    form.image_link.data = selected_venue.image_link
    form.website.data = selected_venue.website
    form.seeking_talent.data = selected_venue.seeking_talent
    form.seeking_description.data = selected_venue.seeking_description

    venue = {
        "id": selected_venue.id,
        "name": selected_venue.name,
        "address": selected_venue.address,
        "genres": selected_venue.genres,
        "city": selected_venue.city,
        "state": selected_venue.state,
        "phone": selected_venue.phone,
        "website": selected_venue.website,
        "facebook_link": selected_venue.facebook_link,
        "seeking_venue": selected_venue.seeking_talent,
        "seeking_description": selected_venue.seeking_description,
        "image_link": selected_venue.image_link,
    }
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)

    try:
        form = VenueForm(request.form)

        seeking_talent = False
        seeking_description = ''
        if 'seeking_talent' in request.form:
            seeking_talent = form.seeking_talent.data == 'y'
        if 'seeking_description' in request.form:
            seeking_description = form.seeking_description.data

        venue.name = form.name.data
        venue.address = form.address.data
        venue.genres = form.genres.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        venue.facebook_link = form.facebook_link.data
        venue.image_link = form.image_link.data
        venue.website = form.website.data
        venue.seeking_talent = seeking_talent
        venue.seeking_description = seeking_description

        db.session.commit()
        flash('Venue ' + venue.name + ' was successfully edited!')

    except:
        db.session.rollback()
        flash('An error occurred. Venue ' +
              venue.name + ' could not be edited.')
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

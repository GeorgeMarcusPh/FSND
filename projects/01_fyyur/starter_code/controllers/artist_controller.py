#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_wtf import Form
from forms import *
from db_data_models import *

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    data = []
    artists = Artist.query.all()

    for artist in artists:
        artist = dict(zip(('id', 'name'), (artist.id, artist.name)))
        data.append(artist)
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    response = {
        "count": len(result),
        "data": result
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)

#  Artist Details
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    selected_artist = Artist.query.get(artist_id)

    upcoming_shows = selected_artist.artist_show.filter(
        Show.start_time >= datetime.now()).all()

    past_shows = selected_artist.artist_show.filter(
        Show.start_time < datetime.now()).all()

    data = selected_artist.map_artist_to_dict()

    data["past_shows"] = past_shows
    data["upcoming_shows"] = upcoming_shows
    data["past_shows_count"] = len(past_shows)
    data["upcoming_shows_count"] = len(upcoming_shows)

    return render_template('pages/show_artist.html', artist=data)

#  Create
#  ----------------------------------------------------------------


@ app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@ app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()
    try:
        seeking_venue = False
        seeking_description = ''
        if 'seeking_venue' in request.form:
            seeking_venue = form.seeking_venue.data
        if 'seeking_description' in request.form:
            seeking_description = form.seeking_description.data

        artist = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            genres=form.genres.data,
            image_link=form.image_link.data,
            facebook_link=form.facebook_link.data,
            website=form.website.data,
            seeking_venue=seeking_venue,
            seeking_description=seeking_description,
        )
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + artist.name + ' was successfully listed!')

    except:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    form.name.data = artist.name
    form.genres.data = artist.genres
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    form.website.data = artist.website
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description

    artist = artist.map_artist_to_dict()
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)
    try:
        form = ArtistForm(request.form)

        seeking_venue = False
        seeking_description = ''
        if 'seeking_venue' in form:
            seeking_venue = form.seeking_venue.data
        if 'seeking_description' in form:
            seeking_description = form.seeking_description.data

        artist.name = form.name.data
        artist.genres = form.genres.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.facebook_link = form.facebook_link.data
        artist.image_link = form.image_link.data
        artist.website = form.website.data
        artist.seeking_venue = seeking_venue
        artist.seeking_description = seeking_description

        db.session.commit()
        flash('Artist ' + artist.name + ' was successfully edited!')

    except:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              artist.name + ' could not be edited.')
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))

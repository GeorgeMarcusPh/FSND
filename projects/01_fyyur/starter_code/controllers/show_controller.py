#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_wtf import Form
from forms import *
from db_data_models import *

# -----------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------


@ app.route('/shows')
def shows():
    data = []
    shows = Show.query.options(db.joinedload(
        Show.Venue), db.joinedload(Show.Artist)).all()
    for show in shows:
        data.append({
            "venue_id": show.venue_id,
            "venue_name": Venue.query.filter_by(id=show.venue_id).first().name,
            "artist_id": show.artist_id,
            "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
            "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
            "start_time": show.start_time})
    return render_template('pages/shows.html', shows=data)


@ app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@ app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm()
    try:
        show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data,
        )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        flash('An error occurred. show could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')

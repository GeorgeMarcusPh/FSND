
import json
import dateutil.parser
import babel
from flask import Flask, render_template
import logging
from logging import Formatter, FileHandler
from controllers.venue_controller import *
from controllers.artist_controller import *
from controllers.show_controller import *
from db_data_models import *
from sqlalchemy import desc
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):

    if isinstance(value, str):
        date = dateutil.parser.parse(value)
    else:
        date = dateutil.parser.parse(value.strftime('%Y-%m-%d %H:%S:%M'))
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Home Controller
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    venues = Venue.query.order_by(desc(Venue.id)).limit(10).all()
    artists = Artist.query.order_by(desc(Artist.id)).limit(10).all()
    data = {
        "venues": venues,
        "artists": artists
    }
    return render_template('pages/home.html', data=data)


#----------------------------------------------------------------------------#
# Error Handling
#----------------------------------------------------------------------------#

@ app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

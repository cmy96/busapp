from flask import render_template, flash, redirect, url_for, request, make_response
from app import app
from app.forms import BusForm
from app.plots import display_plot
from app.bus import get_busstop_rankings, get_busservice_rankings, get_segment_rankings
import io
import base64
import matplotlib.pyplot as plt

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = BusForm()
    if form.validate_on_submit():
        flash("Querying")
        query = url_for("query",bus=form.bus.data, \
        timing=form.timing.data.hour,weekday=form.weekday.data,to_busstop=form.to_busstop.data)
        return redirect(query)
    return render_template('index.html',form = form,title = "Home page")

@app.route('/query')
def query():
    bus = request.args.get("bus")
    timing = request.args.get("timing") or False
    weekday = request.args.get('weekday') == "weekday"
    busstop = request.args.get("to_busstop") or False
    # return timing
    img = io.BytesIO()
    display_plot(bus,weekday=weekday,timing = timing,busstop=busstop)
    plt.savefig(img, format='png')
    # plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    url = 'data:image/png;base64,{}'.format(plot_url)
    return render_template("query.html",processed_url=url)

@app.route("/busstop_rankings")
def busstop_rankings():
    rankings_weekday = get_busstop_rankings()
    rankings_weekend = get_busstop_rankings(weekday=False)
    page = "Bus Stop"
    return render_template('ranking.html',rankings_weekday = rankings_weekday, rankings_weekend=rankings_weekend, page = page)


@app.route("/segment_rankings")
def segment_rankings():
    rankings_weekday = get_segment_rankings()
    rankings_weekend = get_segment_rankings(weekday=False)
    page = "Bus Segment"
    return render_template('ranking.html',rankings_weekday = rankings_weekday, rankings_weekend=rankings_weekend, page = page)

@app.route("/busservice_rankings")
def busservice_rankings():
    rankings_weekday = get_busservice_rankings()
    rankings_weekend = get_busservice_rankings(weekday=False)
    page = "Bus Service" 
    return render_template('ranking.html',rankings_weekday = rankings_weekday, rankings_weekend=rankings_weekend, page = page)
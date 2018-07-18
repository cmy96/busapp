from flask import render_template, flash, redirect, url_for, request, make_response
from app import app
from app.forms import BusForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = BusForm()
    if form.validate_on_submit():
        flash("Querying")
        query = url_for("query",bus=form.bus.data, \
        timing=form.timing.data,weekday=form.weekday.data)
        return redirect(query)
    return render_template('index.html',form = form,title = "Home page")

@app.route('/query')
def query():
    # bus = request.args.get("bus")
    # timing = request.args.get("timing")
    # weekday = request.args.get('weekday')
    return render_template("query.html")

@app.route('/image.png')
def image():
    import datetime
    from io import BytesIO
    import random

    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    response=make_response(png_output.getvalue())
    response.headers['Content-Type'] = 'image/png'
    return response
from operator import mod
from flask import Blueprint, render_template, request, flash, jsonify, abort
import json
from flask.helpers import url_for
import numpy as np
from datetime import date, datetime, timedelta
from flask_login import login_required
from werkzeug.utils import redirect

from edge_system import db
from edge_system.info_machine.model.machine import Machine, RegisterForm
from edge_system.info_machine.model.part_info import Part
from edge_system.info_machine.model.rework_part_info import ReworkPart

def get_machine_info_json():
    try:
        with open("edge_system/static/tmp/machine.json", "r") as read_file:
            data = json.load(read_file)
    except:
        print("ERROR")
        return None
    return data

machine = Blueprint('machine', __name__)

@machine.before_request  # con esto, esta función se ejecuta antes de cada endpoint que tengamos definido en este documento
@login_required
def constructor():
   pass

@machine.route('/machine/register_json')
def fill_machine_register_json():
    data_json = get_machine_info_json()
    form = RegisterForm(meta={'csrf': False})
    form.id.data = 13
    form.path_image.data = 'img/tmp_workstation_01.jpeg'
    form.nickname.data = data_json['nickname']
    form.description.data = data_json['description']
    form.brand.data = data_json['brand']
    form.model.data = data_json['model']
    form.voltage.data = int(data_json['voltage'])
    form.amperage.data = float(data_json['amperage'])
    form.serie.data = data_json['serie']
    form.id_line.data = int(data_json['id_line'])
    form.manufacturing_date.data = datetime.strptime(data_json['manufacturing_date'], '%Y-%m-%dT%H:%M:%S')
    form.instalation_date.data = datetime.strptime(data_json['instalation_date'], '%Y-%m-%dT%H:%M:%S')
    form.id_supplier.data = int(data_json['id_supplier'])
    form.run_date.data = datetime.strptime(data_json['run_date'], '%Y-%m-%dT%H:%M:%S')
    
    return render_template('machine/register.html', form = form)
    #return redirect(url_for('machine.machine_register', form = form))


@machine.route('/machine/register', methods=['GET', 'POST'])
def machine_register():
    print("HOLAAAA")
    form = RegisterForm(meta={'csrf': False})
    if form.validate_on_submit():
        if Machine.query.get(form.id.data):
            flash('Machine already registered!')
            return redirect(url_for('machine.machine_register'))
        #form.path_image.data = 'img/tmp_workstation_01.jpeg'
        machine_ =  Machine(id=form.id.data,
        nickname=form.nickname.data,
        description=form.description.data,
        brand=form.brand.data,
        model=form.model.data,
        voltage=form.voltage.data,
        amperage=form.amperage.data,
        serie=form.serie.data,
        id_line=form.id_line.data,
        manufacturing_date=form.manufacturing_date.data,
        instalation_date=form.instalation_date.data,
        id_supplier=form.id_supplier.data,
        run_date=form.run_date.data,
        path_image= form.path_image.data)
        print(machine_)
        db.session.add(machine_)
        db.session.commit()
        flash("Machine information saved locally!!")
        return redirect(url_for('home.home_page'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('machine/register.html', form = form)

@machine.route('/test_get_data')
def test_get_data():
    data = {'id': [], 'working_time': []}
    metrics = {'avg': 0.0, 'min': 0.0, 'max': 0.0, 'std': 0.0}
    return render_template("test/production_test.html", mode = "Week", info = "OK-NOK", \
        data = data, metrics = metrics) 

@machine.route('/get_data/<static_period>/<type_info>', methods=['GET'])
def get_data(static_period=None, type_info = None):
    print('Period::: ', static_period, '    type info: ', type_info)
    if static_period == None:
        metrics = {'empty': 'No data for the period "{}" !'.format(static_period)}
        return jsonify(metrics)
    # get data ... 
    if type_info == "Working-Time":
        metrics = get_data_working_time_from_static_period(static_period)
    elif type_info == "OK-NOK":
        metrics = get_data_ok_nok_from_static_period(static_period)
    elif type_info == "Rework":
        metrics = get_data_rework_ok_nok_from_static_period(static_period)
    else:
        metrics = get_data_reworking_time_from_static_period(static_period) 
    return jsonify(metrics)

@machine.route('/machine/info')
def info():
    machine_ = Machine.query.first()
    print(machine_)
    return render_template("machine/machine_info.html", machine = machine_)

@machine.route('/machine_info')
def info2():
    try:
        with open("edge_system/static/tmp/machine.json", "r") as read_file:
            data = json.load(read_file)
        #print(data)
        # Select the main information only:
        data_filtered = data
        nickname = data['nickname']
        print('data type: ',type(data))
        del data_filtered['nickname']
    except:
        print("ERROR")
    return render_template("machine/machine_info2.html", nickname = nickname, data = data_filtered)

#### Showing the production 

@machine.route('/production_information/<static_period>/<type_info>', methods=['GET'])
def production_information(static_period=None, type_info = None):
    if static_period is None:
        mode = "Week"
    else:
        mode = static_period
    if type_info is None:
        info = "OK-NOK"
    else:
        info = type_info
    # Display a list of the different visualizations of the data over the current week
    return render_template("production/production_sidebar.html", mode = mode,  info = info) 

# Week 
@machine.route('/week_production')
def week_production():
    # Display a list of the different visualizations of the data over the current week
    return render_template("production/production_menu.html", mode = "Week") 

@machine.route('/week_production/ok')
def week_production_ok_nok():
    # Display the information about the ok and nok items/pieces
    #parts_info = Part.query.all()
    print("Hola www ")
    return render_template("production/production.html", mode = "Week", info = "OK-NOK") 

@machine.route('/week_production/time')
def week_production_time():
    # Display the information about the statistics of the time work (the ok pieces): average, max, min,
    return render_template("production/production.html", mode = "Week", info = "Working-Time") 

@machine.route('/week_production/rework')
def week_production_rework():
    return render_template("production/production.html", mode = "Week", info = "Rework")

@machine.route('/week_production/reworking-time')
def week_production_reworking_time():
    return render_template("production/production.html", mode = "Week", info = "Reworking-Time")

# day
@machine.route('/day_production')
def day_production():
    # Display a list of the different visualizations of the data over the current day
    return render_template("production/production_menu.html", mode = "Day") 

@machine.route('/day_production/ok')
def day_production_ok_nok():
    # Display the information about the ok and nok items/pieces
    return render_template("production/production.html", mode = "Day", info = "OK-NOK")  

@machine.route('/day_production/time')
def day_production_time():
    # Display the information about the statistics of the time work (the ok pieces): average, max, min,
    return render_template("production/production.html", mode = "Day", info = "Working-Time")  

@machine.route('/day_production/rework')
def day_production_rework():
    return render_template("production/production.html", mode = "Day", info = "Rework")

@machine.route('/day_production/reworking-time')
def day_production_reworking_time():
    return render_template("production/production.html", mode = "Day", info = "Reworking-Time")

# month

@machine.route('/month_production')
def month_production():
    # Display a list of the different visualizations of the data over the current month
    return render_template("production/production_menu.html", mode = "Month") 

@machine.route('/month_production/ok')
def month_production_ok_nok():
    # Display the information about the ok and nok items/pieces
    return render_template("production/production.html", mode = "Month", info = "OK-NOK")  

@machine.route('/month_production/time')
def month_production_time():
    # Display the information about the statistics of the time work (the ok pieces): average, max, min,
    return render_template("production/production.html", mode = "Month", info = "Working-Time")  

@machine.route('/month_production/rework')
def month_production_rework():
    return render_template("production/production.html", mode = "Month", info = "Rework")

@machine.route('/month_production/reworking-time')
def month_production_reworking_time():
    return render_template("production/production.html", mode = "Month", info = "Reworking-Time")


# window time

@machine.route('/time_window_production')
def time_windowproduction():
    # Display a list of the different visualizations of the data over a time_window
    return render_template("production/production_menu.html", mode = "Time window") 



##### Functions ... 

def get_parts_ok_nok_timewindow(start_datetime, end_datetime):
    parts_info = Part.query.filter(Part.timestamp <= end_datetime)\
        .filter(Part.timestamp >= start_datetime).all() 
    return parts_info

def get_parts_working_time_timewindow(start_datetime, end_datetime):
    parts_info = Part.query.filter(Part.timestamp <= end_datetime)\
        .filter(Part.timestamp >= start_datetime).filter(Part.status == False).all() 
    return parts_info

def get_parts_rework_ok_nok(start_datetime, end_datetime):
    rework_parts_info = ReworkPart.query.filter(ReworkPart.timestamp <= end_datetime)\
        .filter(ReworkPart.timestamp >= start_datetime).all() 
    return rework_parts_info

def get_parts_reworking_time_timewindow(start_datetime, end_datetime):
    rework_parts_info = ReworkPart.query.filter(ReworkPart.timestamp <= end_datetime)\
        .filter(ReworkPart.timestamp >= start_datetime).filter(ReworkPart.status == False).all() 
    return rework_parts_info

def get_rework_ok_nok_metrics(rework_parts_info):
    """
    Get the OK/NOK rework parts metrics 
    """
    data = {}
    metrics = {'tot_ok': 0, 'tot_nok': 0}
    for part in rework_parts_info:
        if part:
            data['id'] = part.id
            data['status'] = part.status
            if data['status'] == False:
                metrics['tot_ok'] += 1
            else:
                metrics['tot_nok'] += 1
    print(metrics)
    return data, metrics

def get_ok_nok_metrics(parts_info):
    """
    Get the OK/NOK parts metrics 
    """
    data = {}
    metrics = {'tot_ok': 0, 'tot_nok': 0}
    for part in parts_info:
        if part:
            data['id'] = part.id
            data['status'] = part.status
            if data['status'] == False:
                metrics['tot_ok'] += 1
            else:
                metrics['tot_nok'] += 1
    print(metrics)
    return data, metrics

def get_reworking_time_metrics(rework_parts_info):
    data = {'id': [], 'working_time': []}
    metrics = {'avg': 0.0, 'min': 0.0, 'max': 0.0, 'std': 0.0}
    if len(rework_parts_info) != 0:
        for part in rework_parts_info:
            data['id'].append(part.id)
            data['working_time'].append(part.working_time)
        dat_ = np.array(data['working_time'])
        metrics['min'] = min(data['working_time'])
        metrics['max'] = max(data['working_time'])
        metrics['avg'] = np.mean(dat_, axis=0)
        metrics['std'] = np.std(dat_, axis=0)
    return data, metrics


def get_working_time_metrics(parts_info):
    data = {'id': [], 'working_time': []}
    metrics = {'avg': 0.0, 'min': 0.0, 'max': 0.0, 'std': 0.0}
    if len(parts_info) != 0:
        for part in parts_info:
            data['id'].append(part.id)
            data['working_time'].append(part.working_time)
        dat_ = np.array(data['working_time'])
        metrics['min'] = min(data['working_time'])
        metrics['max'] = max(data['working_time'])
        metrics['avg'] = np.mean(dat_, axis=0)
        metrics['std'] = np.std(dat_, axis=0)
    return data, metrics


def get_data_ok_nok_from_static_period(period):
    metrics = {}
    # Month [Default]
    limInfDate = date.today() + timedelta(days=-30)
    if period == "Week":
        print('In week!!!')
        limInfDate = date.today() + timedelta(days=-7)
    elif period == "Day":
        limInfDate = date.today() + timedelta(days=-1)
        print('In Day!!!')

    parts_info = get_parts_ok_nok_timewindow(limInfDate, datetime.now())
    data, metrics = get_ok_nok_metrics(parts_info)
    metrics['date_start'] = limInfDate.strftime("%d/%m/%Y")
    metrics['date_end'] = datetime.now().strftime("%d/%m/%Y")
    return metrics

def get_data_working_time_from_static_period(period):
    metrics = {}
    # Month [Default]
    limInfDate = date.today() + timedelta(days=-30)
    if period == "Week":
        print('In week!!!')
        limInfDate = date.today() + timedelta(days=-7)
    elif period == "Day":
        limInfDate = date.today() + timedelta(days=-1)
        print('In Day!!!')
    
    parts_info = get_parts_working_time_timewindow(limInfDate, datetime.now())
    data, metrics = get_working_time_metrics(parts_info)
    metrics['date_start'] = limInfDate.strftime("%d/%m/%Y")
    metrics['date_end'] = datetime.now().strftime("%d/%m/%Y")
    metrics['data'] = data
    return metrics 


def get_data_rework_ok_nok_from_static_period(period):
    metrics = {}
    # Month [Default]
    limInfDate = date.today() + timedelta(days=-30)
    if period == "Week":
        print('In week!!!')
        limInfDate = date.today() + timedelta(days=-7)
    elif period == "Day":
        limInfDate = date.today() + timedelta(days=-1)
        print('In Day!!!')

    rework_parts_info = get_parts_rework_ok_nok(limInfDate, datetime.now())
    data, metrics = get_rework_ok_nok_metrics(rework_parts_info)
    metrics['date_start'] = limInfDate.strftime("%d/%m/%Y")
    metrics['date_end'] = datetime.now().strftime("%d/%m/%Y")
    return metrics

def get_lim_date(period):
    # Month [Default]
    limInfDate = date.today() + timedelta(days=-30)
    if period == "Week":
        print('In week!!!')
        limInfDate = date.today() + timedelta(days=-7)
    elif period == "Day":
        limInfDate = date.today() + timedelta(days=-1)
        print('In Day!!!')
    return limInfDate

def get_data_reworking_time_from_static_period(period):
    metrics = {}
    print(period, '::: reworking time')
    limInfDate = get_lim_date(period)
    rework_parts_info = get_parts_reworking_time_timewindow(limInfDate, datetime.now())
    data, metrics = get_reworking_time_metrics(rework_parts_info)
    metrics['date_start'] = limInfDate.strftime("%d/%m/%Y")
    metrics['date_end'] = datetime.now().strftime("%d/%m/%Y")
    metrics['data'] = data
    return metrics 

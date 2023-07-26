from operator import mod
from flask import Blueprint, render_template, request, flash, jsonify, abort
import json
from flask.helpers import url_for
import numpy as np
from datetime import date, datetime, timedelta
from flask_login import login_required
from werkzeug.utils import redirect, secure_filename
import os

from edge_system import db, ALLOWED_EXTENSIONS_FILE, app
from edge_system.info_machine.model.machine import Machine, RegisterForm
from edge_system.info_machine.model.part_info import Part, PartForm
from edge_system.info_machine.model.rework_part_info import ReworkPart

control = Blueprint('control', __name__)

@control.before_request
@login_required
def constructor():
   pass

@control.route('/panel')
def panel():
    '''print('Panel')'''
    return render_template('control/panel.html')
    
@control.route('/panel/stop')
def stop():
    '''print('stop')
    flash('Paro de emergencia','danger')'''
    return render_template('control/panel.html')    

@control.route('/panel/on')
def luzon():
    '''print('luzon')
    flash('Luz prendida','warning')'''
    return render_template('control/panel.html')

@control.route('/panel/off')
def luzoff():
    '''print('luzoff')
    flash('Luz apagada','dark')'''
    return render_template('control/panel.html')

@control.route('/panel/start')
def start():
    '''print('start')
    flash('Inicio')'''
    return render_template('control/panel.html')
    



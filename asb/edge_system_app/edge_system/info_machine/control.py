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

@control.route('/panel/')
def panel():
    return render_template('control/panel.html')

@control.route('/stop/')
def stop():
    return render_template('control/panel.html')

@control.route('/luz/on/')
def luzon():
    return render_template('control/panel.html')

@control.route('/luz/off')
def luzoff():
    return render_template('control/panel.html')

@control.route('/start/')
def start():
    return render_template('control/panel.html')
    



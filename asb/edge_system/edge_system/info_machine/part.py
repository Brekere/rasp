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

part = Blueprint('part', __name__)

@part.before_request
@login_required
def constructor():
   pass

def allowed_extensions_file(filename):
    return '.' in filename and filename.lower().rsplit('.',1)[1] in ALLOWED_EXTENSIONS_FILE


@part.route('/part/register', methods=['POST', 'GET'])
def part_register():
    form = PartForm() #meta={'csrf': False}

    machines = [(m.id, m.nickname) for m in Machine.query.all()]
    form.id_machine.choices=machines

    if form.validate_on_submit():      
        if Part.query.get(form.id.data):
            flash('Part already registered!')
            return redirect(url_for('part.part_register'))
        
        part_ =  Part(
        request.form['id'],
        request.form['namepart'],
        request.form['timestamp'], 
        request.form['status'], 
        request.form['working_time'], 
        request.form['id_machine'],
        request.form['file'])

        if form.file.data:
         file = form.file.data
         if allowed_extensions_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            part.file = filename


        db.session.add(part_)
        db.session.commit()
        flash("Part information saved locally!!")
        return redirect(url_for('part.part_info_all'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('part/register.html', form = form)



@part.route('/part/update/<int:id>', methods=['POST', 'GET'])
def part_update(id):
    part = Part.query.get_or_404(id)

    form = PartForm() #meta={'csrf': False}

    machines = [(m.id, m.nickname) for m in Machine.query.all()]
    form.id_machine.choices=machines

    if request.method == 'GET':
        form.id.data = part.id
        form.namepart.data = part.namepart
        form.timestamp.data = part.timestamp
        form.status.data = part.status
        form.working_time.data = part.working_time
        form.id_machine.data = part.id_machine
        form.file.data = part.file
        
    if form.validate_on_submit():
        # actualizar un registro
        part.id = form.id.data
        part.namepart = form.namepart.data
        part.timestamp = form.timestamp.data
        part.status = form.status.data
        part.working_time = form.working_time.data
        part.id_machine = form.id_machine.data

        if form.file.data:
         file = form.file.data
         if allowed_extensions_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            part.file = filename
        
        db.session.add(part)
        db.session.commit()
        flash("Parte actualizada con exito")
        return redirect(url_for('part.part_info_all', id=part.id))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('part/update.html', part=part, form=form)

@part.route('/part/info_all/')
def part_info_all():
    parts = Part.query.all()
    print(parts)
    return render_template("part/parts_info.html", parts = parts)

@part.route('/part/<int:id>')
def show(id):
    part = Part.query.get_or_404(id)
    return render_template('part/show.html', part=part)

@part.route('/part/delete/<int:id>')
def part_delete(id):
    part = Part.query.get_or_404(id)

    db.session.delete(part)
    db.session.commit()
    flash("parte borrada con exito")

    return redirect(url_for('part.part_info_all'))


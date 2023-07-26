from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy.sql.expression import and_

from edge_system.info_machine.model.part_info import Part, PartForm
from edge_system import db, ALLOWED_EXTENSIONS_FILE, app, rol_admin_need


production = Blueprint('production', __name__)

@production.before_request  # con esto, esta función se ejecuta antes de cada endpoint que tengamos definido en este documento
@login_required
@rol_admin_need
def constructor():
   pass

@production.route('/production')
def production_all():
    parts = Part.query.all()
    ok = sum([p.OK for p in Part.query.all()])
    nok = sum([p.NOK for p in Part.query.all()])
    date = [p.timestamp for p in Part.query.all()]
    '''print(date)

    for p in date:
        print(p.day)
        print(p.month)
        print(p.year)'''

    #print(p.strftime("%d/%m/%Y"))
        
    return render_template("production/production_all.html", parts=parts, ok=ok, nok=nok)

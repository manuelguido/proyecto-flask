from flask import redirect, render_template, request, url_for, abort, session, flash
from flaskps.db import get_db
from flaskps.models.user import User
from flaskps.models.ciclo import Ciclo
from flaskps.models.taller import Taller
from flaskps.models.responsable import Responsable
from flaskps.helpers.auth import authenticated
from flaskps.resources import forms

def store():
    if not authenticated(session):
        abort(401)
    #Chequea permiso
    User.db = get_db()
    if (User.tiene_permiso(session['id'],'administrativo_new')):
        if request.method == "POST" and forms.ValidateCiclo(request.form).validate():
            if int(request.form['año']) < int(1990) or int(request.form['año']) > int(2025):
                flash('Verifica los campos obligatorios. No ingreses valores no permitidos', 'error')
            else:
                Ciclo.db = get_db()
                if not Ciclo.semestreExiste(request.form):
                    Ciclo.store(request.form)
                    flash("Ciclo lectivo agregado correctamente" ,'success')
                else:
                    flash("El semestre ya tiene un ciclo lectivo asignado", 'error')
        else:
            flash('Verifica los campos obligatorios. No ingreses valores no permitidos', 'error')
        return redirect(url_for('panel_ciclos'))
    else:
        abort(401)

def delete(id_data):
    if not authenticated(session):
        abort(401)
    #Chequea permiso
    User.db = get_db()
    if (User.tiene_permiso(session['id'],'administrativo_destroy')):
        Ciclo.db = get_db()
        Ciclo.delete(id_data)
        flash("Se eliminó el ciclo lectivo correctamente" ,'success')
        return redirect(url_for('panel_ciclos'))
    else:
        abort(401)

def update():
    if not authenticated(session):
        abort(401)

    #Chequea permiso
    User.db = get_db()
    if (User.tiene_permiso(session['id'],'administrativo_update')):
        if request.method == "POST" and forms.ValidateCiclo(request.form).validate():
            Ciclo.db = get_db()
            Ciclo.update(request.form)
            flash("Se actualizó el ciclo lectivo correctamente" ,'success')
        else:
            flash('Verifica los campos obligatorios. No ingreses valores no permitidos', 'error')
            return redirect(url_for("get_update_ciclo", id_data=request.form.get("id_data")))
        return redirect(url_for('panel_ciclos'))
    else:
        abort(401)

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required

from app.forms import AliasSearchForm, AliasEditor, AliasCreator


from . import LDAP, alias
from .models import AliasObject


@alias.route('/', methods=['GET', 'POST'], defaults={'name': 'index'})
@alias.route('/<name>')
def show(name):
    if name != 'index':
        desc, result = LDAP.alias_values(name)
        if not result:
            flash('Алиаса\'{0}\' не существует'.format(name))
            return redirect(url_for('alias.show'))
        else:
            return render_template('alias_show.html', title=name, description=desc, values=result)

    else:
        result = ''
        form = AliasSearchForm()
        if form.validate_on_submit():
            result = LDAP.find_aliases(form.search.data)
            flash('Вы искали \'{}\''.format(form.search.data))
        return render_template('alias_search.html', aliases=result, form=form)


@alias.route('/<name>/edit', methods=['GET', 'POST'])
@login_required
def edit(name):
    aliasobj = AliasObject(name, LDAP)
    form = AliasEditor(obj=aliasobj)
    if request.method == 'POST':
        if 'submit' in request.form:
            if form.validate_on_submit():
                form.populate_obj(aliasobj)
                aliasobj.clean()
                if aliasobj.change():
                    flash('Все значения сохранены')
                    return redirect(url_for('alias.show', name=name))
                else:
                    flash('Не удалось сохранить данные')
                    return redirect(url_for('alias.edit', name=name))
        else:
            flash('Изменения отменены')
            return redirect(url_for('alias.show', name=name))
    return render_template('alias_edit.html', title=name, form=form)


@alias.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = AliasCreator()
    if request.method == 'POST':
        if 'submit' in request.form:
            if form.validate_on_submit():
                aliasobj = AliasObject(form.key.data, LDAP)
                result = aliasobj.add2ldap()
                if result == 'success':
                    flash('Новый алиас создан, не забудьте изменить значения по умолчанию')
                    return redirect(url_for('alias.edit', name=form.key.data))
                else:
                    flash('Не удалось добавить \'{0}\': {1}'.format(form.key.data, result))
                    return redirect(url_for('alias.new'))
        else:
            flash('Изменения отменены')
            return redirect(url_for('alias.show', name='index'))
    return render_template('alias_new.html', form=form)

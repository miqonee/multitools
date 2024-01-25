from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required

from app.forms import ProxySearchForm, ProxyUnlimForm


from . import ldap_proxy, proxy


@proxy.route('/', methods=['GET', 'POST'])
def search():
    result = ''
    form = ProxySearchForm()
    if form.validate_on_submit():
        result = ldap_proxy.find_accounts(form.attribute.data, form.search.data)
        flash('Вы искали \'{}\''.format(form.search.data))
    return render_template('proxy_search.html', accounts=result, form=form)


@proxy.route('/<dn>', methods=['GET', 'POST'])
@login_required
def edit(dn):
    values = ldap_proxy.account_values(dn)
    if not values:
        flash('Аккаунта\'{0}\' не существует'.format(dn))
        return redirect(url_for('proxy.search'))
    else:
        form = ProxyUnlimForm()
        action = {'TRUE': 'снято', 'FALSE': 'установлено'}
        if request.method == 'POST':
            unlim = 'TRUE' if 'noblock' in request.form else 'FALSE'
            if 'submit' in request.form:
                if unlim != str(values['proxyTempNoBlock'][0]).upper():
                    if ldap_proxy.unlim_account(dn, unlim):
                        flash('{0}: ограничение трафика {1}'.format(values['cn'][0],
                                                                    action[unlim]))
                    else:
                        flash('Ошибка, не удалось переключить ограничение')
                if str(form.limit.data) != str(values['proxySize'][0]):
                    if ldap_proxy.change_limit(dn, form.limit.data):
                        flash('{0}: новый порог трафика - {1}МБ'.format(values['cn'][0],
                                                                        form.limit.data))
                    else:
                        flash('Ошибка, не удалось изменить порог трафика')

                return redirect(url_for('proxy.edit', dn=dn))
            else:
                flash('Ничего не изменилось')
        return render_template('proxy_edit.html', form=form, state=values)

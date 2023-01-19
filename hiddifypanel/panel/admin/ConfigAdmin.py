from flask_admin.contrib import sqla
from hiddifypanel.panel.database import db
from hiddifypanel.models import ConfigEnum
from wtforms.validators import Regexp,ValidationError
import re
import uuid

class ConfigAdmin(sqla.ModelView):
    can_export = True
    column_default_sort=('category',False)
    column_display_pk = True
    can_delete = False
    can_create  = False
    column_editable_list=["value"]
    column_searchable_list=["key","value"]
    form_widget_args = {
        'description': {
            'readonly': True
        },
    }
    def on_model_change(self, form, model, is_created):
        if model.key==ConfigEnum.decoy_site:
            if not re.match("http(s|)://([A-Za-z0-9\-\.]+\.[a-zA-Z]{2,})/?", model.value):            
                raise ValidationError('Invalid address: e.g., https://www.wikipedia.org/')
        if model.key in [ConfigEnum.admin_secret,ConfigEnum.ssfaketls_secret]:
            if not re.match("^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$", model.value):            
                raise ValidationError('Invalid UUID e.g.,'+ str(uuid.uuid4()))

        if model.key in [ConfigEnum.telegram_secret]:
            if not re.match("^[0-9a-fA-F]{32}$", model.value):            
                raise ValidationError('Invalid UUID e.g.,'+ uuid.uuid4().hex)

        if model.key==ConfigEnum.proxy_path:
            if not re.match("^[a-zA-Z0-9]*$", model.value):            
                raise ValidationError('Invalid path. should be asci string')

        if model.key in [ConfigEnum.tls_ports,ConfigEnum.kcp_ports,ConfigEnum.http_ports]:
            if not re.match("^(\d,?)*$", model.value):            
                raise ValidationError('Invalid path. should be asci string')

        if model.key==ConfigEnum.http_ports:
            if "80" not in model.value.split(","):
                raise ValidationError('Port 80 should always be presented')
        if model.key==ConfigEnum.tls_ports:
            if "443" not in model.value.split(","):
                raise ValidationError('Port 443 should always be presented')
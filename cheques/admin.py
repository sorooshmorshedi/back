from django.contrib import admin

from cheques.models.ChequeModel import Cheque
from cheques.models.ChequebookModel import Chequebook
from cheques.models.StatusChangeModel import StatusChange

admin.site.register(Cheque)
admin.site.register(Chequebook)
admin.site.register(StatusChange)


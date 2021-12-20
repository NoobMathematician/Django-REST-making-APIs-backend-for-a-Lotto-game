from django.contrib import admin
from .models import Lottos, Prizes, Tickets,PrizeSingle

admin.site.register(Lottos)
admin.site.register(Prizes)
admin.site.register(Tickets)
admin.site.register(PrizeSingle)

from django.contrib import admin

# Register your models here.
from league.models import League,LeagueStage,Team,TeamStage,fixtures

admin.site.register(League)
admin.site.register(LeagueStage)
admin.site.register(Team)
admin.site.register(TeamStage)
admin.site.register(fixtures)

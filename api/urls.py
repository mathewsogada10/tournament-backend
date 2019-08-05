from api.views import LeagueRudeView,LeagueRudViewPost,LeagueRudViewAll,LeaguStageAll,LeaguStagePost,LeagueStageView
from api.views import TeamViewPost,TeamView,TeamViewAll,TeamStageView,TeamStagePost,TeamStageViewAll
from api.views import FixtureView,FixturePost,FixtureViewAll
from django.urls import path
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [
    url(r'^auth-jwt/', obtain_jwt_token),
    url(r'^auth-jwt-refresh/', refresh_jwt_token),
    url(r'^auth-jwt-verify/', verify_jwt_token),
  
    path(r'league/all', LeagueRudViewAll.as_view(), name='league_all'),
    path(r'league/create', LeagueRudViewPost.as_view(), name='league_create'),
    url (r'^league/(?P<id>\d+)/$', LeagueRudeView.as_view(), name = 'my_league'),

    path(r'league/stages', LeaguStageAll.as_view(), name='league_stages'),
    path(r'league/createStage',LeaguStagePost.as_view(),name = 'league_create_stage'),
    url (r'^league/stage/(?P<id>\d+)/$', LeagueStageView.as_view(), name = 'league_stage'),

    path(r'league/teams', TeamViewAll.as_view(), name='league_teams'),
    path(r'league/createTeam',TeamViewPost.as_view(),name = 'league_create_team'),
    url (r'^league/team/(?P<id>\d+)/$', TeamView.as_view(), name = 'league_team'),

    path(r'league/teamStages', TeamStageViewAll.as_view(), name='team_stages'),
    path(r'league/createTeamStage',TeamStagePost.as_view(),name = 'create_team_stage'),
    url (r'^league/teamStage/(?P<id>\d+)/$', TeamStageView.as_view(), name = 'team_stage'),
    
    path(r'league/fixtures', FixtureViewAll.as_view(), name='league_fixtures'),
    path(r'league/createFixture',FixturePost.as_view(),name = 'create_fixture'),
    url (r'^league/fixture/(?P<id>\d+)/$', FixtureView.as_view(), name = 'league_fixture')
]
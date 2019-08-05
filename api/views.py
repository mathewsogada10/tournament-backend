#from django.shortcuts import render
from league.models import League,LeagueStage,Team,TeamStage,fixtures
from .serializers import LeagueSerializer,LeagueStageSerializer,TeamSerializer,TeamStageSerializer,FixtureSerializer
from rest_framework import generics, mixins
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly
from datetime import datetime, timedelta

class LeagueRudeView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field  = 'id'  # slug, id # url(r'?P<pk>\d+')
    #queryset  = League.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LeagueSerializer
    def get_queryset(self):
        return League.objects.all()

    #def get_object(self):
     #   pk = self.kwargs.get("id")
     #   return League.objects.get(pk = pk)

class LeagueRudViewPost(generics.CreateAPIView):
    lookup_field  = 'id'  # slug, id # url(r'?P<pk>\d+')
    #queryset  = League.objects.all()
    serializer_class = LeagueSerializer
    def get_queryset(self):
        return League.objects.all()

class LeagueRudViewAll(mixins.CreateModelMixin, generics.ListAPIView):
      # slug, id # url(r'?P<pk>\d+')
    #queryset  = League.objects.all()
    serializer_class = LeagueSerializer
    def get_queryset(self):
        #return League.objects.all()
        qs = League.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(name__icontains = query)).distinct()
        return qs
    
    def post(self,request, *args,**kwargs):
        return self.create(*args,**kwargs)
    def put(self,request, *args,**kwargs):
        return self.create(*args,**kwargs)
    def patch(self,request, *args,**kwargs):
        return self.create(*args,**kwargs)

#League Stages
class LeagueStageView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = LeagueStageSerializer

    def get_queryset(self):
        return LeagueStage.objects.all()

class LeaguStagePost(generics.CreateAPIView):
    lookup_field = 'id'
    serializer_class = LeagueStageSerializer
    def get_queryset(self):
        return LeagueStage.objects.all()

class LeaguStageAll(mixins.CreateModelMixin,generics.ListAPIView):
    serializer_class = LeagueStageSerializer
    def get_queryset(self):
        qs = LeagueStage.objects.all().order_by("-seasonEnd")
        stage = self.request.GET.get("stage")
        leag = self.request.GET.get("league")
        season = self.request.GET.get("season")
        if leag is not None and season is not None:
            qs = qs.filter(Q(league__name__icontains = leag,seasonStart__icontains=season))
        elif stage is not None and leag is not None and season is not None:
            qs = qs.filter(Q(league__name__icontains = leag, seasonStart__icontains = season, name__icontains = stage))
        elif leag is not None and stage is not None:
            qs = qs.filter(Q(league__name__icontains = leag, name__icontains = stage))
        elif leag is not None and season is None:
            qs = qs.filter(Q(league__name = leag))
        return qs

#Teams
class TeamViewPost(generics.CreateAPIView):
    lookup_field = 'id'
    serializer_class = TeamSerializer
    def get_queryset(self):
        return Team.objects.all()

class TeamView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = TeamSerializer
    def get_queryset(self):
        return Team.objects.all()

class TeamViewAll(mixins.CreateModelMixin,generics.ListAPIView):
    serializer_class = TeamSerializer
    
    def get_queryset(self):
        qs = Team.objects.all()
        query = self.request.GET.get('name')
        if query is not None:
            qs = qs.filter(Q(name__icontains = query))
        return qs

#League and stage relation
class TeamStageView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = TeamStageSerializer
    def get_queryset(self):
        return TeamStage.objects.all()

class TeamStagePost(generics.CreateAPIView):
    lookup_field = 'id'
    def get_queryset(self):
        return TeamStage.objects.all()

class TeamStageViewAll(mixins.CreateModelMixin,generics.ListAPIView):
    serializer_class = TeamStageSerializer
    def get_queryset(self):
        qs = TeamStage.objects.order_by('-points','-goalDiff','-stage__name')
        query = self.request.GET.get('stageId')
        if query is not None:
            qs = qs.filter(Q(stage__id = query)).order_by('-points','-goalDiff')
        return qs


#fixtures
class FixtureView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = FixtureSerializer
    def get_queryset(self):
        return fixtures.objects.all()

    def put(self, request, *args, **kwargs):
        #serializer = FixtureSerializer(fx, many=True)
        fxDict = self.request.data
        #st_id = fx.stage
        #hTeam = serializer.data[0]["homeTeam"]
        #ATeam = serializer.data[0]["awayTeam"]
        #print(serializer.data[0]["stage"])
        #teamStHome = qs.filter(Q(team = hTeam,stage=st_id))
        teamStHome = TeamStage.objects.get(team = fxDict["homeTeam"], stage=fxDict["stage"])
        teamStAway = TeamStage.objects.get(team = fxDict["awayTeam"], stage=fxDict["stage"])
        teamStHome.goalScored = teamStHome.goalScored + fxDict["homeTeamGoal"]
        teamStHome.goalConceded = teamStHome.goalConceded + fxDict["awayTeamGoal"]
        teamStAway.goalScored = teamStAway.goalScored + fxDict["awayTeamGoal"]
        teamStAway.goalConceded = teamStAway.goalConceded + fxDict["homeTeamGoal"]
        teamStAway.goalDiff = teamStAway.goalScored - teamStAway.goalConceded
        teamStHome.goalDiff = teamStHome.goalScored - teamStHome.goalConceded
        teamStHome.gamesPlayed = teamStHome.gamesPlayed + 1
        teamStAway.gamesPlayed = teamStAway.gamesPlayed + 1

        if fxDict["homeTeamGoal"] > fxDict["awayTeamGoal"]:
            teamStHome.points = teamStHome.points + 3
        elif fxDict["awayTeamGoal"] > fxDict["homeTeamGoal"]:
            teamStAway.points = teamStAway.points + 3
        else:
            teamStAway.points = teamStAway.points + 1
            teamStHome.points = teamStHome.points + 1
        teamStHome.save()
        teamStAway.save()
        return self.update(request, *args, **kwargs)
        

class FixturePost(generics.CreateAPIView):
    lookup_field = 'id'
    serializer_class = FixtureSerializer
    def get_queryset(self):
        fx = fixtures.objects.all()
        return fx

class FixtureViewAll(mixins.CreateModelMixin,generics.ListAPIView):
    serializer_class = FixtureSerializer
    def get_queryset(self):
        qs = fixtures.objects.order_by('-matchDate')
        leagueName = self.request.GET.get('league')
        stageName = self.request.GET.get('season')
        if leagueName is not None and stageName is not None:
            qs = qs.filter(Q(stage__name = stageName,stage__league__name=leagueName)).order_by('-matchDate')
        else:
            d = datetime.today()
            qs = qs.filter(Q(matchDate >= d)).order_by('-matchDate')
        return qs

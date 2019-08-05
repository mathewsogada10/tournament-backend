from rest_framework import serializers
from league.models import League,LeagueStage,Team,TeamStage,fixtures
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Q

class LeagueSerializer(serializers.ModelSerializer): #form.modelform
    class Meta:
        model = League
        fields = [
            'id',
            'name',
            'createdAt'
        ]

        read_only_fields = ['id']
# serializer converts to JSON and validates data passed
    def validate_name(self,value):
            nm = League.objects.filter(name=value)
            if nm.exists(): 
                raise serializers.ValidationError("The name must be unique")
            return value
#Team Stage
class TeamStageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TeamStage
        fields = [
            'id',
            'team',
            'stage',
            'points',
            'goalScored',
            'goalConceded',
            'goalDiff',
            'gamesPlayed'
        ]
        read_only_fields=['id']

class LeagueStageSerializer(serializers.ModelSerializer):
    #teamStages = serializers.StringRelatedField(many=True, read_only=True)
    #teamStages = TeamStageSerializer(many=True, read_only=True)
    teamStages = serializers.SerializerMethodField('get_Tstages')
    class Meta:
        model = LeagueStage
        fields = [
            'id',
            'name',
            'league',
            'seasonStart',
            'seasonEnd',
            'teamStages'
        ]
        read_only_fields = [id]

        validators = [
            UniqueTogetherValidator(
                queryset=LeagueStage.objects.all(),
                fields=['league', 'name','seasonStart']
            )
        ]

    def get_Tstages(self, obj):
        qset = TeamStage.objects.all().filter(Q(stage=obj.id)).order_by('-points','-goalDiff')
        ser = TeamStageSerializer(qset, many=True, read_only=True)
        return ser.data
        
class TeamSerializer(serializers.ModelSerializer):
    teamFixtures = serializers.SerializerMethodField('get_teams')
    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'teamFixtures'
        ]
        read_only_fields = [id]

        validators = [
            UniqueTogetherValidator(
                queryset = Team.objects.all(),
                fields = ['name']
            )
        ]

    def validate_name(self,value):
        nm = Team.objects.filter(name=value)
        if nm.exists(): 
             raise serializers.ValidationError("The name must be unique")
        return value

    def get_teams(self,obj):
        qs = fixtures.objects.order_by('-matchDate')
        ser = FixtureSerializer(qs,many = True, read_only=True)
        return ser.data

class FixtureSerializer(serializers.ModelSerializer):
    class Meta:
        model = fixtures
        fields = [
            'id',
            'homeTeam',
            'awayTeam',
            'createdAt',
            'matchDate',
            'homeTeamGoal',
            'awayTeamGoal',
            'stage'
        ]
        read_only_fields = [id]
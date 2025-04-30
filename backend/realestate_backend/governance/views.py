from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import VotingProposal, Vote, GovernanceRule
from .serializers import VotingProposalSerializer, VoteSerializer, GovernanceRuleSerializer


# Create your views here.

class VotingProposalViewSet(viewsets.ModelViewSet):
    queryset = VotingProposal.objects.all()
    serializer_class = VotingProposalSerializer
    permission_classes = [IsAuthenticated]


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]


class GovernanceRuleViewSet(viewsets.ModelViewSet):
    queryset = GovernanceRule.objects.all()
    serializer_class = GovernanceRuleSerializer
    permission_classes = [IsAuthenticated]
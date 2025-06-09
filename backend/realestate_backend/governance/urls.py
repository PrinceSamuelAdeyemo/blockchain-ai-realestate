from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VotingProposalViewSet,
    VoteViewSet,
    GovernanceRuleViewSet,
)

router = DefaultRouter()

router.register(r'voting-proposals', VotingProposalViewSet, basename='votingproposal')
router.register(r'votes', VoteViewSet, basename='vote')
router.register(r'governance-rules', GovernanceRuleViewSet, basename='governancerule')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]

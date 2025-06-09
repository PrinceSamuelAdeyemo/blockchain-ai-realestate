from django.contrib import admin
from .models import VotingProposal, Vote, GovernanceRule
from django.utils.translation import gettext_lazy as _

# Register your models here.
admin.site.register([
    VotingProposal,
    Vote,
    GovernanceRule,
])
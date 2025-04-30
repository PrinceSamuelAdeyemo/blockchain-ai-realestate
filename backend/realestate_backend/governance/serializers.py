from rest_framework import serializers
from .models import VotingProposal, Vote, GovernanceRule


class VotingProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotingProposal
        fields = [
            'id', 'tokenized_asset', 'proposed_by', 'proposal_type', 'title',
            'description', 'status', 'voting_system', 'start_block', 'end_block',
            'min_tokens_to_pass', 'execution_calls', 'executed_at', 'execution_tx',
            'created_at', 'updated_at'
        ]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = [
            'id', 'proposal', 'voter', 'choice', 'voting_power', 'voted_at_block',
            'signature', 'is_delegated', 'delegate', 'created_at'
        ]


class GovernanceRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernanceRule
        fields = [
            'id', 'name', 'description', 'scope', 'is_active', 'condition',
            'actions', 'created_by_proposal', 'version', 'previous_version',
            'created_at', 'updated_at'
        ]
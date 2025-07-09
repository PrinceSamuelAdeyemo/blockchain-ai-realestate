from django.core.management.base import BaseCommand
from web3 import Web3
import json, os
from decouple import config
from property.models import Property
from core.models import CustomUser

class Command(BaseCommand):
    help = "Sync blockchain events with backend DB"

    def handle(self, *args, **kwargs):
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        contract_path = [
            'P:\\', 'decentralized_ai_realestate', 'blockchain',
            'artifacts', 'contracts', 'PropertyCrowdfund.sol', 'PropertyCrowdfund.json'
        ]
        with open(os.path.join(*contract_path)) as f:
            contract_json = json.load(f)
        contract_abi = contract_json["abi"]
        contract_address = config("PROPERTYCROWDFUND_CONTRACTADDRESS")
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)

        # Example: Sync PropertyListed events
        last_block = 0  # Store/load this from DB for incremental sync!
        latest_block = w3.eth.block_number
        events = contract.events.PropertyListed().get_logs(fromBlock=last_block+1, toBlock=latest_block)
        for event in events:
            property_id = event['args']['propertyId']
            owner = event['args']['owner']
            # Update or create property in DB
            prop, created = Property.objects.get_or_create(
                blockchain_property_id=property_id,
                defaults={'blockchain_tx_hash': event['transactionHash'].hex()}
            )
            if created:
                # Optionally assign owner if you have a mapping
                user = CustomUser.objects.filter(wallet_address__iexact=owner).first()
                if user:
                    prop.owners.add(user)
                prop.save()
        # Repeat for other events (OwnershipTransferred, etc.)
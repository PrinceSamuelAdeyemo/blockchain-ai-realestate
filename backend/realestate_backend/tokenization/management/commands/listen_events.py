from django.core.management.base import BaseCommand
from web3 import Web3
from .models import ContractEvent

class Command(BaseCommand):
    def handle(self, *args, **options):
        w3 = get_web3()
        token_contract = get_contract('TOKEN')
        
        event_filter = token_contract.events.Transfer.createFilter(
            fromBlock='latest'
        )
        
        while True:
            for event in event_filter.get_new_entries():
                ContractEvent.objects.create_from_web3_event(
                    contract=SmartContract.objects.get(name='TOKEN'),
                    web3_event=event
                )
            time.sleep(10)
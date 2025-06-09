from django.shortcuts import render
from .models import (
    TokenizedAsset,
    TokenOwnership,
    FractionalOwnership,
    TokenTransaction
)
from .serializers import (
    TokenizedAssetSerializer,
    TokenOwnershipSerializer,
    FractionalOwnershipSerializer, 
    TokenTransactionSerializer
)
from rest_framework import viewsets

from property.models import Property
from tokenization.models import TokenizedAsset
#from decentralized_ai_realestate.blockchain.utils import get_contract

from web3 import Web3
import json
import os
from decouple import config


# Create your views here.

class TokenizedAssetViewSet(viewsets.ModelViewSet):
    queryset = TokenizedAsset
    serializer_class = TokenizedAssetSerializer
    
    
class TokenOwnershipViewSet(viewsets.ModelViewSet):
    queryset = TokenOwnership
    serializer_class = TokenOwnershipSerializer
    
    
class FractionalOwnershipViewset(viewsets.ModelViewSet):
    queryset = FractionalOwnership
    serializer_class = FractionalOwnershipSerializer
    
    
class TokenTransactionViewSet(viewsets.ModelViewSet):
    queryset = TokenTransaction
    serializer_class = TokenTransactionSerializer
    
    

def tokenize_property(request, property_id):
    property = Property.objects.get(id=property_id)
    
    # 1. Deploy token contract
    token_contract = get_contract('TOKEN')
    tx_hash = token_contract.functions.mintTokens(
        request.user.profile.default_wallet.address,
        int(property.base_value * 10**18 / token_price)
    ).transact({
        'from': settings.PLATFORM_WALLET
    })
    
    # 2. Create TokenizedAsset record
    tokenized = TokenizedAsset.objects.create(
        property=property,
        token_name=f"{property.title} Tokens",
        token_symbol=f"RE{property.id}",
        total_supply=property.base_value,
        contract_address=token_contract.address,
        deployer_address=request.user.profile.default_wallet.address
    )
    
    # 3. Update PropertyRegistry
    registry = get_contract('REGISTRY')
    registry.functions.transferOwnership(
        property.id,
        token_contract.address
    ).transact({
        'from': settings.PLATFORM_WALLET
    })
    
    return JsonResponse({'status': 'success', 'tx_hash': tx_hash.hex()})


def get_contract():
    # Connect to Ganache
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    # Load ABI
    with open("p:/decentralized_ai_realestate/blockchain/artifacts/contracts/PropertyCrowfund.sol/PropertyCrowdfund.json") as f:
        contract_json = json.load(f)
        abi = contract_json["abi"]

    # Contract address from deployment
    contract_address = config("PROPERTYCROWDFUND_CONTRACT_ADDRESS")

    contract = w3.eth.contract(address=contract_address, abi=abi)

    return contract

def list_property(owner_private_key, price_wei):
    acct = w3.eth.account.privateKeyToAccount(owner_private_key)
    tx = get_contract.functions.listProperty(price_wei).build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 300000,
        "gasPrice": w3.toWei("20", "gwei"),
    })
    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

def invest_property(investor_private_key, property_id, amount_wei):
    acct = w3.eth.account.privateKeyToAccount(investor_private_key)
    tx = get_contract.functions.invest(property_id).build_transaction({
        "from": acct.address,
        "value": amount_wei,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 300000,
        "gasPrice": w3.toWei("20", "gwei"),
    })
    signed = acct.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)
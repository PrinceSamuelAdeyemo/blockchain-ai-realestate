from web3 import Web3
from django.conf import settings

def get_web3():
    w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_CONFIG['PROVIDER_URL']))
    if settings.BLOCKCHAIN_CONFIG['CHAIN_ID'] in [137, 80001]:  # Polygon/Mumbai
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def get_contract(contract_name):
    w3 = get_web3()
    abi = SmartContract.objects.get(name=contract_name).abi.abi_json
    return w3.eth.contract(
        address=settings.BLOCKCHAIN_CONFIG['CONTRACT_ADDRESSES'][contract_name],
        abi=abi
    )
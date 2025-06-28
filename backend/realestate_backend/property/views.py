from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Property, PropertyType, Amenity, PropertyImage, PropertyDocument
from .serializers import (
    PropertySerializer,
    PropertyTypeSerializer,
    AmenitySerializer,
    PropertyImageSerializer,
    PropertyDocumentSerializer,
)

from django.shortcuts import render
import pickle
from sklearn.preprocessing import LabelEncoder
from django.views.decorators.csrf import csrf_exempt
import os
import pandas as pd
import joblib
import os
from web3 import Web3
from decouple import config
import json
from core.models import CustomUser

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from ai_integration.train_and_register_model import load_model_and_predict

from drf_spectacular.utils import extend_schema



class PropertyTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing PropertyType objects.
    """
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer


class AmenityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Amenity objects.
    """
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer


class PropertyImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing PropertyImage objects.
    """
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer


class PropertyDocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing PropertyDocument objects.
    """
    queryset = PropertyDocument.objects.all()
    serializer_class = PropertyDocumentSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    
    def create(self, request, *args, **kwargs):
        print(request.data)
        request.data["owners"] = [request.data["owners"]]
        print("ggg", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        property_instance = serializer.instance
        owner = property_instance.owners.first()  # Assuming ManyToMany or FK
        owner_wallet_address = owner.wallet_address if owner else None

        try:
            # Connect to Ganache
            w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
            if not w3.is_connected():
                raise Exception("Web3 is not connected to Ganache")

            print(w3.is_connected())

            # Load contract ABI and address
            contract_path = [
                'P:\\', 'decentralized_ai_realestate', 'blockchain',
                'artifacts', 'contracts', 'PropertyCrowdfund.sol', 'PropertyCrowdfund.json'
            ]
            with open(os.path.join(*contract_path)) as f:
                contract_json = json.load(f)

            contract_abi = contract_json["abi"]
            contract_address = Web3.to_checksum_address(config("PROPERTYCROWDFUND_CONTRACTADDRESS"))

            contract = w3.eth.contract(address=contract_address, abi=contract_abi)

            acct = w3.eth.account.from_key("0x70ecd64667e2a471ac548c01f3fcb0131d29b1223b719a0cd7892f2e85ad9a10")
            print(w3.from_wei(w3.eth.get_balance(acct.address), 'ether'))

            # Price in ETH -> Wei conversion
            print("Base Value (USD):", property_instance.base_value)
            eth_usd_rate = 2700  # Assume static rate or get live rate
            price_in_eth = property_instance.base_value / eth_usd_rate
            price_in_wei = w3.to_wei(price_in_eth, 'ether')
            print("Price in Wei:", price_in_wei)

            # Determine sender account
            if owner_wallet_address:
                sender = Web3.to_checksum_address(owner_wallet_address)
            else:
                sender = w3.eth.accounts[0]  # Default to Ganache account 0

            # Print balances
            print(f"Sender Wallet: {sender}")
            print(f"Balance: {w3.from_wei(w3.eth.get_balance(sender), 'ether')} ETH")

            # Optional: Check another account
            alt = w3.eth.accounts[7]
            print(f"Other Wallet (accounts[7]): {alt} -> {w3.from_wei(w3.eth.get_balance(alt), 'ether')} ETH")

            # Send transaction to contract
            tx_hash = contract.functions.listProperty(int(price_in_wei)).transact({'from': sender})
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            # Extract propertyId from event
            logs = contract.events.PropertyListed().process_receipt(tx_receipt)
            blockchain_property_id = logs[0]['args']['propertyId'] if logs else None

            # Save to model
            property_instance.blockchain_tx_hash = tx_hash.hex()
            property_instance.blockchain_property_id = blockchain_property_id
            property_instance.save()

            return Response(
                {"message": "Property saved to backend and blockchain"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            print("Blockchain registration failed:", e)

        # Still return backend result even if blockchain fails
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        print(data)

        # Prepare input for prediction
        prediction_input = {
            'apartment_total_area': data.get('total_area'),
            'apartment_living_area': data.get('usable_area'),
            'apartment_rooms': data.get('bedrooms', 0) + data.get('bathrooms', 0),
            'apartment_bedrooms': data.get('bedrooms'),
            'apartment_bathrooms': data.get('bathrooms'),
            'building_age': 8,
            'building_total_floors': data.get('total_floors'),
            'apartment_floor': data.get('floor_number'),
            'country_encoded': data.get('country_encoded'),
            'price_per_sqm': data.get('price_per_sqm'),
        }

        try:
            prediction = predict_price_from_dict(prediction_input)
            data['price_prediction'] = prediction
            print(prediction)
        except Exception as e:
            data['price_prediction'] = None
            data['prediction_error'] = str(e)

        if instance.owners.exists():
            owner = instance.owners.first()
            data['owner_wallet_address'] = owner.wallet_address

        return Response(data)


    @extend_schema(description="Buy a property from the blockchain.")
    @action(detail=True, methods=['post'], url_path='buy')
    def buy_property(self, request, pk=None):
        """
        Buy a property (single buyer).
        Expects: { "buyer_wallet": "0x...", "price": ... }
        """
        property_instance = self.get_object()
        buyer_wallet = request.data.get("buyer_wallet")
        price = request.data.get("price")  # in ETH

        if not buyer_wallet or not price:
            return Response({"error": "buyer_wallet and price required"}, status=400)

        # Blockchain interaction
        try:
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

            # Get blockchain propertyId
            blockchain_property_id = property_instance.blockchain_property_id
            price_in_wei = w3.toWei(price, 'ether')

            # Assume seller is the current owner wallet
            seller_wallet = property_instance.owners.first().wallet_address
            if not seller_wallet:
                return Response({"error": "Property has no owner"}, status=400)
            
            tx_hash = contract.functions.transferToSingleBuyer(
                int(blockchain_property_id), buyer_wallet
            ).transact({'from': seller_wallet, 'value': price_in_wei})

            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            # Update backend owner
            buyer_user = UserProfile.objects.get(wallet_address=buyer_wallet)
            property_instance.owners.clear()
            property_instance.owners.add(buyer_user)
            property_instance.save()

            return Response({"message": "Property bought successfully", "tx_hash": tx_hash.hex()}, status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @extend_schema(description="Invest in a property (crowdfund).")
    @action(detail=True, methods=['post'], url_path='invest')
    def invest_property(self, request, pk=None):
        """
        Invest in a property (crowdfund).
        Expects: { "investor_wallet": "0x...", "amount": ... }
        """
        property_instance = self.get_object()
        investor_wallet = request.data.get("investor_wallet")
        amount = request.data.get("amount")  # in ETH

        if not investor_wallet or not amount:
            return Response({"error": "investor_wallet and amount required"}, status=400)

        try:
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

            blockchain_property_id = property_instance.blockchain_property_id
            amount_in_wei = w3.toWei(amount, 'ether')

            tx_hash = contract.functions.invest(int(blockchain_property_id)).transact({
                'from': investor_wallet,
                'value': amount_in_wei
            })
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            return Response({"message": "Investment successful", "tx_hash": tx_hash.hex()}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    @extend_schema(description="Get investors")
    @action(detail=True, methods=['get'], url_path='investors')
    def get_investors(self, request, pk=None):
        """
        Get the list and count of investors for this property from the blockchain.
        """
        property_instance = self.get_object()
        try:
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

            blockchain_property_id = property_instance.blockchain_property_id
            investors = contract.functions.getInvestors(int(blockchain_property_id)).call()
            return Response({
                "investors": investors,
                "count": len(investors)
            }, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        
    


def sell_to_single_person(owner_id = None, owners_id: list = None, buyer = None, property_id = None, price = None, eth_price=None, contract = None):
    try:
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        # Owner id is the seller with the property, then get the blockchain wallet address of the person
        seller = owner_id
        buyer = buyer  # This should be the blockchain wallet address of the buyer  
        price_in_wei = w3.toWei(eth_price, 'ether')  # Convert to wei if needed
        # Connect to ganache 
        if owner_id == None and owners_id == None:
            return "Owner not selected"
        
        if buyer == None:
            return "Buyer not selected"
        
        # Assuming contract is already connected to the blockchain
        # Call the smart contract function to transfer ownership
        # This is a placeholder, replace with actual contract function call
        # Example: contract.functions.transferToSingleBuyer(property_id, buyer).transact({'from': seller, 'value': price_in_wei})
        # Connect to Ganache

        # one to one
        if buyer != None and owner_id != None:
            tx_hash = contract.functions.transferToSingleBuyer(property_id, buyer).transact({
                'from': seller,
                'value': price_in_wei
            })
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        # many to one
        elif buyer != None and owner_id == None and owners_id != None:
            
            tx_hash = contract.functions.buyFromMultiple(
                property_id,
                [owner1, owner2, owner3]
            ).transact({'from': buyer, 'value': price_in_wei})
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Backend to handle implementation
        property = Property.objects.get(reference_id = property_id)
        owner = CustomUser.objects.get(id = owner_id)
        property.owners.add(owner_id)
        property.blockchain_tx_hash = tx_hash.hex()  # Save the transaction hash
        property.save()

    except Property.DoesNotExist:
        return "Property does not exist"
    
    except Exception as e:
        return "Error occurred"

def sell_to_multiple_people(owner_id = None, owners_id: list = None, buyers: list = None, property_id = None, price = None, eth_price=None, contract = None):
    try:
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        seller = owner_id
        owners = owners  # This should be a list of blockchain wallet addresses of the owners
        price_in_wei = w3.toWei(eth_price, 'ether')  # Convert to wei if needed
        # Connect to ganache
        if owner_id == None and owners_id == None:
            return "Owner not selected"
        
        if buyers == None:
            return "Buyers not selected"
        
        # Assuming contract is already connected to the blockchain
        # Call the smart contract function to fractionalize ownership
        # This is a placeholder, replace with actual contract function call
        # Example: contract.functions.fractionalize(property_id, buyers, shares).transact({'from': seller, 'value': price_in_wei})
        # Connect to Ganache

        # one to many
        if owner_id != None and buyers != None and owners == None:
            tx_hash = contract.functions.fractionalize(
                property_id,
                [investor1, investor2, investor3],
                [3000, 4000, 3000]  # sum must be 10000
            ).transact({'from': owner})
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        
        elif buyers != None and owners != None and owner_id == None:
            # Assuming owners is a list of user IDs and buyers is a list of user IDs
            # price should be in wei if using Ethereum
            
            # many to many

            tx_hash = contract.functions.redistributeShares(
                property_id,
                [investorA, investorB],
                [6000, 4000]
            ).transact({'from': admin})
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


        # Backend to handle implementation
        property = Property.objects.get(reference_id = property_id)
        owner = CustomUser.objects.get(id = owner_id)
        property.owners.add(*owners_id)
        property.blockchain_tx_hash = tx_hash.hex()  # Save the transaction hash
        property.save()
        

    except Property.DoesNotExist:
        return "Property does not exist"

    except Exception as e:
        return "Error occurred"

def sell_property(owner = None, buyer = None, owners = None, buyers = None, property_id = None, price = None):
    """
    Sell a property to a single buyer.
    :param owner: The current owner of the property.
    :param buyer: The new buyer of the property.
    :param owners: List of owners (if multiple).
    :param buyers: List of buyers (if multiple).
    :param property_id: ID of the
    """

    eth_price = price/2700
    folder = ['P:\\', 'decentralized_ai_realestate', 'blockchain', 'artifacts', 'contracts', 'PropertyCrowdfund.sol']
    with open(os.path.join(*folder, 'PropertyCrowdfund.json')) as f:
        contract_json = json.load(f)

    contract_abi = contract_json["abi"]
    contract_address = config("PROPERTYCROWDFUND_CONTRACTADDRESS")
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    
    if owner == None and owners == None:
        return Response({"message": "Owner(s) not selected"})
    
    elif owner != None and owners == None:
        if buyer != None and buyers == None:
            w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
            price_in_wei = w3.toWei(eth_price, 'ether')  # Convert to wei if needed
            # Call the smart contract function to transfer ownership
            """ tx_hash = contract.functions.transferToSingleBuyer(property_id, buyer).transact({
                'from': owner,
                'value': price_in_wei
            })
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)  """

            sold = sell_to_single_person(owner_id=owner, buyer=buyer, property_id=property_id, price = price, eth_price=eth_price, contract=contract)
            if sold:
                return Response({"message": "Property has been sold"}, status = status.HTTP_200_OK)
            
        elif buyer == None and buyers != None:
            # Sell to multiple people
            # Assuming owners is a list of user IDs and buyers is a list of user IDs
            # price should be in wei if using Ethereum
            # tx_hash = contract.functions.fractionalize(
            #     property_id,
            #     buyers,  # List of buyer addresses
            #     [1000] * len(buyers)  # Example: equal shares, adjust as needed
            # ).transact({'from': owner})
            sold = sell_to_multiple_people(owner_id = owner, buyers=buyers, property_id = property_id, price = price, eth_price=eth_price, contract=contract)
            if sold:
                return Response({"message": "Property has been sold"}, status = status.HTTP_200_OK)
            
    elif owner == None and owners != None:
        if buyer != None and buyers == None:
            # Sell to a single person
            # Assuming owner is a single user ID and buyer is a single user ID
            # price should be in wei if using Ethereum
            # price_in_wei = Web3.toWei(price, 'ether')  # Convert to wei if needed
            # Call the smart contract function to transfer ownership
            # tx_hash = contract.functions.transferToSingleBuyer(property_id, buyer).transact({
            #     'from': owner,
            #     'value': price_in_wei
            # })
            # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash) 
            sold = sell_to_single_person(owners=owners, buyer=buyer, property_id=property_id, price = price, eth_price=eth_price, contract=contract)
            if sold:
                return Response({"message": "Property has been sold"}, status = status.HTTP_200_OK)
            
        elif buyer == None and buyers != None:
            # Sell to multiple people
            # Assuming owners is a list of user IDs and buyers is a list of user IDs
            # price should be in wei if using Ethereum
            # tx_hash = contract.functions.fractionalize(
            #     property_id,
            #     buyers,  # List of buyer addresses
            #     [1000] * len(buyers)  # Example: equal shares, adjust as needed
            # ).transact({'from': owner})
            sold = sell_to_multiple_people(owners = owners, buyers=buyers, property_id = property_id, price = price, eth_price=eth_price, contract=contract)
            if sold:
                return Response({"message": "Property has been sold"}, status = status.HTTP_200_OK)



""" 
class PropertyViewSet(viewsets.ModelViewSet):
    ""
    ViewSet for managing Property objects.
    ""
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Prepare input for prediction
        prediction_input = {
            'apartment_total_area': data.get('total_area'),
            'apartment_living_area': data.get('usable_area'),
            'apartment_rooms': data.get('bedrooms') + data.get('bathrooms'),
            'apartment_bedrooms': data.get('bedrooms'),
            'apartment_bathrooms': data.get('bathrooms'),
            'building_age': 8,
            'building_total_floors': data.get('total_floors'),
            'apartment_floor': data.get('floor_number'),
            'country_encoded': data.get('country_encoded'),
            'price_per_sqm': data.get('price_per_sqm'),
        }

        # Call the prediction function directly (not as an API call)
        try:
            #from ai_integration.train_and_register_model import load_model_and_predict
            # Simulate a request object for the prediction function
            #class DummyRequest:
            data = prediction_input
            ##prediction_response = load_model_and_predict(data)
            mypredict_price(prediction_input)
            # If using DRF Response, get .data
            if hasattr(prediction_response, 'data'):
                prediction = prediction_response.data.get('predictions')
            else:
                prediction = prediction_response
            data['price_prediction'] = prediction
        except Exception as e:
            data['price_prediction'] = None
            data['prediction_error'] = str(e)

        return Response(data)

 """


""" def mypredict_price(data):
    ""
    Predict real estate prices using the trained model.
    ""
    input_data = data
    # If country_encoded is a string or label, encode it. If it's already an int, skip.
    if isinstance(input_data['country_encoded'], str):
        le = LabelEncoder()
        input_data['country_encoded'] = le.fit_transform([input_data['country_encoded']])[0]
    # Make predictions
    predictions = load_model_and_predict(input_data)
    # If predictions is a DRF Response, extract .data
    if hasattr(predictions, 'data'):
        return predictions.data.get('predictions', [None])[0]
    # If it's a numpy array or list
    if isinstance(predictions, (list, tuple)) or hasattr(predictions, 'tolist'):
        return predictions[0] if len(predictions) else None
    return predictions """



import datetime

def predict_price_from_dict(input_data):
    """
    Takes a dict of features, returns a list of price predictions for the next 5 years.
    Each entry: {year: YYYY, price: ...}
    """
    import pandas as pd
    import joblib
    import os

    # Load the trained model
    model_path = 'xgboost_model.pkl'
    if not os.path.exists(model_path):
        raise FileNotFoundError("Trained model file not found. Please train the model first.")

    model = joblib.load(model_path)

    current_year = datetime.datetime.now().year
    predictions = []

    for i in range(5):
        year = current_year + i
        # Optionally, increment building_age for each year
        input_copy = input_data.copy()
        if input_copy.get('building_age') is not None:
            input_copy['building_age'] = input_copy['building_age'] + i
            input_copy['price_per_sqm'] = float(input_copy['price_per_sqm']) * (1 + 0.02 * i)  # Example: 2% annual increase
        
        # Convert to DataFrame for prediction
        df = pd.DataFrame([input_copy])
        price = model.predict(df)[0]
        print(model.predict(df))
        # Append the prediction
        predictions.append({"year": year, "price": float(price)})

    return predictions




""" 
def predict_price_from_dict(input_data):
    ""
    Pure function: takes a dict of features, returns prediction (not a DRF Response).
    ""
    import pandas as pd
    import joblib
    import os

    # Load the trained model
    model_path = 'xgboost_model.pkl'
    if not os.path.exists(model_path):
        raise FileNotFoundError("Trained model file not found. Please train the model first.")

    # Convert input data to DataFrame if it's a dictionary
    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])

    # Make predictions
    model = joblib.load(model_path)
    predictions = model.predict(input_data)
    return predictions[0] if len(predictions) else None
 """

@api_view(["POST"])
def predict_price(data):
    """
    Predict real estate prices using the trained model.
    """
    input_data = data
    # If country_encoded is a string or label, encode it. If it's already an int, skip.
    if isinstance(input_data['country_encoded'], str):
        le = LabelEncoder()
        input_data['country_encoded'] = le.fit_transform([input_data['country_encoded']])[0]
    # Use the pure function
    return predict_price_from_dict(input_data)



#@api_view(["POST"])
def mypredict_price(request):
    """
    API endpoint to predict real estate prices using the trained model.
    """
    input_data = request.data
    le = LabelEncoder()
    input_data['country_encoded'] = le.transform([input_data['country_encoded']])[0]
    print(input_data)


    try:
        # Make predictions
        predictions = load_model_and_predict(input_data)
        print("prediction", predictions)
        return Response({"predictions": predictions.tolist()}, status=status.HTTP_200_OK)
    except FileNotFoundError as e:
        print("File error", str(e))
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        print("error here", str(e))
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["POST"])
def load_model_and_predict(request):
    """
    Load the trained model and make predictions on the input data.
    :param input_data: A dictionary or DataFrame containing the input features.
    :return: Predicted values.
    """
    raw_data = request.data
    input_data = {
        key: float(raw_data[key][0] if isinstance(raw_data[key], list) else raw_data[key])
        for key in raw_data
    }
    # Load the trained model
    model_path = 'xgboost_model.pkl'
    if not os.path.exists(model_path):
        raise FileNotFoundError("Trained model file not found. Please train the model first.")

    model = joblib.load(model_path)

    print(input_data)
    # Convert input data to DataFrame if it's a dictionary
    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])

    # Ensure input data has the same features as the training data
    required_features = [
        'apartment_total_area', 'apartment_living_area', 'apartment_rooms',
        'apartment_bedrooms', 'apartment_bathrooms', 'building_age',
        'building_total_floors', 'apartment_floor', 'country_encoded',
        'price_per_sqm'
    ]
    #missing_features = [feature for feature in required_features if feature not in input_data]
    #if missing_features:
    #    raise ValueError(f"Missing required features: {missing_features}")

    # Make predictions
    predictions = model.predict(input_data)
    return Response({"predictions": predictions})
    #return predictions
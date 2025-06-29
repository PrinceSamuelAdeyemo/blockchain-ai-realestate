from django.db import models
from django.db.models import Count, Case, When, IntegerField
from transactions import Transaction
from tokenization.models import TokenOwnership
import uuid
from django.db.models import F
from web3 import Web3
from django.db import transaction
# Create your models here.





class ContractEvent(models.Model):
    # Core Identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract = models.ForeignKey("smartcontract.SmartContract", on_delete=models.CASCADE)
    transaction = models.ForeignKey("transactions.Transaction", on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    event_signature = models.CharField(max_length=66)
    block_number = models.IntegerField()
    log_index = models.IntegerField()
    arguments = models.JSONField()
    raw_data = models.JSONField()
    processed = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    property_id = models.ForeignKey(
        "property.Property", on_delete=models.CASCADE
    , null=True, blank=True, related_name='contract_events'
    )
    @classmethod
    def create_from_web3_event(cls, contract, web3_event):
        """Create DB record from Web3 event"""
        with transaction.atomic():
            tx_obj, _ = Transaction.objects.get_or_create(
                blockchain_tx_hash=web3_event['transactionHash'].hex(),
                defaults={
                    'transaction_type': 'CONTRACT_EVENT',
                    'status': 'COMPLETED',
                    'blockchain_network': contract.network
                }
            )
            
            return cls.objects.create(
                contract=contract,
                transaction=tx_obj,
                event_name=web3_event['event'],
                event_signature=Web3.keccak(text=f"{web3_event['event']}(...)").hex(),
                block_number=web3_event['blockNumber'],
                log_index=web3_event['logIndex'],
                arguments=dict(web3_event['args']),
                raw_data=dict(web3_event)
            )
    
    def process_event(self):
        """Handle specific event types"""
        if self.event_name == 'OwnershipTransferred':
            self._process_ownership_change()
        elif self.event_name == 'DividendPaid':
            self._process_dividend()
        self.processed = True
        self.save()
    
    def _process_ownership_change(self):
        from .models import TokenOwnership
        # Update ownership records
        TokenOwnership.objects.filter(
            asset__contract=self.contract
        ).update(
            is_verified=False
        )
         
class SmartContract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    contract_type = models.CharField(max_length=50)
    address = models.CharField(max_length=42, unique=True)
    abi = models.JSONField()
    network = models.CharField(max_length=50)
    deployer = models.CharField(max_length=42)
    deployment_tx = models.CharField(max_length=66, null=True, blank=True)
    deployment_block = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def deploy_to_blockchain(self):
        from web3 import Web3
        from .utils import get_web3_provider
        
        w3 = get_web3_provider(self.network)
        
        # Prepare contract
        contract = w3.eth.contract(
            abi=self.abi.abi_json,
            bytecode=self.abi.bytecode
        )
        
        # Build transaction
        tx_hash = contract.constructor().transact({
            'from': self.deployer,
            'gas': 5000000
        })
        
        # Wait for receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Update record
        self.address = tx_receipt.contractAddress
        self.deployment_tx = tx_hash.hex()
        self.deployment_block = tx_receipt.blockNumber
        self.save()
        
        return tx_receipt
    
    
class GasFeeRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    network = models.CharField(max_length=50)
    transaction_hash = models.CharField(max_length=66)
    block_number = models.IntegerField()
    gas_price = models.DecimalField(max_digits=30, decimal_places=0)
    gas_used = models.DecimalField(max_digits=30, decimal_places=0)
    gas_limit = models.DecimalField(max_digits=30, decimal_places=0)
    usd_cost = models.DecimalField(max_digits=20, decimal_places=8)
    block_time = models.DateTimeField()
    
    @classmethod
    def analyze_network_fees(cls, network, days=30):
        from django.db.models import Avg, Max, Min
        from datetime import datetime, timedelta
        
        date_threshold = datetime.now() - timedelta(days=days)
        
        return cls.objects.filter(
            network=network,
            block_time__gte=date_threshold
        ).aggregate(
            avg_gas_price=Avg('gas_price'),
            max_gas_price=Max('gas_price'),
            min_gas_price=Min('gas_price'),
            avg_usd_cost=Avg('usd_cost'),
            efficiency_ratio=Avg(F('gas_used') / F('gas_limit'))
        )
        
"""   
class MaintenanceRequest(models.Model):
    # ... (existing fields) ...
    
    @classmethod
    def forecast_yearly_costs(cls, property_id):
        from django.db.models import Sum
        from statsmodels.tsa.arima.model import ARIMA
        import pandas as pd
        
        # Get historical data
        history = cls.objects.filter(
            property_id=property_id,
            completed_date__isnull=False
        ).annotate(
            month=TruncMonth('completed_date')
        ).values('month').annotate(
            total_cost=Sum('actual_cost')
        ).order_by('month')
        
        # Convert to time series
        df = pd.DataFrame(list(history))
        df.set_index('month', inplace=True)
        df = df.resample('M').asfreq().fillna(0)
        
        # ARIMA forecasting
        model = ARIMA(df['total_cost'], order=(1,1,1))
        results = model.fit()
        forecast = results.forecast(steps=12)
        
        return {
            'history': df.to_dict(),
            'forecast': forecast.to_dict(),
            'model_summary': str(results.summary())
        }
        
    
    
class MaintenanceRequest(models.Model):
    # ... (existing fields) ...
    
    @classmethod
    def predict_future_requests(cls, property_id):
        from sklearn.ensemble import RandomForestClassifier
        import pandas as pd
        
        # Prepare training data
        history = cls.objects.filter(property_id=property_id).values(
            'priority', 'area', 'created_at__month'
        )
        df = pd.DataFrame(list(history))
        
        # Feature engineering
        df = pd.get_dummies(df, columns=['priority', 'area'])
        
        # Train model
        X = df.drop(columns=['created_at__month'])
        y = df['created_at__month']
        
        model = RandomForestClassifier()
        model.fit(X, y)
        
        # Predict next 3 months
        future_months = pd.date_range(
            start=datetime.now(),
            periods=3,
            freq='M'
        ).month.tolist()
        
        return {
            'predicted_requests': dict(zip(future_months, model.predict_proba(X)[0])),
            'feature_importance': dict(zip(X.columns, model.feature_importances_))
        }
        
        
"""
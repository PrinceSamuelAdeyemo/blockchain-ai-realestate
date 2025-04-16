from django.db import models
from django.db.models import Count, Case, When, IntegerField
# Create your models here.




class Lease(models.Model):
    # ... (existing fields) ...
    
    def create_renewal_offer(self):
        """Generate a new lease with 1-year extension"""
        if self.status != 'ACTIVE':
            raise ValueError("Only active leases can be renewed")
            
        return Lease.objects.create(
            property=self.property,
            tenant=self.tenant,
            lease_type=self.lease_type,
            start_date=self.end_date + timedelta(days=1),
            end_date=self.end_date + timedelta(days=365),
            monthly_rent=self.monthly_rent * Decimal('1.03'),  # 3% increase
            security_deposit=self.security_deposit,
            payment_due_day=self.payment_due_day,
            document=self.document  # Copy previous document
        )
    
    def generate_rent_statement(self):
        """Create PDF rent statement"""
        from reportlab.pdfgen import canvas
        from io import BytesIO
        
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        
        # PDF generation logic
        p.drawString(100, 800, f"RENT STATEMENT - {self.property.title}")
        p.drawString(100, 780, f"Tenant: {self.tenant.full_name}")
        p.drawString(100, 760, f"Period: {datetime.now().strftime('%B %Y')}")
        p.drawString(100, 740, f"Amount Due: ${self.monthly_rent}")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return buffer
    
    
from web3 import Web3
from django.db import transaction

class ContractEvent(models.Model):
    # ... (existing fields) ...
    
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
    
    def get_maintenance_priority_stats(property_id=None):
    
    
        queryset = MaintenanceRequest.objects.all()
        if property_id:
            queryset = queryset.filter(property_id=property_id)
        
        return queryset.annotate(
            priority_value=Case(
                When(priority='URGENT', then=4),
                When(priority='HIGH', then=3),
                When(priority='MEDIUM', then=2),
                When(priority='LOW', then=1),
                output_field=IntegerField()
            )
        ).values('priority').annotate(
            count=Count('id'),
            avg_days_to_complete=Avg(
                F('completed_date') - F('created_at'),
                output_field=DurationField()
            ),
            avg_cost=Avg('actual_cost')
        ).order_by('-priority_value')
        
        
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
        
        
class SmartContract(models.Model):
    # ... (existing fields) ...
    
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
    # ... (existing fields) ...
    
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
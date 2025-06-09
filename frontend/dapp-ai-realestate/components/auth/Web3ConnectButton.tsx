import { useWeb3Auth } from '@/providers/Web3AuthProvider';
import { Button } from '../ui/Button';
import { shortenAddress } from '@/lib/web3/utils';

export const Web3ConnectButton = () => {
  const { account, connect, disconnect, isAuthenticated } = useWeb3Auth();

  const handleConnect = async () => {
    if (window.ethereum ) {
      try {
        console.log("A")
        await connect();
        console.log("B")
      } catch (error) {
        console.error('Error reconnecting wallet:', error);
      }
    }
    

   /*  try {
      console.log("hhhhhh")
      await connect();
    } catch (error) {
      console.error('Error connecting wallet:', error);
    } */
  };

  return (
    <div>
      {isAuthenticated && account ? (
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium">{shortenAddress(account)}</span>
          <Button variant="outline" className='bg-blue-700' onClick={disconnect}>
            Disconnect
          </Button>
        </div>
      ) : (
        <Button type='button' onClick={handleConnect}>Connect Wallet</Button>
      )}
    </div>
  );
};
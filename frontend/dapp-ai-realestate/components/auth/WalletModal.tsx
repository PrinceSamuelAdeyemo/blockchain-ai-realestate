import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../ui/Dialog';
import { Button } from '../ui/Button';
import Image from 'next/image';

interface WalletModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (wallet: 'metamask' | 'walletconnect') => void;
}

export const WalletModal = ({ isOpen, onClose, onSelect }: WalletModalProps) => {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Connect Wallet</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <Button
            variant="outline"
            className="w-full flex items-center justify-start gap-3 py-6"
            onClick={() => onSelect('metamask')}
          >
            <Image
              src="/wallets/metamask.png"
              alt="MetaMask"
              width={32}
              height={32}
            />
            <span>MetaMask</span>
          </Button>
          <Button
            variant="outline"
            className="w-full flex items-center justify-start gap-3 py-6"
            onClick={() => onSelect('walletconnect')}
          >
            <Image
              src="/wallets/walletconnect.png"
              alt="WalletConnect"
              width={32}
              height={32}
            />
            <span>WalletConnect</span>
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};
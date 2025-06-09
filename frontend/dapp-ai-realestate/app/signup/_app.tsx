import type { AppProps } from 'next/app';
import { GoogleOAuthProvider } from '@react-oauth/google';
import '../styles/globals.css';

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <GoogleOAuthProvider clientId="YOUR_GOOGLE_CLIENT_ID">
      <Component {...pageProps} />
    </GoogleOAuthProvider>
  );
}


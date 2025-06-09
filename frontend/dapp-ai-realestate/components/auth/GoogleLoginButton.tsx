'use client';

import { GoogleLogin, CredentialResponse } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';
import axios from 'axios';
import api from '@/lib/auth/axios';

interface DecodedToken {
  email: string;
  name: string;
  picture: string;
  sub: string;
}

export default function GoogleLoginButton() {
  const handleLogin = async (credentialResponse: CredentialResponse) => {
    if (credentialResponse.credential) {
        const decoded: DecodedToken = jwtDecode(credentialResponse.credential);
        console.log('Decoded User:', decoded);

        try {
            const res = await api.post(`/core/api/google/validate/`, {
            token: credentialResponse.credential,

            });
            console.log('Backend Response:', res.data);
        } catch (err) {
            console.error('Login error:', err);
        }
        }
    };

    return (
        <GoogleLogin
        onSuccess={handleLogin}
        onError={() => console.log('Login Failed')}
        />
    );
}


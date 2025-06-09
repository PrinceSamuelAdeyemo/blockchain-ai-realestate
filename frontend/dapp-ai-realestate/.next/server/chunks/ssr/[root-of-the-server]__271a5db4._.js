module.exports = {

"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}}),
"[externals]/node:crypto [external] (node:crypto, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("node:crypto", () => require("node:crypto"));

module.exports = mod;
}}),
"[externals]/stream [external] (stream, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("stream", () => require("stream"));

module.exports = mod;
}}),
"[externals]/http [external] (http, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("http", () => require("http"));

module.exports = mod;
}}),
"[externals]/url [external] (url, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("url", () => require("url"));

module.exports = mod;
}}),
"[externals]/punycode [external] (punycode, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("punycode", () => require("punycode"));

module.exports = mod;
}}),
"[externals]/https [external] (https, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("https", () => require("https"));

module.exports = mod;
}}),
"[externals]/zlib [external] (zlib, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("zlib", () => require("zlib"));

module.exports = mod;
}}),
"[externals]/events [external] (events, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("events", () => require("events"));

module.exports = mod;
}}),
"[externals]/net [external] (net, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("net", () => require("net"));

module.exports = mod;
}}),
"[externals]/tls [external] (tls, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("tls", () => require("tls"));

module.exports = mod;
}}),
"[externals]/crypto [external] (crypto, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("crypto", () => require("crypto"));

module.exports = mod;
}}),
"[externals]/buffer [external] (buffer, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("buffer", () => require("buffer"));

module.exports = mod;
}}),
"[project]/lib/web3/utils.ts [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname } = __turbopack_context__;
{
__turbopack_context__.s({
    "getConnectedAccounts": (()=>getConnectedAccounts),
    "getWeb3Instance": (()=>getWeb3Instance),
    "shortenAddress": (()=>shortenAddress),
    "switchNetwork": (()=>switchNetwork)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$web3$2f$lib$2f$esm$2f$index$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$module__evaluation$3e$__ = __turbopack_context__.i("[project]/node_modules/web3/lib/esm/index.js [app-ssr] (ecmascript) <module evaluation>");
;
const getWeb3Instance = async ()=>{
    if ("TURBOPACK compile-time falsy", 0) {
        "TURBOPACK unreachable";
    }
    // Non-dapp browsers or no wallet installed
    console.log('Non-Ethereum browser detected. Consider installing MetaMask!');
    return null;
};
const getConnectedAccounts = async (web3)=>{
    return await web3.eth.getAccounts();
};
const shortenAddress = (address, chars = 4)=>{
    return `${address.substring(0, chars + 2)}...${address.substring(address.length - chars)}`;
};
const switchNetwork = async (web3, chainId)=>{
    if (!window.ethereum) throw new Error('MetaMask not installed');
    try {
        await window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [
                {
                    chainId: web3.utils.toHex(chainId)
                }
            ]
        });
    } catch (error) {
        // This error code indicates that the chain has not been added to MetaMask
        if (error.code === 4902) {
            throw new Error('Network not added to MetaMask');
        }
        throw error;
    }
};
}}),
"[project]/lib/web3/auth.ts [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname } = __turbopack_context__;
{
__turbopack_context__.s({
    "connectWallet": (()=>connectWallet),
    "signMessage": (()=>signMessage),
    "verifySignature": (()=>verifySignature)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$web3$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/lib/web3/utils.ts [app-ssr] (ecmascript)");
;
const connectWallet = async ()=>{
    const web3 = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$web3$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getWeb3Instance"])();
    if (!web3) throw new Error('Web3 not initialized');
    const accounts = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$web3$2f$utils$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["getConnectedAccounts"])(web3);
    if (accounts.length === 0) throw new Error('No accounts found');
    return {
        web3,
        account: accounts[0],
        chainId: await web3.eth.getChainId()
    };
};
const signMessage = async (web3, account, message)=>{
    return await web3.eth.personal.sign(message, account, '');
};
const verifySignature = async (web3, message, signature, address)=>{
    const recoveredAddress = await web3.eth.personal.ecRecover(message, signature);
    return recoveredAddress.toLowerCase() === address.toLowerCase();
};
}}),
"[project]/utils/env.ts [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname } = __turbopack_context__;
{
__turbopack_context__.s({
    "apiUrl": (()=>apiUrl)
});
let getEnvVariables = ()=>{
    if (process.env.NEXT_PUBLIC_ENV === 'production') {
        return {
            apiUrl: 'https://api.example.com'
        };
    } else if (process.env.NEXT_PUBLIC_ENV === 'staging') {
        return {
            apiUrl: 'https://staging-api.example.com'
        };
    } else {
        return {
            apiUrl: 'http://localhost:8000'
        };
    }
};
const { apiUrl } = getEnvVariables();
}}),
"[project]/providers/Web3AuthProvider.tsx [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname } = __turbopack_context__;
{
__turbopack_context__.s({
    "Web3AuthProvider": (()=>Web3AuthProvider),
    "useWeb3Auth": (()=>useWeb3Auth)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$web3$2f$auth$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/lib/web3/auth.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$utils$2f$env$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/utils/env.ts [app-ssr] (ecmascript)");
"use client";
;
;
;
;
const Web3AuthContext = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["createContext"])(undefined);
const Web3AuthProvider = ({ children })=>{
    const [web3, setWeb3] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [account, setAccount] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [chainId, setChainId] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [authToken, setAuthToken] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const connect = async ()=>{
        console.log("apiUrl triggered", __TURBOPACK__imported__module__$5b$project$5d2f$utils$2f$env$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["apiUrl"]);
        try {
            const { web3, account, chainId } = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$web3$2f$auth$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["connectWallet"])();
            setWeb3(web3);
            setAccount(account);
            setChainId(chainId);
            // Generate a signature for backend verification
            // Step 1: Request a nonce from the backend
            console.log("account", account);
            console.log("apiUrl", __TURBOPACK__imported__module__$5b$project$5d2f$utils$2f$env$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["apiUrl"]);
            console.log("web3", web3);
            const nonceResponse = await fetch(`${__TURBOPACK__imported__module__$5b$project$5d2f$utils$2f$env$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["apiUrl"]}/core/api/auth/nonce`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    address: account
                })
            });
            if (!nonceResponse.ok) {
                throw new Error('Failed to fetch nonce');
            }
            const { nonce } = await nonceResponse.json();
            const message = `Sign this message to verify your wallet: ${nonce}`;
            const signature = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$web3$2f$auth$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["signMessage"])(web3, account, nonce);
            /* // In a real app, you would send this to your backend for verification
      const isValid = await verifySignature(web3, message, signature, account);
      if (isValid) {
        setAuthToken(signature); // In production, use a proper JWT from your backend
      } */ // Step 3: Verify the signature with the backend
            const verifyResponse = await fetch(`${__TURBOPACK__imported__module__$5b$project$5d2f$utils$2f$env$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["apiUrl"]}/core/api/auth/verify`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    address: account,
                    signature: signature,
                    message: nonce
                })
            });
            console.log("Message", message);
            console.log("Signature", signature);
            console.log("Account", account);
            if (!verifyResponse.ok) {
                throw new Error('Signature verification failed');
            }
            const { success, token } = await verifyResponse.json();
            if (success) {
                setAuthToken(token); // Use the token provided by the backend
            }
            // Listen for account changes
            if (window.ethereum) {
                window.ethereum.on('accountsChanged', (accounts)=>{
                    if (accounts.length > 0) {
                        setAccount(accounts[0]);
                    } else {
                        disconnect();
                    }
                });
                window.ethereum.on('chainChanged', ()=>{
                    window.location.reload();
                });
            }
        } catch (error) {
            console.error('Error connecting wallet:', error);
            throw error;
        }
    };
    const disconnect = ()=>{
        setWeb3(null);
        setAccount(null);
        setChainId(null);
        setAuthToken(null);
    };
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        // Check if wallet is already connected when component mounts
        const checkConnectedWallet = async ()=>{
            if (window.ethereum && window.ethereum.selectedAddress) {
                try {
                    await connect();
                } catch (error) {
                    console.error('Error reconnecting wallet:', error);
                }
            }
        };
        checkConnectedWallet();
        return ()=>{
            if (window.ethereum) {
                window.ethereum.removeAllListeners();
            }
        };
    }, []);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Web3AuthContext.Provider, {
        value: {
            web3,
            account,
            chainId,
            connect,
            disconnect,
            isAuthenticated: !!authToken,
            authToken
        },
        children: children
    }, void 0, false, {
        fileName: "[project]/providers/Web3AuthProvider.tsx",
        lineNumber: 133,
        columnNumber: 5
    }, this);
};
const useWeb3Auth = ()=>{
    const context = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useContext"])(Web3AuthContext);
    if (context === undefined) {
        throw new Error('useWeb3Auth must be used within a Web3AuthProvider');
    }
    return context;
};
}}),
"[next]/internal/font/google/inter_59dee874.module.css [app-ssr] (css module)": ((__turbopack_context__) => {

var { g: global, __dirname } = __turbopack_context__;
{
__turbopack_context__.v({
  "className": "inter_59dee874-module__9CtR0q__className",
});
}}),
"[next]/internal/font/google/inter_59dee874.js [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": (()=>__TURBOPACK__default__export__)
});
var __TURBOPACK__imported__module__$5b$next$5d2f$internal$2f$font$2f$google$2f$inter_59dee874$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__ = __turbopack_context__.i("[next]/internal/font/google/inter_59dee874.module.css [app-ssr] (css module)");
;
const fontData = {
    className: __TURBOPACK__imported__module__$5b$next$5d2f$internal$2f$font$2f$google$2f$inter_59dee874$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].className,
    style: {
        fontFamily: "'Inter', 'Inter Fallback'",
        fontStyle: "normal"
    }
};
if (__TURBOPACK__imported__module__$5b$next$5d2f$internal$2f$font$2f$google$2f$inter_59dee874$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].variable != null) {
    fontData.variable = __TURBOPACK__imported__module__$5b$next$5d2f$internal$2f$font$2f$google$2f$inter_59dee874$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].variable;
}
const __TURBOPACK__default__export__ = fontData;
}}),
"[externals]/next/dist/server/app-render/action-async-storage.external.js [external] (next/dist/server/app-render/action-async-storage.external.js, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("next/dist/server/app-render/action-async-storage.external.js", () => require("next/dist/server/app-render/action-async-storage.external.js"));

module.exports = mod;
}}),
"[externals]/next/dist/server/app-render/work-unit-async-storage.external.js [external] (next/dist/server/app-render/work-unit-async-storage.external.js, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("next/dist/server/app-render/work-unit-async-storage.external.js", () => require("next/dist/server/app-render/work-unit-async-storage.external.js"));

module.exports = mod;
}}),
"[externals]/next/dist/server/app-render/work-async-storage.external.js [external] (next/dist/server/app-render/work-async-storage.external.js, cjs)": (function(__turbopack_context__) {

var { g: global, __dirname, m: module, e: exports } = __turbopack_context__;
{
const mod = __turbopack_context__.x("next/dist/server/app-render/work-async-storage.external.js", () => require("next/dist/server/app-render/work-async-storage.external.js"));

module.exports = mod;
}}),
"[project]/app/layout.tsx [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": (()=>RootLayout)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
/* import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
 */ var __TURBOPACK__imported__module__$5b$project$5d2f$providers$2f$Web3AuthProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/providers/Web3AuthProvider.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$next$5d2f$internal$2f$font$2f$google$2f$inter_59dee874$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[next]/internal/font/google/inter_59dee874.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/navigation.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$react$2d$oauth$2f$google$2f$dist$2f$index$2e$esm$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/@react-oauth/google/dist/index.esm.js [app-ssr] (ecmascript)");
"use client";
;
;
;
;
;
;
function RootLayout({ children }) {
    const pathname = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["usePathname"])();
    const needsWallet = pathname.startsWith('/wallet') || pathname.startsWith('/buy');
    console.log('needsWallet:', needsWallet);
    console.log('google client id', ("TURBOPACK compile-time value", "231777452986-na670ui90tkp1euml42hqaamdgrd5lra.apps.googleusercontent.com"));
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("html", {
        lang: "en",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("body", {
            className: __TURBOPACK__imported__module__$5b$next$5d2f$internal$2f$font$2f$google$2f$inter_59dee874$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].className,
            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f40$react$2d$oauth$2f$google$2f$dist$2f$index$2e$esm$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["GoogleOAuthProvider"], {
                clientId: ("TURBOPACK compile-time value", "231777452986-na670ui90tkp1euml42hqaamdgrd5lra.apps.googleusercontent.com"),
                children: needsWallet ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$providers$2f$Web3AuthProvider$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Web3AuthProvider"], {
                    children: children
                }, void 0, false, {
                    fileName: "[project]/app/layout.tsx",
                    lineNumber: 70,
                    columnNumber: 13
                }, this) : children
            }, void 0, false, {
                fileName: "[project]/app/layout.tsx",
                lineNumber: 68,
                columnNumber: 9
            }, this)
        }, void 0, false, {
            fileName: "[project]/app/layout.tsx",
            lineNumber: 67,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/app/layout.tsx",
        lineNumber: 66,
        columnNumber: 5
    }, this);
}
}}),

};

//# sourceMappingURL=%5Broot-of-the-server%5D__271a5db4._.js.map
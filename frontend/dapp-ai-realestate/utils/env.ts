
let getEnvVariables = () => {
    if (process.env.NEXT_PUBLIC_ENV === 'production') {
        return {
        apiUrl: 'https://api.example.com', // Replace with your production API URL
        }
    } else if (process.env.NEXT_PUBLIC_ENV === 'staging') {
        return {
        apiUrl: 'https://staging-api.example.com', // Replace with your staging API URL
        }
    } else {
        return {
        apiUrl: 'http://localhost:8000', // Replace with your local development API URL
        }
    }  
}

export const { apiUrl } = getEnvVariables()
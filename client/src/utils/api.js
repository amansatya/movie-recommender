import axios from "axios";

const baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
    baseURL,
    timeout: 180000,
    headers: {
        "Content-Type": "application/json",
    },
});

api.interceptors.request.use(
    (config) => {
        console.log(`🚀 [API REQUEST] ${config.method?.toUpperCase()} ${config.url}`);
        return config;
    },
    (error) => {
        console.error("❌ [API REQUEST ERROR]", error);
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    (response) => {
        console.log(`✅ [API RESPONSE] ${response.status} from ${response.config.url}`);
        return response;
    },
    (error) => {
        if (error.code === "ECONNABORTED") {
            console.error("⏱️ Request timed out after 3 minutes.");
        } else if (error.response) {
            console.error(`⚠️ Server responded with ${error.response.status}:`, error.response.data);
        } else {
            console.error("❌ Network/Server Error:", error.message);
        }
        return Promise.reject(error);
    }
);

export default api;

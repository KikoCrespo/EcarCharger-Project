import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';

axios.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest.__isRetryRequest) {
            originalRequest.__isRetryRequest = true;
            const refresh = sessionStorage.getItem('refresh');

            if (!refresh) {
                router.push('/login');
                return Promise.reject(error);
            }

            try {
                const res = await axios.post('/token/refresh/', { refresh });
                const newAccess = res.data.access;
                sessionStorage.setItem('access', newAccess);

                originalRequest.headers['Authorization'] = `Bearer ${newAccess}`;
                return axios(originalRequest);
            } catch (err) {
                sessionStorage.clear();
                router.push('/login');
                return Promise.reject(err);
            }
        }

        return Promise.reject(error);
    }
);


const axiosInterceptor = axios;
export default axiosInterceptor;

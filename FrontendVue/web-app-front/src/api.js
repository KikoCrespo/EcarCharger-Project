import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
});

export const login = async (email, password) => {
    try {
        const response = await api.post('login/', {
            u_email: email,
            u_password: password
        });
        return response.data;
    } catch (error) {
        return { error: error.response?.data?.error || "Erro ao fazer login" };
    }
};

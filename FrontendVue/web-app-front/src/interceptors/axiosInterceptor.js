import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000/api/',
})

// Adiciona o token a todas as requests
api.interceptors.request.use(config => {
    const access = sessionStorage.getItem('access')
    if (access) {
        config.headers['Authorization'] = `Bearer ${access}`
    }
    return config
})

// Interceptor de resposta para lidar com 401 e renovar token
api.interceptors.response.use(response => response,
    async error => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            const refresh = sessionStorage.getItem('refresh')
            if (!refresh) {
                window.location.href = '/login'
                return Promise.reject(error)
            }

            try {
                const res = await axios.post('http://localhost:8000/api/token/refresh/', {
                    refresh: refresh
                })

                const newAccess = res.data.access
                sessionStorage.setItem('access', newAccess)

                originalRequest.headers['Authorization'] = `Bearer ${newAccess}`
                return api(originalRequest)
            } catch (err) {
                sessionStorage.clear()
                window.location.href = '/login'
                return Promise.reject(err)
            }
        }

        return Promise.reject(error)
    }
)

export default api

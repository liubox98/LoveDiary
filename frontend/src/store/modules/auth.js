import axios from '@/plugins/axios';

const initialState = {
    isAuthenticated: false,
    user: null,
};

// 从本地存储获取值，如果没有则使用初始状态
const storedIsAuthenticated = localStorage.getItem('isAuthenticated');
const storedUser = JSON.parse(localStorage.getItem('user'));

const state = {
    isAuthenticated: storedIsAuthenticated !== null ? JSON.parse(storedIsAuthenticated) : initialState.isAuthenticated,
    user: storedUser !== null ? storedUser : initialState.user,
};

export default {
    state,
    mutations: {
        setAuthentication(state, isAuthenticated) {
            state.isAuthenticated = isAuthenticated;
        },
        setUser(state, user) {
            state.user = user;
        },
    },
    actions: {
        async login({ commit }, credentials) {
            try {
                const response = await axios.post('/token', credentials);

                if (response && response.data && response.data.access_token) {
                    const user = parseUserFromResponse(response.data);
                    commit('setAuthentication', true);
                    commit('setUser', user);

                    // 保存到本地存储
                    localStorage.setItem('isAuthenticated', true);
                    localStorage.setItem('user', JSON.stringify(user));

                    return { success: true, user };
                } else {
                    throw new Error('Invalid response format');
                }
            } catch (error) {
                console.error('Login failed:', error);
                throw error;
            }
        },
    },
    getters: {
        isAuthenticated: (state) => state.isAuthenticated,
        currentUser: (state) => state.user,
    },
};

function parseUserFromResponse(responseData) {
    // 解析用户信息的逻辑
    return responseData.user || null;
}

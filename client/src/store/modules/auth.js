import axios from '@/plugins/axios';

const LOCAL_STORAGE_KEYS = {
    isAuthenticated: 'isAuthenticated',
    user: 'user',
};

const initialState = {
    isAuthenticated: false,
    user: null,
};

const storedIsAuthenticated = localStorage.getItem(LOCAL_STORAGE_KEYS.isAuthenticated);
const storedUser = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEYS.user));

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
                    localStorage.setItem(LOCAL_STORAGE_KEYS.isAuthenticated, true);
                    localStorage.setItem(LOCAL_STORAGE_KEYS.user, JSON.stringify(user));
                    return { success: true, user };
                } else {
                    throw new Error('Invalid response format');
                }
            } catch (error) {
                console.error('Login error:', error.message);
                return { success: false, error: error.message };
            }
        },
    },
    getters: {
        isAuthenticated: (state) => state.isAuthenticated,
        currentUser: (state) => state.user,
    },
};

function parseUserFromResponse(responseData) {
    return responseData.user || null;
}

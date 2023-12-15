import axios from '@/plugins/axios';

const initialState = {
    isAuthenticated: false,
    user: null,
};

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
            const response = await axios.post('/token', credentials);
            if (response && response.data && response.data.access_token) {
                const user = parseUserFromResponse(response.data);
                commit('setAuthentication', true);
                commit('setUser', user);
                localStorage.setItem('isAuthenticated', true);
                localStorage.setItem('user', JSON.stringify(user));
                return { success: true, user };
            } else {
                return false
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

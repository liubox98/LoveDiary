import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';
import LoginView from '@/components/LoginView.vue';
import ActivitiesList from '@/components/ActivitiesList.vue';

const routes = [
    {
        path: '/',
        name: 'LoginView',
        component: LoginView,
    },
    {
        path: '/ActivitiesList',
        name: 'ActivitiesList',
        component: ActivitiesList,
        meta: { requiresAuth: true },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    const isAuthenticated = store.getters['isAuthenticated'];
    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/');
    } else {
        next();
    }
});

export default router;

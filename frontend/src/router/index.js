import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';
import LoginView from '@/components/LoginView.vue';
import ActivitiesList from '@/components/ActivitiesList.vue';

const routes = [
    {
        path: '/',
        name: 'LoginView',
        component: LoginView,
        meta: { title: 'Login -NOTE' }
    },
    {
        path: '/ActivitiesList',
        name: 'ActivitiesList',
        component: ActivitiesList,
        meta: { title: 'Index -NOTE', requiresAuth: true },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {

    // 设置页面标题
    document.title = to.meta.title || 'Default Title';
    const isAuthenticated = store.getters['isAuthenticated'];

    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/');
    } else {
        next();
    }
});

export default router;

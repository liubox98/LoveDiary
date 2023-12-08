<template>
    <div>
        <van-form @submit="submitLogin">
            <h2>Login</h2>
            <van-field v-model="loginData.username" label="Username" placeholder="Enter your username" required />
            <van-field v-model="loginData.password" type="password" label="Password" placeholder="Enter your password"
                required />
            <van-button type="primary" native-type="submit">
                Login
            </van-button>
        </van-form>
    </div>
</template>
  
<script>
export default {
    data() {
        return {
            loginData: {
                username: '',
                password: '',
            },
        };
    },
    methods: {
        async submitLogin() {
            const response = await this.$store.dispatch('login', this.loginData);
            if (response && response.success) {
                this.$router.push('/ActivitiesList');
            } else {
                // 处理登录失败的逻辑
            }
        },
    }
}
</script>
  
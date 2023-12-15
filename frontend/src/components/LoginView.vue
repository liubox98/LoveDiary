<template>
    <div>
        <h2>Login</h2>
        <el-form :model="loginData" :rules="rules" ref="loginForm">
            <el-form-item prop="username">
                <el-input v-model="loginData.username" placeholder="username" />
            </el-form-item>
            <el-form-item prop="password">
                <el-input v-model="loginData.password" type="password" placeholder="password" show-password />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitLogin">LOGIN</el-button>
            </el-form-item>
        </el-form>
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
            rules: {
                username: [{ required: true, message: 'Please input username', trigger: 'blur' }],
                password: [{ required: true, message: 'Please input password', trigger: 'blur' }],
            },
        };
    },
    methods: {
        async submitLogin() {

            try {
                await this.$refs.loginForm.validate();
                const response = await this.$store.dispatch('login', this.loginData);
                if (response && response.success) {
                    this.$router.push('/ActivitiesList');
                    this.$message.success('This is a success message.');
                } else {
                    this.$message.error('Oops, this is an error message.');
                }
            } catch (error) {
                this.$message.warning('Warning, this is a warning message.');
            }
        },
    },
};
</script>
  
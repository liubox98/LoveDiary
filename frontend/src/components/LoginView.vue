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
          <el-button type="primary" @click="submitLogin" :loading="loading">LOGIN</el-button>
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
        loading: false,
      };
    },
    methods: {
      async submitLogin() {
        try {
          // 启用 loading 状态
          this.loading = true;
          await this.$refs.loginForm.validate();
          const response = await this.$store.dispatch('login', this.loginData);
          console.log('response', response)
          if (response && response.success) {
            this.$router.push('/ActivitiesList');
            this.$message.success('Login successful.');
          } else {
            this.$message.error('Invalid username or password.');
          }
        } catch (error) {
          this.$message.warning('An error occurred.');
        } finally {
          // 禁用 loading 状态
          this.loading = false;
        }
      },
    },
  };
  </script>
  
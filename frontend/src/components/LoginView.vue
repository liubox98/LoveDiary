<template>
  <div class="container">
    <div class="login-container">
      <img src="@/assets/logo.png" alt="Logo" class="logo" />
      <h2>Login</h2>
      <el-form :model="loginData" ref="loginForm" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="loginData.username" placeholder="Username" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginData.password" type="password" placeholder="Password" show-password />
        </el-form-item>
        <el-form-item class="login-button">
          <el-button type="primary" @click="submitLogin" :loading="loading">Login</el-button>
        </el-form-item>
      </el-form>
    </div>
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
      loading: false,
    };
  },
  methods: {
    async submitLogin() {
      try {
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
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* 使用 Bootstrap 的容器样式 */
.container {
  width: 100%;
  max-width: 100vw;
  padding: 0 20px;
  /* 添加一些水平间距 */
  box-sizing: border-box;
  /* 防止 padding 影响宽度 */
  margin: 0 auto;
}

.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

.logo {
  width: 80%;
  /* 使用百分比宽度，响应式设计 */
  max-width: 100px;
  /* 设置一个最大宽度 */
  height: auto;
}

.login-form {
  width: 100%;
  max-width: 240px;
}

.login-button {
  text-align: center;
}</style>

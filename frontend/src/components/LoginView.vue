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
        if (response && response.success) {
          this.$router.push('/ActivitiesList');
        } else {
          this.$message.error('检查用户名或密码');
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
.container {
  width: 100%;
  max-width: 100vw;
  padding: 0 20px;
  box-sizing: border-box;
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
  max-width: 100px;
  height: auto;
}

.login-form {
  width: 100%;
  max-width: 240px;
}

.login-button {
  text-align: center;
}
</style>

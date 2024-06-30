<template>
  <div class="command-container">
    <h2>沙箱仿真设计平台</h2>
    <input v-model="address" placeholder="输入IP地址或域名（包含http/https）" />
    <button @click="startMitmWebAndRad">开始爬取</button>
    <button @click="saveFlows">保存</button>
    <button @click="startMitm">启动</button>
    <div v-if="responses.length > 0" class="response-container">
      <h3>输出</h3>
      <div v-for="(response, index) in responses" :key="index">
        <h4>命令: {{ response.command }}</h4>
        <pre>stdout: {{ response.stdout }}</pre>
        <pre>stderr: {{ response.stderr }}</pre>
        <pre>返回代码: {{ response.returncode }}</pre>
        <pre v-if="response.error">错误: {{ response.error }}</pre>
      </div>
    </div>
    <div v-if="error" class="error">
      <h3>错误</h3>
      <pre>{{ error }}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      address: '',
      responses: [],
      error: null
    };
  },
  methods: {
    async startMitmWebAndRad() {
      if (!this.address || !this.validateAddress(this.address)) {
        this.error = '请输入正确的IP地址或域名格式（包含http/https）';
        return;
      }

      this.clearFeedback();
      try {
        const res = await axios.post('http://localhost:5050/execute_combined', { address: this.address });
        this.responses = res.data;
      } catch (error) {
        this.error = error.response ? error.response.data : error.message;
      }
    },
    async saveFlows() {
      this.clearFeedback();
      try {
        const res = await axios.post('http://localhost:5050/save');
        this.responses = [res.data];
      } catch (error) {
        this.error = error.response ? error.response.data : error.message;
      }
    },
    async startMitm() {
      this.clearFeedback();
      try {
        const res = await axios.post('http://localhost:5050/start');
        this.responses = [res.data];
      } catch (error) {
        this.error = error.response ? error.response.data : error.message;
      }
    },
    validateAddress(addr) {
      const urlRegex = /^(http|https):\/\/[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/;
      return urlRegex.test(addr);
    },
    clearFeedback() {
      this.responses = [];
      this.error = null;
    }
  }
};
</script>

<style scoped>
.command-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

h2 {
  margin-bottom: 20px;
}

input {
  width: calc(100% - 22px);
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  display: inline-block;
  padding: 10px 20px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

button:hover {
  background-color: #0056b3;
}

.response-container {
  margin-top: 20px;
}

h3 {
  margin-top: 20px;
}

pre {
  background-color: #eee;
  padding: 10px;
  border-radius: 4px;
}

.error {
  color: red;
  margin-top: 20px;
}
</style>

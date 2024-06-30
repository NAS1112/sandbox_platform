<template>
  <div class="background-container">
    <div class="command-container">
      <h2>沙箱仿真设计平台</h2>
      <div class="input-container">
        <input v-model="address" placeholder="输入IP地址或域名（包含http/https）" />
      </div>
      <button :class="{'scan-button-start': !isScanning, 'scan-button-stop': isScanning}" @click="toggleScan">
        {{ isScanning ? '停止爬取' : '开始爬取' }}
      </button>
      <button :class="{'service-button-start': !isServiceRunning, 'service-button-stop': isServiceRunning}" @click="toggleService">
        {{ isServiceRunning ? '停止服务' : '启动服务' }}
      </button>
      <input type="file" ref="fileInput" style="display:none" @change="uploadFile" />
      <div v-if="responses.length > 0" class="response-container">
        <h3>输出</h3>
        <div v-for="(response, index) in responses" :key="index" class="response-item">
          <h4>命令: {{ response.command }}</h4>
          <pre v-html="formatOutput(response.stdout)"></pre>
          <pre v-html="formatOutput(response.stderr)"></pre>
          <p>返回代码: {{ response.returncode }}</p>
          <p v-if="response.error" class="error">错误: {{ response.error }}</p>
        </div>
      </div>
      <div v-if="error" class="error">
        <h3>错误</h3>
        <pre>{{ error }}</pre>
      </div>
      <div v-if="success" class="success">
        <h3>执行成功</h3>
        <button v-if="serviceUrl" @click="redirectToService">跳转到服务</button>
      </div>
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
      error: null,
      success: false,
      serviceUrl: '',
      isScanning: false,
      isServiceRunning: false,
    };
  },
  methods: {
    async toggleScan() {
      if (this.isScanning) {
        this.stopScan();
      } else {
        this.startScan();
      }
    },
    async startScan() {
      if (!this.address || !this.validateAddress(this.address)) {
        this.error = '请输入正确的IP地址或域名格式（包含http/https）';
        return;
      }

      this.clearFeedback();
      this.isScanning = true;

      try {
        const res = await axios.post('http://localhost:5050/execute_combined', { address: this.address }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });

        if (res.data && Array.isArray(res.data)) {
          this.responses = res.data;
        } else {
          this.error = '返回数据格式错误';
        }
      } catch (error) {
        this.error = error.response ? error.response.data : error.message;
      }
    },
    async stopScan() {
      try {
        const res = await axios.post('http://localhost:5050/stop_scan');
        if (res.data.success) {
          alert(res.data.message);
          this.isScanning = false;
        } else {
          this.error = res.data.error;
        }
      } catch (error) {
        this.error = error.response ? error.response.data : error.message;
      }
    },
    async toggleService() {
      if (this.isServiceRunning) {
        this.stopService();
      } else {
        this.startService();
      }
    },
    async startService() {
      this.$refs.fileInput.click();
    },
    async uploadFile(event) {
      const file = event.target.files[0];
      if (!file) {
        this.error = '请选择要上传的文件';
        return;
      }

      this.clearFeedback();

      const formData = new FormData();
      formData.append('file', file);

      try {
        const res = await axios.post('http://localhost:5050/upload_file', formData);
        if (res.data.success) {
          const filename = res.data.filename;

          const startRes = await axios.post('http://localhost:5050/start_service', { filename }, {
            headers: {
              'Content-Type': 'application/json'
            }
          });

          if (startRes.data.success) {
            this.success = true;
            this.serviceUrl = `http://localhost:12355`;
            this.isServiceRunning = true;
          } else {
            this.error = startRes.data.error;
          }
        } else {
          this.error = res.data.error;
        }
      } catch (error) {
        this.error = error.response ? error.response.data : error.message;
      }
    },
    async stopService() {
      try {
        const res = await axios.post('http://localhost:5050/stop_service');
        if (res.data.success) {
          this.isServiceRunning = false;
          this.success = false; // 清除执行成功状态
          this.serviceUrl = ''; // 清除服务 URL
        } else {
          this.error = res.data.error;
        }
      } catch (error) {
        this.error = error.response ? error.response.data : error.message;
      }
    },
    validateAddress(addr) {
      const urlRegex = /^(http|https):\/\/[a-zA-Z0-9.-]+(:\d+)?(\/.*)?$/;
      return urlRegex.test(addr);
    },
    clearFeedback() {
      this.error = null;
      this.success = false;
      this.responses = [];
    },
    formatOutput(output) {
      return output ? output.replace(/\n/g, '<br>') : '';
    },
    redirectToService() {
      window.open(this.serviceUrl, '_blank');
    }
  }
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  background: url('@/assets/R2.gif') no-repeat center center fixed;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.background-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.command-container {
  background-color: rgba(255, 255, 255, 0.8);
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  max-width: 500px;
  width: 100%;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

.input-container {
  display: flex;
  justify-content: center;
}

input {
  padding: 10px;
  margin-bottom: 20px;
  width: 100%;
  max-width: 400px;
  border: 1px solid #ccc;
  border-radius: 5px;
  text-align: center;
}

button {
  padding: 10px 20px;
  margin: 5px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
  font-size: 16px;
}

.scan-button-start {
  background-color: green;
  color: white;
}

.scan-button-stop {
  background-color: red;
  color: white;
}

.service-button-start {
  background-color: blue;
  color: white;
}

.service-button-stop {
  background-color: red;
  color: white;
}

.loading {
  margin-top: 20px;
  font-size: 18px;
  font-weight: bold;
}

.response-container {
  margin-top: 20px;
  text-align: left;
  display: inline-block;
  max-height: 300px;
  overflow-y: auto;
  width: 100%;
}

.response-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.error {
  color: red;
}

.success {
  color: green;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>

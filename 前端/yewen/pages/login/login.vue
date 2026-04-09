<template>
  <view class="login-page">
    <!-- 背景装饰 -->
    <view class="bg-decoration">
      <view class="bg-blur"></view>
    </view>

    <!-- 顶部Logo区域 -->
    <view class="logo-section">
      <view class="logo-icon">
        <text class="logo-emoji">🌾</text>
      </view>
      <text class="app-name">叶问</text>
      <text class="app-slogan">智慧农业 · 精准防控</text>
    </view>

    <!-- 微信一键登录按钮 -->
    <view class="wechat-login-section">
      <button class="wechat-login-btn" @click="wechatLogin">
        <text class="wechat-icon">💚</text>
        <text class="wechat-text">微信一键登录</text>
      </button>
    </view>

    <!-- 其他登录方式分割线 -->
    <view class="divider">
      <view class="line"></view>
      <text class="divider-text">其他登录方式</text>
      <view class="line"></view>
    </view>

    <!-- 手机号密码登录入口 -->
    <view class="phone-login-entry" @click="showPhoneLogin = true">
      <text class="phone-icon">📱</text>
      <text class="phone-text">手机号密码登录</text>
      <text class="phone-arrow">›</text>
    </view>

    <!-- 协议提示 -->
    <view class="agreement">
      <view class="checkbox small" :class="{ checked: agreeProtocol }" @click="agreeProtocol = !agreeProtocol">
        <text v-if="agreeProtocol">✓</text>
      </view>
      <text>登录即代表同意</text>
      <text class="link" @click="showProtocol('user')">《用户协议》</text>
      <text>和</text>
      <text class="link" @click="showProtocol('privacy')">《隐私政策》</text>
    </view>

    <!-- 手机号密码登录弹窗 -->
    <view class="login-modal" v-if="showPhoneLogin" @click="showPhoneLogin = false">
      <view class="modal-content" @click.stop>
        <view class="modal-header">
          <text class="modal-title">手机号密码登录</text>
          <text class="modal-close" @click="showPhoneLogin = false">✕</text>
        </view>
        
        <view class="modal-body">
          <!-- 密码登录表单 -->
          <view class="login-form">
            <view class="input-group">
              <view class="input-icon">📱</view>
              <input 
                class="input-field" 
                v-model="loginForm.phone" 
                placeholder="请输入手机号"
                type="number"
              />
            </view>
            <view class="input-group">
              <view class="input-icon">🔒</view>
              <input 
                class="input-field" 
                v-model="loginForm.password" 
                placeholder="请输入密码"
                :type="showPassword ? 'text' : 'password'"
              />
              <view class="input-eye" @click="showPassword = !showPassword">
                <text>{{ showPassword ? '👁️' : '👁️‍🗨️' }}</text>
              </view>
            </view>
            <view class="form-options">
              <view class="remember" @click="rememberMe = !rememberMe">
                <view class="checkbox" :class="{ checked: rememberMe }">
                  <text v-if="rememberMe">✓</text>
                </view>
                <text>记住密码</text>
              </view>
              <text class="forgot" @click="forgotPassword">忘记密码？</text>
            </view>
            <button class="login-btn" @click="handlePasswordLogin">登 录</button>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // 协议同意
      agreeProtocol: true,
      
      // 手机号登录弹窗
      showPhoneLogin: false,
      
      // 密码登录表单
      loginForm: {
        phone: '',
        password: ''
      },
      
      // UI状态
      showPassword: false,
      rememberMe: false
    }
  },
  
  onLoad() {
    // 检查是否有保存的账号
    this.loadSavedAccount()
  },
  
  methods: {
    // 加载保存的账号
    loadSavedAccount() {
      const saved = uni.getStorageSync('saved_account')
      if (saved && saved.phone) {
        this.loginForm.phone = saved.phone
        this.loginForm.password = saved.password
        this.rememberMe = true
      }
    },
    
    // 保存账号
    saveAccount() {
      if (this.rememberMe) {
        uni.setStorageSync('saved_account', {
          phone: this.loginForm.phone,
          password: this.loginForm.password
        })
      } else {
        uni.removeStorageSync('saved_account')
      }
    },
    
    // 微信一键登录
    wechatLogin() {
      if (!this.agreeProtocol) {
        uni.showToast({ title: '请先同意用户协议', icon: 'none' })
        return
      }
      
      uni.showLoading({ title: '微信登录中...', mask: true })
      
      // 模拟微信登录（实际开发中调用 uni.login 获取 code 后传给后端）
      setTimeout(() => {
        uni.hideLoading()
        
        // 模拟登录成功
        const userInfo = {
          userId: 'USER_' + Date.now(),
          nickname: '微信用户',
          phone: '',
          avatar: 'https://picsum.photos/id/64/200/200',
          loginType: 'wechat',
          loginTime: new Date().toISOString()
        }
        
        uni.setStorageSync('user_info', userInfo)
        uni.setStorageSync('is_login', true)
        
        uni.showToast({ title: '登录成功', icon: 'success' })
        
        setTimeout(() => {
          uni.switchTab({ url: '/pages/index/index' })
        }, 500)
      }, 1000)
    },
    
    // 密码登录
    handlePasswordLogin() {
      if (!this.loginForm.phone) {
        uni.showToast({ title: '请输入手机号', icon: 'none' })
        return
      }
      if (!this.loginForm.password) {
        uni.showToast({ title: '请输入密码', icon: 'none' })
        return
      }
      
      uni.showLoading({ title: '登录中...', mask: true })
      
      setTimeout(() => {
        uni.hideLoading()
        
        // 演示环境，任意手机号+密码均可登录
        // 正式环境需调用后端接口验证
        const userInfo = {
          userId: 'USER_' + Date.now(),
          nickname: '农场主',
          phone: this.loginForm.phone,
          avatar: 'https://picsum.photos/id/64/200/200',
          loginType: 'phone',
          loginTime: new Date().toISOString()
        }
        
        uni.setStorageSync('user_info', userInfo)
        uni.setStorageSync('is_login', true)
        
        this.saveAccount()
        this.showPhoneLogin = false
        
        uni.showToast({ title: '登录成功', icon: 'success' })
        
        setTimeout(() => {
          uni.switchTab({ url: '/pages/index/index' })
        }, 500)
      }, 1000)
    },
    
    // 忘记密码
    forgotPassword() {
      uni.showModal({
        title: '找回密码',
        content: '请联系客服重置密码',
        confirmText: '联系客服',
        success: (res) => {
          if (res.confirm) {
            uni.showToast({ title: '客服电话: 400-123-4567', icon: 'none' })
          }
        }
      })
    },
    
    // 显示协议
    showProtocol(type) {
      const title = type === 'user' ? '用户协议' : '隐私政策'
      const content = type === 'user' 
        ? '欢迎使用病虫害识别助手！本应用致力于为用户提供专业的病虫害识别与防治建议服务。用户在使用本服务时应遵守相关法律法规，不得利用本服务进行任何违法活动。'
        : '我们重视您的隐私保护。我们会收集您的设备信息、使用记录等以提供更好的服务。我们不会将您的个人信息出售给第三方。'
      
      uni.showModal({
        title: title,
        content: content,
        showCancel: false,
        confirmText: '我知道了'
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #2c5e2a 0%, #4a9e46 50%, #2c5e2a 100%);
  position: relative;
  display: flex;
  flex-direction: column;
  padding-bottom: 40px;
}

/* 背景装饰 */
.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}
.bg-blur {
  position: absolute;
  top: -20%;
  left: -20%;
  width: 140%;
  height: 140%;
  background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 70%);
}

/* Logo区域 */
.logo-section {
  text-align: center;
  margin-top: 80px;
  margin-bottom: 50px;
  z-index: 1;
}
.logo-icon {
  width: 80px;
  height: 80px;
  background: rgba(255,255,255,0.2);
  border-radius: 24px;
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.3);
}
.logo-emoji {
  font-size: 48px;
}
.app-name {
  display: block;
  font-size: 28px;
  font-weight: bold;
  color: white;
  margin-bottom: 8px;
}
.app-slogan {
  display: block;
  font-size: 14px;
  color: rgba(255,255,255,0.8);
}

/* 微信登录按钮 */
.wechat-login-section {
  padding: 0 40px;
  margin-bottom: 30px;
  z-index: 1;
}
.wechat-login-btn {
  width: 100%;
  background: #07c160;
  border-radius: 50px;
  padding: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border: none;
  
  .wechat-icon {
    font-size: 24px;
  }
  
  .wechat-text {
    font-size: 16px;
    font-weight: 600;
    color: white;
  }
}
.wechat-login-btn::after {
  border: none;
}

/* 分割线 */
.divider {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 40px;
  margin-bottom: 24px;
  z-index: 1;
}
.line {
  flex: 1;
  height: 1px;
  background: rgba(255,255,255,0.3);
}
.divider-text {
  font-size: 13px;
  color: rgba(255,255,255,0.7);
}

/* 手机号登录入口 */
.phone-login-entry {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  margin: 0 40px 30px;
  background: rgba(255,255,255,0.15);
  border-radius: 50px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255,255,255,0.2);
  z-index: 1;
  
  .phone-icon {
    font-size: 20px;
  }
  
  .phone-text {
    font-size: 15px;
    color: white;
    font-weight: 500;
  }
  
  .phone-arrow {
    font-size: 18px;
    color: rgba(255,255,255,0.8);
  }
}

/* 协议 */
.agreement {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  margin-top: auto;
  font-size: 12px;
  color: rgba(255,255,255,0.7);
  z-index: 1;
  padding: 20px;
}
.agreement .link {
  color: #fff;
  text-decoration: underline;
}
.checkbox.small {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1px solid rgba(255,255,255,0.5);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: white;
}
.checkbox.small.checked {
  background: #07c160;
  border-color: #07c160;
}

/* 登录弹窗 */
.login-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  width: 85%;
  background: white;
  border-radius: 28px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 20px;
  border-bottom: 1px solid #f0f0e8;
}
.modal-title {
  font-size: 18px;
  font-weight: bold;
  color: #2c5e2a;
}
.modal-close {
  font-size: 24px;
  color: #999;
}
.modal-body {
  padding: 20px;
  overflow-y: auto;
}

/* 输入框 */
.input-group {
  display: flex;
  align-items: center;
  background: #f5f7f0;
  border-radius: 16px;
  padding: 12px 16px;
  margin-bottom: 16px;
}
.input-icon {
  font-size: 20px;
  margin-right: 12px;
}
.input-field {
  flex: 1;
  font-size: 15px;
  background: transparent;
}
.input-eye {
  padding: 4px 8px;
  font-size: 18px;
}

/* 表单选项 */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.remember {
  display: flex;
  align-items: center;
  gap: 8px;
}
.checkbox {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  border: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: white;
}
.checkbox.checked {
  background: #2c5e2a;
  border-color: #2c5e2a;
}
.forgot {
  color: #999;
  font-size: 13px;
}

/* 登录按钮 */
.login-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #2c5e2a, #3a7a36);
  color: white;
  border-radius: 40px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  margin-bottom: 10px;
}
</style>
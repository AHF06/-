<script>
export default {
  onLaunch: function() {
    console.log('App Launch')
    // 检查登录状态
    const isLogin = uni.getStorageSync('is_login')
    if (!isLogin) {
      // 未登录，但先不跳转，让首页自己处理
    }
  },
  onShow: function() {
    console.log('App Show')
  },
  onHide: function() {
    console.log('App Hide')
  }
}
</script>

<style>
/* 全局现代化样式 */
page {
  background-color: #f0f4ec;
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 4px;
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: rgba(44, 94, 42, 0.3);
  border-radius: 4px;
}

/* 平滑动画 */
view, button, image {
  transition: all 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* 禁用点击高亮 */
view {
  -webkit-tap-highlight-color: transparent;
}

/* 玻璃暗色效果 */
.glass-dark {
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(20px);
}
</style>
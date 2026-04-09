"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  data() {
    return {
      // 协议同意
      agreeProtocol: true,
      // 手机号登录弹窗
      showPhoneLogin: false,
      // 密码登录表单
      loginForm: {
        phone: "",
        password: ""
      },
      // UI状态
      showPassword: false,
      rememberMe: false
    };
  },
  onLoad() {
    this.loadSavedAccount();
  },
  methods: {
    // 加载保存的账号
    loadSavedAccount() {
      const saved = common_vendor.index.getStorageSync("saved_account");
      if (saved && saved.phone) {
        this.loginForm.phone = saved.phone;
        this.loginForm.password = saved.password;
        this.rememberMe = true;
      }
    },
    // 保存账号
    saveAccount() {
      if (this.rememberMe) {
        common_vendor.index.setStorageSync("saved_account", {
          phone: this.loginForm.phone,
          password: this.loginForm.password
        });
      } else {
        common_vendor.index.removeStorageSync("saved_account");
      }
    },
    // 微信一键登录
    wechatLogin() {
      if (!this.agreeProtocol) {
        common_vendor.index.showToast({ title: "请先同意用户协议", icon: "none" });
        return;
      }
      common_vendor.index.showLoading({ title: "微信登录中...", mask: true });
      setTimeout(() => {
        common_vendor.index.hideLoading();
        const userInfo = {
          userId: "USER_" + Date.now(),
          nickname: "微信用户",
          phone: "",
          avatar: "https://picsum.photos/id/64/200/200",
          loginType: "wechat",
          loginTime: (/* @__PURE__ */ new Date()).toISOString()
        };
        common_vendor.index.setStorageSync("user_info", userInfo);
        common_vendor.index.setStorageSync("is_login", true);
        common_vendor.index.showToast({ title: "登录成功", icon: "success" });
        setTimeout(() => {
          common_vendor.index.switchTab({ url: "/pages/index/index" });
        }, 500);
      }, 1e3);
    },
    // 密码登录
    handlePasswordLogin() {
      if (!this.loginForm.phone) {
        common_vendor.index.showToast({ title: "请输入手机号", icon: "none" });
        return;
      }
      if (!this.loginForm.password) {
        common_vendor.index.showToast({ title: "请输入密码", icon: "none" });
        return;
      }
      common_vendor.index.showLoading({ title: "登录中...", mask: true });
      setTimeout(() => {
        common_vendor.index.hideLoading();
        const userInfo = {
          userId: "USER_" + Date.now(),
          nickname: "农场主",
          phone: this.loginForm.phone,
          avatar: "https://picsum.photos/id/64/200/200",
          loginType: "phone",
          loginTime: (/* @__PURE__ */ new Date()).toISOString()
        };
        common_vendor.index.setStorageSync("user_info", userInfo);
        common_vendor.index.setStorageSync("is_login", true);
        this.saveAccount();
        this.showPhoneLogin = false;
        common_vendor.index.showToast({ title: "登录成功", icon: "success" });
        setTimeout(() => {
          common_vendor.index.switchTab({ url: "/pages/index/index" });
        }, 500);
      }, 1e3);
    },
    // 忘记密码
    forgotPassword() {
      common_vendor.index.showModal({
        title: "找回密码",
        content: "请联系客服重置密码",
        confirmText: "联系客服",
        success: (res) => {
          if (res.confirm) {
            common_vendor.index.showToast({ title: "客服电话: 400-123-4567", icon: "none" });
          }
        }
      });
    },
    // 显示协议
    showProtocol(type) {
      const title = type === "user" ? "用户协议" : "隐私政策";
      const content = type === "user" ? "欢迎使用病虫害识别助手！本应用致力于为用户提供专业的病虫害识别与防治建议服务。用户在使用本服务时应遵守相关法律法规，不得利用本服务进行任何违法活动。" : "我们重视您的隐私保护。我们会收集您的设备信息、使用记录等以提供更好的服务。我们不会将您的个人信息出售给第三方。";
      common_vendor.index.showModal({
        title,
        content,
        showCancel: false,
        confirmText: "我知道了"
      });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: common_vendor.o((...args) => $options.wechatLogin && $options.wechatLogin(...args), "fa"),
    b: common_vendor.o(($event) => $data.showPhoneLogin = true, "dc"),
    c: $data.agreeProtocol
  }, $data.agreeProtocol ? {} : {}, {
    d: $data.agreeProtocol ? 1 : "",
    e: common_vendor.o(($event) => $data.agreeProtocol = !$data.agreeProtocol, "24"),
    f: common_vendor.o(($event) => $options.showProtocol("user"), "32"),
    g: common_vendor.o(($event) => $options.showProtocol("privacy"), "9b"),
    h: $data.showPhoneLogin
  }, $data.showPhoneLogin ? common_vendor.e({
    i: common_vendor.o(($event) => $data.showPhoneLogin = false, "eb"),
    j: $data.loginForm.phone,
    k: common_vendor.o(($event) => $data.loginForm.phone = $event.detail.value, "49"),
    l: $data.showPassword ? "text" : "password",
    m: $data.loginForm.password,
    n: common_vendor.o(($event) => $data.loginForm.password = $event.detail.value, "a9"),
    o: common_vendor.t($data.showPassword ? "👁️" : "👁️‍🗨️"),
    p: common_vendor.o(($event) => $data.showPassword = !$data.showPassword, "43"),
    q: $data.rememberMe
  }, $data.rememberMe ? {} : {}, {
    r: $data.rememberMe ? 1 : "",
    s: common_vendor.o(($event) => $data.rememberMe = !$data.rememberMe, "49"),
    t: common_vendor.o((...args) => $options.forgotPassword && $options.forgotPassword(...args), "d9"),
    v: common_vendor.o((...args) => $options.handlePasswordLogin && $options.handlePasswordLogin(...args), "f9"),
    w: common_vendor.o(() => {
    }, "b5"),
    x: common_vendor.o(($event) => $data.showPhoneLogin = false, "c5")
  }) : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-e4e4508d"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/login/login.js.map

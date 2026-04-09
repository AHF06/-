"use strict";
const common_vendor = require("../../common/vendor.js");
const common_assets = require("../../common/assets.js");
const _sfc_main = {
  data() {
    return {
      // 整体背景图片（全局背景）
      bgImage: "https://images.pexels.com/photos/162240/barn-rural-nature-grange-162240.jpeg?auto=compress&cs=tinysrgb&w=800",
      // Hero区域背景图片（first.jpg）
      heroBgImage: "/static/first.jpg",
      greetingText: "早安，农场主",
      scrollHeight: 0,
      // 天气数据
      weatherIcon: "☀️",
      weatherTemp: 22,
      weatherDesc: "晴",
      currentLocation: "南京市",
      weatherHumidity: 65,
      weatherRainfall: 0,
      weatherWindSpeed: 8,
      weatherUV: 3,
      weatherTip: "今日天气晴朗，适合田间作业，注意防晒",
      // 弹窗控制
      showWeatherModal: false,
      recentRecords: [
        {
          id: 1,
          name: "水稻稻瘟病",
          date: "2026-04-01",
          severity: "严重",
          thumbnail: "https://picsum.photos/id/33/100/100"
        },
        {
          id: 2,
          name: "小麦条锈病",
          date: "2026-03-30",
          severity: "中等",
          thumbnail: "https://picsum.photos/id/32/100/100"
        },
        {
          id: 3,
          name: "玉米螟危害",
          date: "2026-03-28",
          severity: "轻度",
          thumbnail: "https://picsum.photos/id/31/100/100"
        }
      ]
    };
  },
  onLoad() {
    this.setGreeting();
    this.calcScrollHeight();
    this.getLocation();
    this.getWeather();
  },
  onShow() {
    this.checkLoginStatus();
    this.checkSyncData();
  },
  methods: {
    checkLoginStatus() {
      const isLogin = common_vendor.index.getStorageSync("is_login");
      const userInfo = common_vendor.index.getStorageSync("user_info");
      if (!isLogin || !userInfo) {
        setTimeout(() => {
          common_vendor.index.navigateTo({ url: "/pages/login/login" });
        }, 100);
      }
    },
    getLocation() {
      common_vendor.index.getLocation({
        type: "gcj02",
        success: (res) => {
          this.getCityName(res.latitude, res.longitude);
        },
        fail: () => {
          this.currentLocation = "南京市";
          this.getWeather();
        }
      });
    },
    getCityName(latitude, longitude) {
      this.currentLocation = "南京市";
      this.getWeather();
    },
    getWeather() {
      const weathers = [
        { icon: "☀️", temp: 28, desc: "晴", humidity: 45, rainfall: 0, windSpeed: 8, uv: 8, tip: "天气晴朗，适合田间作业，注意防晒" },
        { icon: "🌤️", temp: 24, desc: "晴转多云", humidity: 55, rainfall: 0, windSpeed: 10, uv: 6, tip: "天气较好，适合喷洒农药" },
        { icon: "☁️", temp: 20, desc: "多云", humidity: 65, rainfall: 0, windSpeed: 12, uv: 4, tip: "多云天气，注意田间通风" },
        { icon: "🌧️", temp: 18, desc: "小雨", humidity: 85, rainfall: 15, windSpeed: 10, uv: 2, tip: "有降雨，不适合露天作业，注意排水" }
      ];
      const randomIndex = Math.floor(Math.random() * weathers.length);
      const weather = weathers[randomIndex];
      this.weatherIcon = weather.icon;
      this.weatherTemp = weather.temp;
      this.weatherDesc = weather.desc;
      this.weatherHumidity = weather.humidity;
      this.weatherRainfall = weather.rainfall;
      this.weatherWindSpeed = weather.windSpeed;
      this.weatherUV = weather.uv;
      this.weatherTip = weather.tip;
    },
    refreshWeather() {
      common_vendor.index.showToast({ title: "正在刷新...", icon: "none" });
      setTimeout(() => {
        this.getWeather();
        common_vendor.index.showToast({ title: "已更新", icon: "success" });
      }, 1e3);
    },
    showWeatherDetail() {
      this.showWeatherModal = true;
    },
    setGreeting() {
      const hour = (/* @__PURE__ */ new Date()).getHours();
      if (hour < 6)
        this.greetingText = "凌晨好，农场主";
      else if (hour < 12)
        this.greetingText = "早安，农场主";
      else if (hour < 18)
        this.greetingText = "下午好，农场主";
      else
        this.greetingText = "晚上好，农场主";
    },
    calcScrollHeight() {
      const systemInfo = common_vendor.index.getSystemInfoSync();
      this.scrollHeight = systemInfo.windowHeight - 50;
    },
    loadSyncData() {
      const syncList = common_vendor.index.getStorageSync("sync_diseases") || [];
      if (syncList.length > 0) {
        const syncRecords = syncList.slice(0, 3).map((item) => ({
          id: item.id,
          name: item.description.substring(0, 20) + (item.description.length > 20 ? "..." : ""),
          date: item.time.split(" ")[0],
          severity: "待诊断",
          thumbnail: "https://picsum.photos/id/20/100/100",
          isSync: true,
          originalDesc: item.description
        }));
        this.recentRecords = [...syncRecords, ...this.recentRecords].slice(0, 5);
      }
    },
    checkSyncData() {
      const syncList = common_vendor.index.getStorageSync("sync_diseases") || [];
      if (syncList.length > 0) {
        const lastSync = syncList[0];
        const lastCheckTime = common_vendor.index.getStorageSync("last_sync_check") || 0;
        if (lastSync.id > lastCheckTime) {
          common_vendor.index.showToast({
            title: `📋 来自农友圈：${lastSync.description.substring(0, 15)}...`,
            icon: "none",
            duration: 2500
          });
          common_vendor.index.setStorageSync("last_sync_check", lastSync.id);
          this.loadSyncData();
        }
      }
    },
    openCamera() {
      const isLogin = common_vendor.index.getStorageSync("is_login");
      if (!isLogin) {
        common_vendor.index.showModal({
          title: "提示",
          content: "请先登录后再使用拍照识别功能",
          confirmText: "去登录",
          success: (res) => {
            if (res.confirm)
              common_vendor.index.navigateTo({ url: "/pages/login/login" });
          }
        });
        return;
      }
      common_vendor.index.chooseImage({
        count: 1,
        sourceType: ["camera"],
        success: (res) => {
          const tempFilePath = res.tempFilePaths[0];
          common_vendor.index.showLoading({ title: "识别中...", mask: true });
          setTimeout(() => {
            common_vendor.index.hideLoading();
            const resultData = {
              imageUrl: tempFilePath,
              diseaseName: "稻瘟病",
              latinName: "Pyricularia oryzae",
              confidence: 94,
              severity: "中度",
              pathogen: "稻瘟病菌",
              harmPart: "叶片、叶鞘、节、穗颈",
              conditions: "高温高湿、多雨天气、氮肥过量",
              agriculturalControl: ["选用抗病品种", "合理施肥，增施磷钾肥", "科学灌水，适时晒田"],
              chemicalControl: ["喷施75%三环唑2000-3000倍液", "或40%稻瘟灵乳油800-1000倍液"],
              notes: ["注意轮换用药", "遵守安全间隔期", "施药时做好个人防护"],
              similarDiseases: []
            };
            common_vendor.index.navigateTo({
              url: `/pages/result/result?data=${encodeURIComponent(JSON.stringify(resultData))}&imageUrl=${encodeURIComponent(tempFilePath)}`
            });
          }, 1500);
        },
        fail: () => {
          common_vendor.index.showToast({ title: "拍照失败", icon: "none" });
        }
      });
    },
    handleMacroWarning() {
      common_vendor.index.navigateTo({ url: "/pages/warning/warning" });
    },
    viewRecordDetail(item) {
      if (item.isSync && item.originalDesc) {
        common_vendor.index.showModal({
          title: "同步病情",
          content: item.originalDesc,
          confirmText: "开始诊断",
          success: (res) => {
            if (res.confirm)
              this.openCamera();
          }
        });
      } else {
        common_vendor.index.navigateTo({ url: `/pages/history/detail?id=${item.id}` });
      }
    },
    gotoHistory() {
      common_vendor.index.switchTab({ url: "/pages/history/history" });
    },
    openAssistant() {
      common_vendor.index.navigateTo({ url: "/pages/ai/ai" });
    }
  }
};
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
  return common_vendor.e({
    a: $data.bgImage,
    b: common_vendor.t($data.greetingText),
    c: common_vendor.t($data.weatherIcon),
    d: common_vendor.t($data.weatherTemp),
    e: common_vendor.t($data.weatherDesc),
    f: common_vendor.t($data.currentLocation),
    g: common_vendor.o((...args) => $options.showWeatherDetail && $options.showWeatherDetail(...args), "96"),
    h: common_vendor.o((...args) => $options.handleMacroWarning && $options.handleMacroWarning(...args), "36"),
    i: "url(" + $data.heroBgImage + ")",
    j: common_assets._imports_0$1,
    k: common_vendor.o((...args) => $options.openCamera && $options.openCamera(...args), "8a"),
    l: common_vendor.o((...args) => $options.gotoHistory && $options.gotoHistory(...args), "5a"),
    m: $data.recentRecords.length > 0
  }, $data.recentRecords.length > 0 ? {
    n: common_vendor.f($data.recentRecords, (item, idx, i0) => {
      return {
        a: item.thumbnail,
        b: common_vendor.t(item.name),
        c: common_vendor.t(item.date),
        d: common_vendor.t(item.severity),
        e: common_vendor.n(item.severity === "严重" ? "severe" : "mild"),
        f: idx,
        g: common_vendor.o(($event) => $options.viewRecordDetail(item), idx)
      };
    })
  } : {
    o: common_vendor.o((...args) => $options.gotoHistory && $options.gotoHistory(...args), "2e")
  }, {
    p: $data.scrollHeight + "px",
    q: common_assets._imports_0,
    r: common_vendor.o((...args) => $options.openAssistant && $options.openAssistant(...args), "c1"),
    s: $data.showWeatherModal
  }, $data.showWeatherModal ? {
    t: common_vendor.o(($event) => $data.showWeatherModal = false, "6c"),
    v: common_vendor.t($data.weatherIcon),
    w: common_vendor.t($data.weatherTemp),
    x: common_vendor.t($data.weatherDesc),
    y: common_vendor.t($data.currentLocation),
    z: common_vendor.t($data.weatherHumidity),
    A: common_vendor.t($data.weatherRainfall),
    B: common_vendor.t($data.weatherWindSpeed),
    C: common_vendor.t($data.weatherUV),
    D: common_vendor.t($data.weatherTip),
    E: common_vendor.o((...args) => $options.refreshWeather && $options.refreshWeather(...args), "eb"),
    F: common_vendor.o(() => {
    }, "0e"),
    G: common_vendor.o(($event) => $data.showWeatherModal = false, "73")
  } : {});
}
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["render", _sfc_render], ["__scopeId", "data-v-1cf27b2a"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/index/index.js.map

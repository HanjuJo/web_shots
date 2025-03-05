<template>
  <div class="settings-view">
    <div class="settings-header">
      <h1>설정</h1>
    </div>
    
    <div class="settings-content">
      <div class="settings-section">
        <h2>일반 설정</h2>
        <div class="form-group">
          <label>언어</label>
          <select class="form-control" v-model="settings.language">
            <option value="ko">한국어</option>
            <option value="en">English</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>테마</label>
          <select class="form-control" v-model="settings.theme">
            <option value="light">라이트</option>
            <option value="dark">다크</option>
          </select>
        </div>
      </div>
      
      <div class="settings-section">
        <h2>알림 설정</h2>
        <div class="form-check">
          <input type="checkbox" class="form-check-input" id="emailNotif" v-model="settings.notifications.email">
          <label class="form-check-label" for="emailNotif">이메일 알림</label>
        </div>
        
        <div class="form-check">
          <input type="checkbox" class="form-check-input" id="pushNotif" v-model="settings.notifications.push">
          <label class="form-check-label" for="pushNotif">푸시 알림</label>
        </div>
      </div>
      
      <div class="settings-actions">
        <button class="btn btn-primary" @click="saveSettings">
          <i class="fas fa-save"></i> 저장
        </button>
        <button class="btn btn-outline-secondary" @click="resetSettings">
          <i class="fas fa-undo"></i> 초기화
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsView',
  data() {
    return {
      settings: {
        language: 'ko',
        theme: 'light',
        notifications: {
          email: true,
          push: true
        }
      }
    }
  },
  methods: {
    saveSettings() {
      // Save settings logic will be implemented here
      console.log('Settings saved:', this.settings)
    },
    resetSettings() {
      // Reset settings logic will be implemented here
      this.settings = {
        language: 'ko',
        theme: 'light',
        notifications: {
          email: true,
          push: true
        }
      }
    }
  }
}
</script>

<style scoped>
.settings-view {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.settings-header {
  margin-bottom: 30px;
}

.settings-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.settings-actions {
  display: flex;
  gap: 10px;
  margin-top: 30px;
}

.form-check {
  margin-bottom: 10px;
}
</style>

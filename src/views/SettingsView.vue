&lt;template>
  &lt;div class="settings">
    &lt;div class="settings-container">
      &lt;h2>설정&lt;/h2>
      
      &lt;div class="settings-section">
        &lt;h3>계정 설정&lt;/h3>
        &lt;div class="setting-item">
          &lt;label>채널 ID&lt;/label>
          &lt;input type="text" v-model="channelId" placeholder="채널 ID를 입력하세요">
        &lt;/div>
        &lt;div class="setting-item">
          &lt;label>API 키&lt;/label>
          &lt;input type="password" v-model="apiKey" placeholder="YouTube API 키를 입력하세요">
        &lt;/div>
      &lt;/div>

      &lt;div class="settings-section">
        &lt;h3>알림 설정&lt;/h3>
        &lt;div class="setting-item">
          &lt;label class="checkbox-label">
            &lt;input type="checkbox" v-model="notifications.comments">
            새 댓글 알림
          &lt;/label>
        &lt;/div>
        &lt;div class="setting-item">
          &lt;label class="checkbox-label">
            &lt;input type="checkbox" v-model="notifications.subscribers">
            새 구독자 알림
          &lt;/label>
        &lt;/div>
        &lt;div class="setting-item">
          &lt;label class="checkbox-label">
            &lt;input type="checkbox" v-model="notifications.milestones">
            마일스톤 달성 알림
          &lt;/label>
        &lt;/div>
      &lt;/div>

      &lt;div class="settings-section">
        &lt;h3>데이터 표시&lt;/h3>
        &lt;div class="setting-item">
          &lt;label>기본 통계 기간&lt;/label>
          &lt;select v-model="defaultPeriod">
            &lt;option value="7">최근 7일&lt;/option>
            &lt;option value="28">최근 28일&lt;/option>
            &lt;option value="90">최근 90일&lt;/option>
            &lt;option value="365">최근 1년&lt;/option>
          &lt;/select>
        &lt;/div>
      &lt;/div>

      &lt;div class="button-group">
        &lt;button class="save-button" @click="saveSettings">
          &lt;i class="fas fa-save">&lt;/i> 설정 저장
        &lt;/button>
        &lt;button class="reset-button" @click="resetSettings">
          &lt;i class="fas fa-undo">&lt;/i> 초기화
        &lt;/button>
      &lt;/div>
    &lt;/div>
  &lt;/div>
&lt;/template>

&lt;script>
export default {
  name: 'SettingsView',
  data() {
    return {
      channelId: '',
      apiKey: '',
      notifications: {
        comments: true,
        subscribers: true,
        milestones: true
      },
      defaultPeriod: '28'
    }
  },
  methods: {
    saveSettings() {
      // TODO: API 연동
      console.log('설정 저장:', {
        channelId: this.channelId,
        apiKey: this.apiKey,
        notifications: this.notifications,
        defaultPeriod: this.defaultPeriod
      })
    },
    resetSettings() {
      this.channelId = ''
      this.apiKey = ''
      this.notifications = {
        comments: true,
        subscribers: true,
        milestones: true
      }
      this.defaultPeriod = '28'
    }
  }
}
&lt;/script>

&lt;style scoped>
.settings {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.settings-container {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
}

h2 {
  font-size: 1.875rem;
  color: #1f2937;
  margin-bottom: 2rem;
}

.settings-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.settings-section:last-child {
  border-bottom: none;
}

h3 {
  font-size: 1.25rem;
  color: #374151;
  margin-bottom: 1rem;
}

.setting-item {
  margin-bottom: 1rem;
}

label {
  display: block;
  font-size: 0.875rem;
  color: #4b5563;
  margin-bottom: 0.5rem;
}

input[type="text"],
input[type="password"],
select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

input[type="checkbox"] {
  width: 1rem;
  height: 1rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

button {
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.save-button {
  background-color: #6366f1;
  color: white;
  border: none;
}

.save-button:hover {
  background-color: #4f46e5;
}

.reset-button {
  background-color: white;
  color: #4b5563;
  border: 1px solid #d1d5db;
}

.reset-button:hover {
  background-color: #f3f4f6;
}

button i {
  font-size: 0.875rem;
}
&lt;/style>

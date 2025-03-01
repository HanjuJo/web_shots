<template>
  <section class="video-editor">
    <h2>AI 영상 편집</h2>
    <textarea v-model="inputText" placeholder="편집할 텍스트 입력"></textarea>
    <button @click="editVideo">편집 시작</button>
    <div v-if="result">
      <p>편집된 영상: {{ result.edited_video }}</p>
      <p>길이: {{ result.duration }}</p>
      <p>상태: {{ result.status }}</p>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  name: 'VideoEditor',
  data() {
    return {
      inputText: '',
      result: null
    };
  },
  methods: {
    async editVideo() {
      if (this.inputText) {
        try {
          const response = await axios.post('https://creatortool-backend-123-c965e7aaa680.herokuapp.com/api/edit_video', { text: this.inputText });
          this.result = response.data;
        } catch (error) {
          console.error('Error editing video:', error);
        }
      }
    }
  }
}
</script>

<style scoped>
.video-editor {
  margin: 40px;
  text-align: center;
}
textarea {
  width: 80%;
  height: 100px;
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>
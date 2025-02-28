<script>
import axios from 'axios';

export default {
  name: 'FeatureList',
  data() {
    return {
      features: []
    };
  },
  mounted() {
    axios.get('https://creatortool-backend-123-c965e7aaa680.herokuapp.com/api/features')
      .then(response => {
        this.features = response.data;
      })
      .catch(error => {
        console.error('Error fetching features:', error);
      });
  },
  methods: {
    getIconClass(index) {
      const icons = [
        'fab fa-youtube',
        'fas fa-video',
        'fas fa-closed-captioning',
        'fas fa-image'
      ];
      return icons[index];
    },
    getIconStyle(index) {
      const colors = [
        '#ff0000',
        '#007bff',
        '#007bff',
        '#007bff'
      ];
      return { color: colors[index] };
    }
  }
}
</script>
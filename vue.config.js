const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: 'localhost',
    port: 8080,
    hot: true,
    client: {
      webSocketURL: 'auto://0.0.0.0:0/ws',
      overlay: {
        errors: true,
        warnings: false
      }
    },
    proxy: {
      '/api': {
        target: 'http://localhost:5003',
        changeOrigin: true,
        ws: true
      }
    },
    headers: {
      'Content-Security-Policy': "default-src 'self' 'unsafe-inline' 'unsafe-eval' http://localhost:5003; img-src 'self' https: data:; font-src 'self' https: data:;"
    }
  },
  configureWebpack: {
    devtool: 'source-map',
    performance: {
      hints: false
    }
  }
})

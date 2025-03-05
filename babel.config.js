module.exports = {
  presets: [
    ['@vue/cli-plugin-babel/preset', {
      targets: {
        node: 'current'
      }
    }]
  ],
  assumptions: {
    privateFieldsAsProperties: true,
    setPublicClassFields: true
  },
  plugins: [
    ['@babel/plugin-transform-private-methods', { loose: true }],
    ['@babel/plugin-transform-class-properties', { loose: true }],
    ['@babel/plugin-transform-private-property-in-object', { loose: true }]
  ]
}

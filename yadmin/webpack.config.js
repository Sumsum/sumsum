var webpack = require('webpack')


var jsdir = __dirname + '/static/yadmin/dist/js/'
var uglifyOpts = {}


module.exports = {
  entry: {
    app: jsdir + 'app.js',
  },
  output: {
    path: jsdir,
    filename: "app.min.js"
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin(uglifyOpts)
  ]
}

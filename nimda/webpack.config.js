/* global __dirname */
var webpack = require('webpack')


var config = {
  entry: {
    main: './src/main.js',
    vendor: [
      'jquery',
      'select2',
      'bootstrap',
      './src/django',
      './src/sirtrevor/image-picker.js',
      './src/sirtrevor/image-picker.css',
      'vue',
      'vuex',
      'sortablejs',
      'dropzone',
      'dropzone/dist/dropzone.css', // messes things up
      'sir-trevor',
      'sir-trevor/build/sir-trevor.css',
      'ionicons/css/ionicons.css',
      'lodash'
    ]
  },
  output: {
    path: __dirname + '/../dist/nimda',
    publicPath: '/dist/nimda/',
    filename: '[name].js'
  },
  module: {
    loaders: [
      { test: require.resolve("jquery"), loader: "expose?$!expose?jQuery" },
      {
        test: /\.js$/,
        loader: 'babel',
        exclude: /node_modules|vue\/dist|vue-hot-reload-api|vue-loader/
      },
      {
        test: /\.vue$/,
        loader: 'vue'
      },
      {
        test: /\.(eot|svg|ttf|woff)/,
        loader: 'url-loader?limit=10000'
      },
      {
        test: /\.scss$/,
        //loader: ExtractTextPlugin.extract('style-loader', 'css-loader!sass-loader')
        loader: 'style-loader!css-loader!sass-loader'
      },
      {
        test: /\.css$/,
        //loader: ExtractTextPlugin.extract('style-loader', 'css-loader')
        loader: 'style-loader!css-loader'
      }
    ]
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin('vendor', 'vendor.bundle.js'),
    //new ExtractTextPlugin('[name].css')
  ]
}


module.exports = config

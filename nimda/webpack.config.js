/* global __dirname */
var webpack = require('webpack')


var config = {
  entry: {
    main: './src/main.js',
    vendor: [
      'jquery',
      'select2',
      'bootstrap',
      'lodash'
      './src/django',
      './src/adminlte',
    ]
  },
  output: {
    path: __dirname + '/../dist/nimda',
    publicPath: '/dist/nimda/',
    filename: '[name].js'
  },
  module: {
    rules: [{
      test: require.resolve('jquery'),
      use: [{
        loader: 'expose-loader',
        options: 'jQuery'
      },{
        loader: 'expose-loader',
        options: '$'
      }]
    }],
    loaders: [
      {
        test: /\.js$/,
        loader: 'babel-loader'
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
    new webpack.optimize.CommonsChunkPlugin({ name: 'vendor', filename: 'vendor.bundle.js' })
    //new ExtractTextPlugin('[name].css')
  ]
}


module.exports = config

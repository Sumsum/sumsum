/* global __dirname */
const webpack = require('webpack')
const ExtractTextPlugin = require('extract-text-webpack-plugin')


const DEBUG = process.env.NODE_ENV != 'production'
const extractCSS = new ExtractTextPlugin({
  filename: '[name].css',
})
const vendorBundle = new webpack.optimize.CommonsChunkPlugin({
  name: 'vendor',
})


let config = {
  entry: {
    main: [
      './src/main.js',
      './src/main.css',
    ],
    vendor: [
      'jquery',
      'select2',
      'select2/dist/css/select2.css',
      'bootstrap',
      'bootstrap/dist/css/bootstrap.css',
      'bootstrap-datepicker',
      'bootstrap-datepicker/dist/css/bootstrap-datepicker3.css',
      'bootstrap-timepicker',
      'bootstrap-timepicker/css/bootstrap-timepicker.css',
      'lodash',
      'font-awesome/css/font-awesome.css',
      'ionicons/dist/css/ionicons.css',
      'admin-lte/dist/js/app.js',
      'admin-lte/dist/css/AdminLTE.css',
      'admin-lte/dist/css/skins/skin-black.min.css',
      './src/django',
    ]
  },
  output: {
    path: __dirname + '/../dist/nimda',
    publicPath: '/dist/nimda/',
    filename: '[name].js'
  },
  module: {
    rules: [
      // OK
      {
        test: require.resolve('jquery'),
        use: [{
          loader: 'expose-loader',
          options: 'jQuery'
        },{
          loader: 'expose-loader',
          options: '$'
        }],
      },
      // OK
      {
        test: /\.css$/,
        use: extractCSS.extract({
          use: 'css-loader',
          fallback: 'style-loader',
        }),
      },
      // OK
      {
        test: /\.scss$/,
        use: extractCSS.extract({
          use: ['css-loader', 'sass-loader'],
          fallback: 'style-loader',
        })
      },
      // OK
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['env']
          }
        }
      },
      // OK
      {
        test: /\.(ttf|eot|woff|woff2)$/,
        loader: 'file-loader',
        options: {
          name: 'fonts/[name].[ext]',
        },
      },
      // OK
      {
        test: /\.(svg|jpg|png|gif)$/,
        loader: 'file-loader',
        options: {
          name: 'img/[name].[ext]',
        },
      },
    ]
  },
  plugins: [
    vendorBundle,
    extractCSS,
  ],
}

module.exports = config

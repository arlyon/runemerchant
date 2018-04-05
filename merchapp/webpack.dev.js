const path = require('path');
const webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');

const API_URL = "http://192.168.1.169:8000";

/**
 * The dev build config with react hot loader so that
 * changes in the css and js are automatically reflected
 * on the dom. Includes dev server for hosting the site.
 */
module.exports = {

    entry: [
        '@babel/polyfill',
        'react-hot-loader/patch',
        './src/js/dev.tsx',
        './src/scss/style.scss'
    ],

    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'dist')
    },

    module: {
        rules: [
            {
                test: /\.tsx?$/,
                exclude: /node_modules/,
                loaders: ['babel-loader', 'ts-loader'],
            },
            {
                test: /\.scss$/,
                use: [{
                    loader: "style-loader"
                }, {
                    loader: "css-loader",
                    options: {
                        sourceMap: true
                    }
                }, {
                    loader: "sass-loader",
                    options: {
                        sourceMap: true
                    }
                }]
            }
        ]
    },

    resolve: {
        extensions: ['.tsx', '.ts', '.js'],
    },

    mode: "development",
    devtool: 'inline-source-map',

    devServer: {
        historyApiFallback: true,
        contentBase: path.resolve(__dirname, 'dist'),
        overlay: true
    },

    plugins: [
        new webpack.DefinePlugin({
            API_URL: JSON.stringify(API_URL),
        }),
        new CopyWebpackPlugin([
                {from: 'src/static'}
            ],
        ),
    ]
};

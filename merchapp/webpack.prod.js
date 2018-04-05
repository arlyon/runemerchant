const path = require('path');
const webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

const API_URL = "http://192.168.1.169:8000";

/**
 * The prod build config that extracts css to an
 * external file and minifies js/css.
 */
module.exports = {

    entry: [
        '@babel/polyfill',
        './src/js/prod.tsx',
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
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].css',
                            outputPath: './'
                        }
                    },
                    {
                        loader: 'extract-loader',
                        options: {publicPath: ""} // https://github.com/peerigon/extract-loader/issues/32
                    },
                    {
                        loader: 'css-loader',
                        options: {
                            minimize: true
                        }
                    },
                    {
                        loader: 'sass-loader',
                    }
                ]
            }
        ]
    },

    resolve: {
        extensions: ['.tsx', '.ts', '.js'],
    },

    mode: "production",
    devtool: "source-map",

    plugins: [
        new webpack.DefinePlugin({
            API_URL: JSON.stringify(API_URL),
            'process.env.NODE_ENV': JSON.stringify('production')
        }),
        new CopyWebpackPlugin([
                {from: 'src/static'}
            ],
        ),
        new UglifyJSPlugin({
            sourceMap: true
        }),
        new BundleAnalyzerPlugin()
    ],

    // allows us to not have react bundled
    externals: {
        "react": "React",
        "react-dom": "ReactDOM"
    },
};

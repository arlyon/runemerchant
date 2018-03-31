const path = require('path');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

/**
 * The prod build config that extracts css to an
 * external file and minifies js/css.
 */
module.exports = {

    entry: [
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
                loader: 'ts-loader',
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

    plugins: [
        new CopyWebpackPlugin([
                {from: 'src/static'}
            ],
        )
    ],


};

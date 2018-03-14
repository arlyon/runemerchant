const path = require('path');

const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
    entry: ['./src/js/main.tsx', './src/css/style.scss'],
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'dist')
    },

    devtool: 'source-map',

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
                            outputPath: path.resolve(__dirname, 'dist')
                        }
                    },
                    {
                        loader: 'extract-loader'
                    },
                    {
                        loader: 'css-loader'
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            importer: function (url, prev) {
                                if (url.indexOf('@material') === 0) {
                                    const filePath = url.split('@material')[1];
                                    const nodeModulePath = `./node_modules/@material/${filePath}`;
                                    return {file: require('path').resolve(nodeModulePath)};
                                }
                                return {file: url};
                            }
                        }
                    }
                ]
            }
        ]
    },

    resolve: {
        extensions: ['.tsx', '.ts', '.js'],
    },

    mode: "development",

    devServer: {
        historyApiFallback: true,
        contentBase: path.resolve(__dirname, 'dist'),
        compress: true
    },

    plugins: [
        new CopyWebpackPlugin([
                {from: 'src/static'}
            ],
        ),
        //new UglifyJSPlugin(),
    ]
};

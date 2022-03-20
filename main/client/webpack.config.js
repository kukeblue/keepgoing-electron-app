const path = require('path');
const HTMLWebpackPlugin = require('html-webpack-plugin')
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const webpack = require('webpack')
const ROOT_DIRECTORY = path.join(__dirname)
const SRC_DIRECTORY = path.join(ROOT_DIRECTORY, 'src')
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    mode: 'development',
    entry: {
        index: './src/index.ts'
    },
    resolve: {
        extensions: ['.ts', '.tsx', '.js', '.json'],
        modules: [path.resolve('node_modules'), 'node_modules']
    },
    devtool: 'cheap-source-map',
    devServer: {
        proxy: {
            '/api': {
                target: 'http://103.100.210.203:3828',
                // target: 'http://127.0.0.1:3000',
                changeOrigin: true,
                pathRewrite: { '^/api': '/api' }
            }
        },
        contentBase: './dist',
        historyApiFallback: true,
        hot: true,
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx|ts|tsx)$/,
                exclude: /node_modules/,
                include: path.resolve(__dirname, "src"),
                use: [
                    {
                        loader: 'babel-loader',
                        options: {
                            presets: ['@babel/preset-env', "@babel/preset-react"],
                            plugins: ["@babel/plugin-syntax-dynamic-import"]
                        }
                    },
                    {
                        loader: 'ts-loader'
                    }
                ]
            },
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, 'style-loader', 'css-loader', 'postcss-loader']
            },
            {
                test: /\.(less)$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    {
                        loader: 'less-loader', // compiles Less to CSS
                        options: {
                            lessOptions: { // 如果使用less-loader@5，请移除 lessOptions 这一级直接配置选项。
                                modifyVars: {
                                    // 'primary-color': '#1DA57A',
                                    // 'link-color': '#1DA57A',
                                    // 'border-radius-base': '2px',
                                },
                                javascriptEnabled: true,
                            },
                        },
                    }
                ]
            },
            {
                test: /\.(jpe?g|png|gif)$/,
                use: [
                    {
                        loader: 'file-loader'
                    }
                ]
            }
        ]
    },
    plugins: [
        // new BundleAnalyzerPlugin(),
        new webpack.DefinePlugin({
            APP_ENV: JSON.stringify('dev'),
            VERSION: JSON.stringify('5fa3b9'),
        }),
        new HTMLWebpackPlugin({

            template: path.join(SRC_DIRECTORY, 'index.html'),
            favicon: "./src/favicon.ico"
        }),
        new MiniCssExtractPlugin()
    ],
    output: {
        filename: '[name].bundle.js',
        chunkFilename: '[name].bundle.js',
        path: path.resolve(__dirname, '../../dist/html')
    },
};

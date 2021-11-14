module.exports = {
    devServer: {
        proxy: {
            '/': {
                target: 'http://127.0.0.1:8000/',
                ws: false
            }
        }
    },
    configureWebpack: {
        resolve: {
            alias: {
                '@': require('path').resolve(__dirname, 'src'),
                vue$: 'vue/dist/vue.esm.js'
            },
            extensions: ['.js', '.vue', '.json', '.scss', '.html']
        }
    },
    runtimeCompiler: true,
    outputDir: './dist/',
    assetsDir: 'static'
}

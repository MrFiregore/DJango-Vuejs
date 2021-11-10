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
                '@': require('path').resolve(__dirname, 'src'), // change this to your folder path
                vue$: 'vue/dist/vue.esm.js'
            },
            extensions: ['.js', '.vue', '.json', '.scss']
        }
    },
    runtimeCompiler: true,
    outputDir: './dist/',
    assetsDir: 'static'

}

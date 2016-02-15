var gulp = require('gulp')
// Include plugins
var plugins = require('gulp-load-plugins')({
  pattern: ['gulp-*', 'gulp.*', 'main-bower-files', 'run-sequence'],
  replaceString: /\bgulp[\-.]/
})
var source = require('vinyl-source-stream')
var buffer = require('vinyl-buffer')
var browserSync = require('browser-sync').create()
var browserify = require('browserify')
var dest = 'frontdev/build/'
var src = 'frontdev/src/'
var bowerBase = src + 'bower/'
var collect = 'static/'

// concatenates js files
gulp.task('js', function () {
  var jsFiles = src + 'javascript/main.js'
  return browserify(jsFiles)
    .bundle()
    .on('error', console.log)
    .pipe(source('main.js'))
    .pipe(buffer())
    .pipe(gulp.dest(dest + 'javascript'))
    .pipe(gulp.dest(collect + 'javascript'))

})

// compiles sass files and autoprefixes the outgoing css
gulp.task('sass', function () {
  var sassFiles = [src + 'sass/**/*.scss']
  return gulp.src(sassFiles)
    .pipe(plugins.sass().on('error', plugins.sass.logError))
    .pipe(plugins.autoprefixer('last 2 version'))
    .pipe(gulp.dest(dest + 'css'))
})

// concatenates css
gulp.task('css', function () {
  var cssFiles = [dest + 'css/*.css']

  return gulp.src(plugins.mainBowerFiles().concat(cssFiles))
    .pipe(plugins.filter('*.css'))
    .pipe(plugins.order([
      'normalize.css',
      '*'
    ]))

    .pipe(plugins.concat('main.css'))
    .pipe(gulp.dest(dest + 'css'))
    .pipe(plugins.cssnano())
    .pipe(gulp.dest(collect + 'css'))

})

// Includes the partials in the html files and copies them to the build folder
gulp.task('html', function () {
  var htmlFiles = [src + 'html/*.html']

  gulp.src(htmlFiles)
    .pipe(plugins.include())
    .on('error', console.log)
    .pipe(gulp.dest(dest))
})

// Copies img to build/img
gulp.task('img', function () {
  var imgFiles = [src + 'img/*']

  gulp.src(imgFiles)
    .pipe(gulp.dest(dest + 'img'))
    .pipe(gulp.dest(collect + 'img'))
})

gulp.task('browserSyncStream', function () {
  var cssFiles = [dest + 'css/*.css']

  gulp.src(cssFiles)
    .pipe(browserSync.stream())
    .pipe(gulp.dest(collect + 'fonts'))
})

gulp.task('compsass', function (callback) {
  plugins.runSequence('sass',
    'css',
    callback)

})

gulp.task('icons', function () {
  return gulp.src(bowerBase + 'font-awesome/fonts/**.*')
    .pipe(gulp.dest(dest + 'fonts'))
    .pipe(gulp.dest(collect + 'fonts'))
})

// Watches everything and starts browser sync
gulp.task('watch', function () {
  browserSync.init({
    proxy: '127.0.0.1:8080'
  })
  gulp.watch(src + 'sass/**/*.scss', ['compsass'])
  gulp.watch(dest + 'css/**/*.css', ['browserSyncStream'])
  gulp.watch(src + 'javascript/**/*.js', ['js']).on('change', browserSync.reload)
  gulp.watch('./**/*.html').on('change', browserSync.reload)
  gulp.watch(src + 'html/**/*.html', ['html'])
  gulp.watch(src + 'img/*', ['img']).on('change', browserSync.reload)
})
gulp.task('default', ['html', 'compsass', 'img', 'js', 'icons'])

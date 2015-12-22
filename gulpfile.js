var gulp = require('gulp');
// Include plugins
var plugins = require("gulp-load-plugins")({
	pattern: ['gulp-*', 'gulp.*', 'main-bower-files', 'run-sequence'],
	replaceString: /\bgulp[\-.]/
});
var browserSync = require('browser-sync').create();
var dest = 'frontdev/build/';
var src = 'frontdev/src/';
var bowerBase = src + 'bower/';

//concatenates js files
gulp.task('js', function() {
	var jsFiles = [src + 'javascript/*.js', ];
	gulp.src(plugins.mainBowerFiles().concat(jsFiles))
		.pipe(plugins.filter('*.js'))
		.pipe(plugins.order([
			'jquery.js',
			'*'
		]))
		.pipe(plugins.concat('main.js'))
		.pipe(gulp.dest(dest + 'javascript'));
});

//compiles sass files and autoprefixes the outgoing css
gulp.task('sass', function() {
	var sassFiles = [src + 'sass/**/*.scss'];
	return gulp.src(sassFiles)
		.pipe(plugins.sass().on('error', plugins.sass.logError))
		.pipe(plugins.autoprefixer('last 2 version', 'safari 5', 'ie 8', 'ie 9'))
		.pipe(gulp.dest(dest + 'css'));
});

//concatenates css
gulp.task('css',  function(){

	var cssFiles = [dest + 'css/*.css'];

	return gulp.src(plugins.mainBowerFiles().concat(cssFiles))
		.pipe(plugins.filter('*.css'))
		.pipe(plugins.order([
			'normalize.css',
			'*'
		]))

	.pipe(plugins.concat('main.css'))
	.pipe(gulp.dest(dest + 'css'));

});

//Includes the partials in the html files and copies them to the build folder
gulp.task('html', function() {

	var htmlFiles = [src + 'html/*.html'];

	gulp.src(htmlFiles)
		.pipe(plugins.include())
      		.on('error', console.log)
		.pipe(gulp.dest(dest));
});

//Copies img to build/img
gulp.task('img', function() {

	var imgFiles = [src + 'img/*'];

	gulp.src(imgFiles)
		.pipe(gulp.dest(dest + 'img'));
});

gulp.task('browserSyncStream', function(){
	var cssFiles = [dest + 'css/*.css'];

	gulp.src(cssFiles)
		.pipe(browserSync.stream());
})

gulp.task('compsass',function(callback) {
	plugins.runSequence('sass',
	                    'css',
	                    callback);

});

//Watches everything and starts browser sync
gulp.task('watch', function() {
	browserSync.init({
		server: {
			baseDir: dest,
		}
	});
	gulp.watch(src + 'sass/**/*.scss', ['compsass']);
	gulp.watch(dest + 'css/**/*.css', ['browserSyncStream']);
	gulp.watch(src + 'javascript/**/*.js', ['js']).on('change', browserSync.reload);
	gulp.watch(src + "html/**/*.html", ['html']).on('change', browserSync.reload);
	gulp.watch(src + "img/*", ['img']).on('change', browserSync.reload);
});

gulp.task('default', ['html', 'compsass', 'img', 'js']);

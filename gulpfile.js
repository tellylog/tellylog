var gulp = require('gulp');
// Include plugins
var plugins = require("gulp-load-plugins")({
	pattern: ['gulp-*', 'gulp.*', 'main-bower-files'],
	replaceString: /\bgulp[\-.]/
});
var browserSync = require('browser-sync').create();
var dest = 'frontdev/build/';
var src = 'frontdev/src/';
var bowerBase = src + 'bower/';

//concatenates js files
gulp.task('js', function(done) {
	var jsFiles = [src + 'javascript/*.js', ];
	gulp.src(plugins.mainBowerFiles().concat(jsFiles))
		.pipe(plugins.filter('*.js'))
		.pipe(plugins.order([
			'jquery.js',
			'*'
		]))
		.pipe(plugins.concat('main.js'))
		.pipe(gulp.dest(dest + 'javascript'));
	done();
});

//compiles sass files and autoprefixes the outgoing css
gulp.task('sass', function(done) {
	var sassFiles = [src + 'sass/**/*.scss'];
	gulp.src(sassFiles)
		.pipe(plugins.sass().on('error', plugins.sass.logError))
		.pipe(plugins.autoprefixer('last 2 version', 'safari 5', 'ie 8', 'ie 9'))
		.pipe(gulp.dest(dest + 'css'));
	done();
});

//concatenates css
gulp.task('css',  function(done){

	var cssFiles = [dest + 'css/*.css'];

	gulp.src(plugins.mainBowerFiles().concat(cssFiles))
		.pipe(plugins.filter('*.css'))
		.pipe(plugins.order([
			'normalize.css',
			'*'
		]))

	.pipe(plugins.concat('main.css'))
	.pipe(gulp.dest(dest + 'css'));
	done();

});

//Includes the partials in the html files and copies them to the build folder
gulp.task('html', function(done) {

	var htmlFiles = [src + 'html/*.html'];

	gulp.src(htmlFiles)
		.pipe(plugins.include())
      		.on('error', console.log)
		.pipe(gulp.dest(dest));

	done();
});

//Copies img to build/img
gulp.task('img', function(done) {

	var imgFiles = [src + 'img/*'];

	gulp.src(imgFiles)
		.pipe(gulp.dest(dest + 'img'));
	done();
});

gulp.task('browserSyncStream', function(done){
	var cssFiles = [dest + 'css/*.css'];

	gulp.src(cssFiles)
		.pipe(browserSync.stream());
	done();
})

//Watches everything and starts browser sync
gulp.task('watch', function() {
	browserSync.init({
		server: {
			baseDir: dest,
		}
	});
	gulp.watch(src + 'sass/**/*.scss', gulp.series('sass', 'css', 'browserSyncStream'));
	gulp.watch(dest + 'css/**/*.css', gulp.parallel('browserSyncStream'));
	gulp.watch(src + 'javascript/**/*.js', gulp.parallel('js')).on('change', browserSync.reload);
	gulp.watch(src + "html/**/*.html", gulp.parallel('html')).on('change', browserSync.reload);
	gulp.watch(src + "img/*", gulp.parallel('img')).on('change', browserSync.reload);
});

gulp.task('default', gulp.series('html', 'sass', 'css', 'img', 'js'));
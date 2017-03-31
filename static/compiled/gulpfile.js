var gulp = require('gulp'),
    sass = require('gulp-sass'),
    jshint = require('gulp-jshint'),
    concat = require('gulp-concat'),
    imagemin = require('gulp-imagemin'),
    plumber = require('gulp-plumber'),
    notify = require('gulp-notify'),
    uglify = require('gulp-uglify'),
    livereload = require('gulp-livereload'),
    autoprefixer = require('gulp-autoprefixer'),
    sourcemaps = require('gulp-sourcemaps'),
    bower = require('gulp-bower');

gulp.task('default', function(){
    console.log('default gulp task...');
});

var config = {
    sassPath: './sass',
    bowerDir: './bower_components'
};


gulp.task('sass', function () {
    return gulp.src(config.sassPath + '/style.scss')
        .pipe(sourcemaps.init())
        .pipe(sass({
            outputStyle: 'compressed',
            precison: 3,
            errLogToConsole: true
        })
        .on("error", notify.onError(function (error) {
          return "Error: " + error.message;
        })))
        .pipe(autoprefixer({
          browsers: [
            'last 4 versions',
            "Android 2.3",
            "Android >= 4",
            "Chrome >= 20",
            "Firefox >= 24",
            "Explorer >= 8",
            "iOS >= 6",
            "Opera >= 12",
            "Safari >= 6"
          ]
        }))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('./'))
        .pipe(livereload());
});

gulp.task('js', function () {

  gulp.src('./js/*.js')

    .pipe(plumber(plumberErrorHandler))
    .pipe(concat('theme.js'))
    .pipe(uglify())
    .pipe(gulp.dest('./'))
    .pipe(livereload());

});

gulp.task('watch', function() {
  livereload.listen();
  gulp.watch('./sass/**/*.scss', ['sass']);
  gulp.watch('./js/*.js', ['js']);

});

var plumberErrorHandler = { errorHandler: notify.onError({

    title: 'Gulp',
    message: 'Error: <%= error.message %>'

  })

};

gulp.task('default', ['sass', 'js', 'watch']);

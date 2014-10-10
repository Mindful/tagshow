    //var alphabet = new RegExp(/^[A-z]+$/)

    function initSlideShow(options, slideshowOptions){
      stretchToFit = typeof options['stretch_to_fit'] !== 'undefined' ? options['stretch_to_fit'] : false;
      fullscreenKey = typeof options['fullscreen_key'] !== 'undefined' ? options['fullscreen_key'] : 'f';

      $('img').each(function(){
        var img = $(this);
        img.data('maxheight', img.height() );
        img.data('maxwidth', img.width() );
      });
      $("#slideshow").cycle(slideshowOptions);
      sizeImages();

      $(document).bind("fullscreenchange", function(){
        setTimeout(function(){sizeImages();}, 250); //Have to wait, this event fires with the old viewport values
      });

      $(document).keydown(function(event) {
          var char = String.fromCharCode(event.which);
          console.log(char)
          if(char.toUpperCase() == fullscreenKey.toUpperCase()){
            $("#slideshow").toggleFullScreen();
          }
      });
    }

    function sizeImages(stretch){
      console.log("resize images");
      var viewportWidth = $(window).width();
      var viewportHeight = $(window).height();
      $('img').each(function(){
        var img = $(this);
        var height = img.data('maxheight');
        var width = img.data('maxwidth');
        var aspectRatio = width/height;
        img.height(Math.min(height, viewportHeight));
        img.width(aspectRatio * img.height());

        if(img.width > viewportWidth){
          img.width(viewportWidth);
          img.height(img.width() / aspectRatio);
        }

        img.css("margin-left", (viewportWidth - img.width())/2);
        img.css("margin-top:", (viewportHeight - img.height())/2);
      });
    }

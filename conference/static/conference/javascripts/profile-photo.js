(function($, Cookies){
  $(function(){
    var $changePhotoCollapse = $('#change-photo-collapse');
    var $deletePhotoCollapse = $('#delete-photo-collapse');
    var $profilePhoto = $('.js-profile-photo');

    // Bind the various actions to the photo field's buttons
    var bindPhotoButtons = function bindPhotoButtons() {
      // Make sure that opening the "change" collapsable closes the "delete"
      // one and vice-versa.
      $changePhotoCollapse.on('show.bs.collapse', function(){
        $deletePhotoCollapse.collapse('hide');
      });
      $deletePhotoCollapse.on('show.bs.collapse', function(){
        $changePhotoCollapse.collapse('hide');
      });

      // When people click the confirm delete button, POST to the delete photo
      // endpoint
      $('#delete-photo').click(function(e){
        e.preventDefault();
        $.ajax(
          '/profile/delete-photo',
          {
            'method': 'post',
            'success': updatePhoto,
            'dataType': 'html'
          }
        );
      });
    };

    // Update the photo field with new HTML from an AJAX call.
    var updatePhoto = function updatePhoto(data) {
      $profilePhoto.html(data);
      bindPhotoButtons();
    };

    // Configure jQuery to send Django's CSRF token with every ajax request.
    $.ajaxSetup({headers: {'X-CSRFToken': Cookies.get('csrftoken')}});

    // Bind the initial buttons
    bindPhotoButtons();
  });
})(window.jQuery, window.Cookies);
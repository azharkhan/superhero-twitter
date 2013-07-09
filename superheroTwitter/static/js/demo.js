$(document).ready(function() {
  $('#tweet_form').submit(function() {
    $.ajax({
      data: $(this).serialize(),
      type: $(this).attr('method'),
      url: $(this).attr('action'),
      success: function(response) {
        $('#tweets').html(response);
      }
    });
    return false;
  });
});
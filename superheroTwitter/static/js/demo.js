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

  $('#search').keyup(function() {
    if($('#search').val().length == 0){
      $('.dropdown-menu').hide();
    }

    else {

    $.ajax({
      type: "POST",
      url: "/search",
      data: {
        'search_text': $('#search').val(),
        'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
      },
      success: searchSuccess
    });
  }
  });

  function searchSuccess(data) {
    $('#search-results').html(data);
    $('.dropdown-menu').show();
  }

});
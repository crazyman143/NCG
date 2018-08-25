
// dynamic content for the confirm order page.
// delete items and remove the element from 
// the page.



var $item_count = $('#item_count');

// this is the class of the submit button
$(".del_item_js_tag").click(function(event) {

  // its parent is the form
  var $form = $(this).parent();
  //console.log( $form );

  //prevent default action (regular form submit)
  event.preventDefault();

  // jquery ajax function
  $.ajax({
    type:'POST',              // type of submission
    url: 'confirm_order',     // where to send the form
    data: $form.serialize(),  // what to send (the form, serialized)

    // if error from server, run:
    error: function() {
      alert('error');
      $form.parent().html('error');   // submit button is replaced with 'error'
    },

    // if success from server, run:
    success: function(data) {

      // if 'code' key in json response contains 'true':
      if ( data.code == 'true' ) {
        // fadeout duration 300, callback function removes element
        $form.parent().parent().fadeOut( 300, function(){$(this).remove();}    );

      // if 'code' key in json response contains 'false':
      } else if ( data.code == 'false' ) {
        $form.parent().html('error');
      }
    },
  });
})
	
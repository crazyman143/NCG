
// dynamic content for the new order page.
// send cart order items and
// get back item count

// https://stackoverflow.com/questions/20522887/referenceerror-event-is-not-defined-error-in-firefox
// https://teamtreehouse.com/community/when-to-use-this-in-jquery
// https://www.sanwebe.com/2016/07/ajax-form-submit-examples-using-jquery

var $item_count = $('#item_count');

// this is the class of the submit button
$(".add_item_js_tag").click(function(event) {

  // its parent's parent's parent is the form
  var $form 		= $(this).parent().parent().parent();
  var $success_msg	= $form.children().find("div[id=success_msg]");
  console.log($success_msg);
  //console.log( $form );


  //prevent default action (regular form submit)
  event.preventDefault();

  // jquery ajax function
  $.ajax({
    type:'POST',				// type of submission
    url: 'new_order',			// where to send the form
    data: $form.serialize(),	// what to send (the form, serialized)

    // if error from server, run:
    error: function() {
      $success_msg.html('Server error occured');
      $success_msg.fadeIn( 300 ).delay( 1000 ).fadeOut( 400 );
    },

    // if success from server, run:
    success: function(data) {

      // if 'form_error' key in response:
      if (data.form_error) {
        $success_msg.html(data.form_error);
        $success_msg.fadeIn( 300 ).delay( 1000 ).fadeOut( 400 );
   		};


      // if 'validation_error' key in response:
      if (data.validation_error) {

      	// isolate the validation json dict
      	var errs = data.validation_error;


      	// for field obj (x) in the errs dict
		for (var x in errs) {

			// find div in form containing an id of the problem field
			$field = $form.find("div[id*=div_id_" + x + "]");

			// within that div's children, find a select or input field. append the invalid class
			$field.children().find("select, input[id*=id_" + x + "]").addClass("is-invalid");

			// get the error message for this field from the json
			errmsg = errs[x][0].message;

			// find amogst the children <p> elements w/ class 'invalid-feedback'
			// count number of elements found. if == 0, then...
			if ($field.children().find("p[class*=invalid-feedback]").length == 0 ) {

				// append amongst the field's div's children a <p> element containing the error msg from the json
				$field.children().append("<p class=\"invalid-feedback\"><strong>" + errmsg + "</strong></p>");
				}

			}

   		};


      // if 'item_count' key in response:
      if (data.item_count) {
        $success_msg.fadeIn( 300 ).delay( 1000 ).fadeOut( 400 );
        $item_count.html(data.item_count);

        // assuming a good form was sent, remove
        // any possible validation errors
        $(document).find("[class*=invalid]").removeClass("is-invalid")

      	};
  	  },
	});
  })
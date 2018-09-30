function selectOnlyOneCheckbox() {
	// the selector will match all input controls of type :checkbox
	// and attach a click event handler 
	$("input:checkbox").on('click', function() {
	  // in the handler, 'this' refers to the box clicked on
	  var $box = $(this);
	  if ($box.is(":checked")) {
	    // the name of the box is retrieved using the .attr() method
	    // as it is assumed and expected to be immutable
	    var group = "input:checkbox[name='" + $box.attr("name") + "']";
	    // the checked state of the group/box on the other hand will change
	    // and the current value is retrieved using .prop() method
	    $(group).prop("checked", false);
	    $box.prop("checked", true);
	  } else {
	    $box.prop("checked", false);
	  }
	});
}

setTimeout(function() {
	selectOnlyOneCheckbox();

	$('.form-row.field-percentage').hide();
	$('.form-row.field-percentage_with_cap.field-cap_percentage').hide();
	$('.form-row.field-absolute_with_min.field-min_absolute').hide();

	$("input:checkbox").on('click', function() {
		var $box = $(this);
	    if ($box.is(":checked")) {
	    	if ($box.attr("value") == "PERCENTAGE") {
	    		$('.form-row.field-percentage').show();
	    		$('.form-row.field-percentage_with_cap.field-cap_percentage').hide();
	    		$('.form-row.field-absolute_with_min.field-min_absolute').hide();
	    	} else if ($box.attr("value") == "PERCENTAGEWITHCAP") {
	    		$('.form-row.field-percentage').hide();
	    		$('.form-row.field-percentage_with_cap.field-cap_percentage').show();
	    		$('.form-row.field-absolute_with_min.field-min_absolute').hide();
	    	} else if ($box.attr("value") == "ABSOLUTEWITHMIN") {
	    		$('.form-row.field-percentage').hide();
	    		$('.form-row.field-percentage_with_cap.field-cap_percentage').hide();
	    		$('.form-row.field-absolute_with_min.field-min_absolute').show();
	    	}
	    }
	});
}, 100);
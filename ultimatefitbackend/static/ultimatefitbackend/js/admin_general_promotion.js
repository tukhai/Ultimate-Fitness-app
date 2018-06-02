console.log("hi1");

// Get all dates between 2 dates, using moment.js
function getDates(startDate, stopDate) {
    var dateArray = [];
    var currentDate = moment(startDate);
    var stopDate = moment(stopDate);
    while (currentDate <= stopDate) {
        dateArray.push(moment(currentDate).format('YYYY-MM-DD'))
        currentDate = moment(currentDate).add(1, 'days');
    }
    return dateArray;
}

function disablingDates(calendarID) {
	var shownMonthYear = $(calendarID + " caption").text();

    for (var i = 0; i < datesToDisableArr.length; i++) {
    	var selectedDay = moment(datesToDisableArr[i]).format('D');

    	if (moment(datesToDisableArr[i]).format('MMMM YYYY') == shownMonthYear) { // and if the date not between the selected dates range
    		$(calendarID + " td a:contains('" + selectedDay + "')").first().css("background-color", "lightgrey");
    		$(calendarID + " td a:contains('" + selectedDay + "')").first().css("pointer-events", "none");
    	}
    }
}

var datesToDisableArr = [];

// Have to put setTimeout MAYBE because the db needs time to display all data 
// (later if something wrong, set time delay to 100ms)

setTimeout(function() {
	$("td.field-percentage").each(function() {
	    var appendedString = $(this).text() + ' %';
	    $(this).html(appendedString);
	});

	//DO NOT disable date range of this current promotion (if not create new promotion, but edit the existing one)
	var currentPromotionStartDate = "";
	var currentPromotionEndDate = "";
    if ($("div#content h1").text() == "Change general promotion") {
    	currentPromotionStartDate = $("input#id_startDate").attr("value");
    	currentPromotionEndDate = $("input#id_endDate").attr("value");
    }

	$.get("/general-promotion-list", function(data, status) {
	    for (var i = 0; i < data.length; i++) {
	    	if (data[i].fields.startDate != currentPromotionStartDate && data[i].fields.endDate != currentPromotionEndDate) {
		    	var rangeDateArr = getDates(data[i].fields.startDate, data[i].fields.endDate);
		    	$.merge(datesToDisableArr, rangeDateArr);
		    }
	    }

	    // disablingDates("#calendarbox0");
	    $("#calendarlink0").click(function() {
	    	disablingDates("#calendarbox0");
	    });
	    $("#calendarbox0 .calendarnav-previous").click(function() {
		    disablingDates("#calendarbox0");
		});
		$("#calendarbox0 .calendarnav-next").click(function() {
		    disablingDates("#calendarbox0");
		});

		// disablingDates("#calendarbox1");
		$("#calendarlink1").click(function() {
	    	disablingDates("#calendarbox1");
	    });
	    $("#calendarbox1 .calendarnav-previous").click(function() {
		    disablingDates("#calendarbox1");
		});
		$("#calendarbox1 .calendarnav-next").click(function() {
		    disablingDates("#calendarbox1");
		});

		// DISABLE Yesterday | Today | Tomorrow buttons also if those are in period
		// Through modifying datesToDisableArr above, Yesterday | Today | Tomorrow buttons are not disabled if it's currentPromotion
		
		// Yesterday
		if (datesToDisableArr.indexOf(moment(new Date()).add(-1,'days').format('YYYY-MM-DD')) > -1) {
			$(".calendar-shortcuts a:contains('Yesterday')").css("color", "lightgrey");
			$(".calendar-shortcuts a:contains('Yesterday')").css("pointer-events", "none");
		};

		// Today
		if (datesToDisableArr.indexOf(moment(new Date()).format('YYYY-MM-DD')) > -1) {
			$(".calendar-shortcuts a:contains('Today')").css("color", "lightgrey");
			$(".calendar-shortcuts a:contains('Today')").css("pointer-events", "none");
		};

		// Tomorrow
		if (datesToDisableArr.indexOf(moment(new Date()).add(1,'days').format('YYYY-MM-DD')) > -1) {
			$(".calendar-shortcuts a:contains('Tomorrow')").css("color", "lightgrey");
			$(".calendar-shortcuts a:contains('Tomorrow')").css("pointer-events", "none");
		};
	});
}, 100);
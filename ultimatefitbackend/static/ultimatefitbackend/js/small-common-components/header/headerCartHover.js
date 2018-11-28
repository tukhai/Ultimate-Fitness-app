/*TRACK PREVIOUS URL TO DISPLAY PROPERLY MESSAGE*/
//console.log("{{previous_url}}");


$('#cartDropdown-hover').hover(function() {
    $(document).find('.cart_list').stop(true, true).delay(50).fadeIn(200);
}, function() {
    $(document).find('.cart_list').stop(true, true).delay(50).fadeOut(200);
});

$('.cart_list').hover(function() {
    $(this).stop(true, true).delay(50).fadeIn(200);
}, function() {
    $(this).stop(true, true).delay(50).fadeOut(200);
});


// Only pull data and render when hover to the button (try this first)
$('#cartDropdown-hover').hover(function() {
    console.log("Pulling data for dropdown cart when hover");
    $.get("/list", function(data, status){
        //console.log("Data: " + data)
        //console.log(typeof(data));
        console.log("Status: " + status);
        $(".cart_list ul").html(data);
    }).fail(function(){
	    popUpInternetConnectionError();
	});
    getTotalToPayFromDB();
});



function getTotalToPayFromDB() {
	$.get("/total", function(data, status){
        console.log("Data: " + data.total + "\nStatus: " + status);
        console.log(typeof(data.total));
        totalToPay = data.total;
        console.log("TOTAL TO PAY FROM DB: " + totalToPay);
    	$("text#total-to-pay").html(totalToPay);
    });
};

function popUpInternetConnectionError() {
	console.log("NO INTERNET");
	$('.internet-connection-error').fadeIn(200);
    $('.internet-connection-error').delay(1500).fadeOut(200);
};

//$(".add-to-cart-list").click(function(){
$(document).on("click", ".add-to-cart-list", function(){
	var idOfFood = $(this).data('id-food'); 
    console.log("Adding food of id: " + idOfFood);

    var priceOfFood = $(this).data('price-food');
    console.log("Price of this food: " + priceOfFood);

    $.post(
    	"/add/" + idOfFood,
        { 
          csrfmiddlewaretoken: csrfToken
        },
        function(data,status){
            console.log("Status: " + status);

            if (status == "success") {
	            //Consider moving this out of post function, so the number change faster, and do the check if status success or false, if false show error box/page 404
		        quantityOfFoodArray[idOfFood] += 1;
		        
	            console.log("Current quantity of food id " + idOfFood + " in database: " + quantityOfFoodArray[idOfFood]);

	            $("span#quantity-for-food-id-" + idOfFood).html(quantityOfFoodArray[idOfFood]);
	            $("span#total-price-for-food-id-" + idOfFood).html(priceOfFood*quantityOfFoodArray[idOfFood]);

			    
				getTotalToPayFromDB();
			};
        }
    ).fail(function(){
	    popUpInternetConnectionError();
	});
});

//$(".remove-from-cart-list").click(function(){
$(document).on("click", ".remove-from-cart-list", function(){
	var idOfFoodToBeRemoved = $(this).data('id-food'); 
    console.log("Removing food of id: " + idOfFoodToBeRemoved);

    var priceOfFoodToBeRemoved = $(this).data('price-food');
    console.log("Price of the food to be removed: " + priceOfFoodToBeRemoved);

    $.post(
    	"/remove/" + idOfFoodToBeRemoved,
        { 
          csrfmiddlewaretoken: csrfToken
        },
        function(data,status){
            console.log("Status: " + status);

            if (status == "success") {
	            //Consider moving this out of post function, so the number change faster, and do the check if status success or false, if false show error box/page 404
		        quantityOfFoodArray[idOfFoodToBeRemoved] -= 1;
		        
	            console.log("Current quantity of food id " + idOfFoodToBeRemoved + " in database: " + quantityOfFoodArray[idOfFoodToBeRemoved]);

	            // when quantity = 0, just remove the item from the list
	            if (quantityOfFoodArray[idOfFoodToBeRemoved] > 0) {
	            	$("span#quantity-for-food-id-" + idOfFoodToBeRemoved).html(quantityOfFoodArray[idOfFoodToBeRemoved]);
	            	$("span#total-price-for-food-id-" + idOfFoodToBeRemoved).html(priceOfFoodToBeRemoved*quantityOfFoodArray[idOfFoodToBeRemoved]);
	        	} else {
	        		$("li#list-item-" + idOfFoodToBeRemoved).remove();
	        	};
        	
			    getTotalToPayFromDB();
			};
        }
    ).fail(function(){
	    popUpInternetConnectionError();
	});
});

//$(".close-list-cart").click(function(){
$(document).on("click", ".close-list-cart", function(){
	var idOfDeleteFood = $(this).data('id-food');
	console.log("deleting all items type of food id: " + idOfDeleteFood);

	var priceOfDeleteFood = $(this).data('price-food');
	console.log("price of 1 item of this type of food: " + priceOfDeleteFood);

	$.post(
    	"/removeall/" + idOfDeleteFood,
        { 
          csrfmiddlewaretoken: csrfToken
        },
        function(data,status){
            console.log("Status: " + status);
            console.log("Successfully delete all food type of id: " + idOfDeleteFood);

            if (status == "success") {
			    getTotalToPayFromDB();
			    //$(this).parent('li').fadeOut(300);
			    quantityOfFoodArray[idOfDeleteFood] = 0;
			    $("li#list-item-" + idOfDeleteFood).fadeOut(150);
			    //$("li#list-item-" + idOfDeleteFood).css("display", "none");
			};
        }
    ).fail(function(){
	    popUpInternetConnectionError();				    
	});
});
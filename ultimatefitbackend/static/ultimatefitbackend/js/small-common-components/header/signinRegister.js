/***Modal box for sign in/register***/
$(document).on("click", ".button-for-authenticate", function(){
    var buttonType = $(this).data('authentication-button');
    console.log("button: " + buttonType);
    if (buttonType == "sign-in-button") {
    	$("#sign-in-page").show();
    	$("#register-page").hide();
    	$("span#login-button-on-modal").css({"color": "red", "text-decoration": "underline"});
    	$("span#register-button-on-modal").css({"color": "#939393", "text-decoration": "none"});
    } else {
    	$("#sign-in-page").hide();
    	$("#register-page").show();
    	$("span#login-button-on-modal").css({"color": "#939393", "text-decoration": "none"});
    	$("span#register-button-on-modal").css({"color": "red", "text-decoration": "underline"});
    }
});

$(document).on('show.bs.modal', '#signin_modal', function(e) {
    console.log("open sign in modal box");		     
});
$(document).on('hidden.bs.modal', '#signin_modal', function (e) {
    console.log("close sign in modal box");
});
/***Ajax login***/
$(document).on("click", "input#btn-login", function(){
	console.log("posting to login...");
	var inputUsername = $("input#login-username").val();
	var inputPassword = $("input#login-password").val();

	console.log("Logging in with username: '" + inputUsername +"'");

	$.post(
    	"/accounts/login/",
        { 
          csrfmiddlewaretoken: csrfToken,
          username: inputUsername,
          password: inputPassword
        },
        function(data,status){
            console.log("Status: " + status);
            if (status == "success") {
	            //refresh the page after login success, so the login would redirect to current page
	            $.get("/total", function(data, status){
			        //console.log("Data: " + data.check_authentication + "\nStatus: " + status);
			        //console.log(typeof(data.check_authentication));
			        //isAuthenticated = data.check_authentication;
			        //console.log("Have user loged in? - " + isAuthenticated);
			        if (data.check_authentication) {
			        	location.reload();
			        } else {
			        	console.log("Wrong username or password");
			        	$("#login-error-message").append('<label style="color: red;">Username and password do not match!</label>');
			        }
			    });
	        };
        }
    ).fail(function(){
	    popUpInternetConnectionError();				    
	});
});
/*Handle log in error message*/
$(document).on("click", "input.form-control", function(){
	$("#login-error-message label").remove();
});

/*****************************************************************/


/**Front-end registration validation**/
function ValidateEmail(mail) {  
	var re = /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}/igm;
	if (re.test(mail)) {
	    return true;
	} else {
	    return false;
	}  
};

function registrationValidation() {
    console.log("validating registration form...");
	
	var inputRegistrationEmail = $("input#id_email").val();
	var inputRegistrationPassword = $("input#id_password1").val();
	var inputRegistrationPasswordConfirm = $("input#id_password2").val();

	if (!ValidateEmail(inputRegistrationEmail)) {
		$("#registration-error-message").append('<label style="color: red;">Invalid email! Please try to re-enter your email.</label>');
		return false;
	}

	if (inputRegistrationPassword.length < 8) {
		$("#registration-error-message").append('<label style="color: red;">Your password must have at least 8 characters.</label>');
		return false;
	}

	if (inputRegistrationPassword != inputRegistrationPasswordConfirm) {
		$("#registration-error-message").append('<label style="color: red;">Password confirmation does not match!</label>');
		return false;
	}

	return true;
};


/***Ajax registration***/
$(document).on("click", "input#btn-registration", function(){				

	$("#registration-error-message label").remove();
	console.log("posting to registion...");
	//var inputRegistrationUsername = $("input#id_username").val();
	var inputRegistrationEmail = $("input#id_email").val();
	var inputRegistrationPassword = $("input#id_password1").val();
	var inputRegistrationPasswordConfirm = $("input#id_password2").val();

	if (registrationValidation()) {

		//console.log("Registering in with username: '" + inputRegistrationUsername +"'");
		console.log("Registering in with email: '" + inputRegistrationEmail +"'");


		/*Check registration validation*/
		$.post(
	    	"/registration_validation/",
	        { 
	          csrfmiddlewaretoken: csrfToken,
	          name: inputRegistrationEmail
	        },
	        function(data,status){
	            console.log("Status: " + status);
	            if (status == "success") {
				    console.log("Data: " + data.registration_validator);
				    if (data.registration_validator) {
				    	/*IF THE EMAIL IS NEW, THEN CLOSE MODAL BOX AND PROCESS TO POST REGISTRATION FORM TO BACKEND*/
						// Clear input text in registration form
						$("p.required input").val("");
						// Close modal box
						$('#signin_modal button.close').click();
						//$('.modal-backdrop').remove(); // Close the backdrop
						$('#submit-registration-message').show();

			        	console.log("Valid registration name, sending activation email..");

			        	$.post(
					    	"/accounts/register/",
					        { 
					          csrfmiddlewaretoken: csrfToken,
					          //username: inputRegistrationUsername,
					          username: inputRegistrationEmail,
					          email: inputRegistrationEmail,
					          password1: inputRegistrationPassword,
					          password2: inputRegistrationPasswordConfirm
					        },
					        function(data,status){
					            console.log("Status: " + status);
					            if (status == "success") {
						            //data callback here is the whole activation email sent to you shortly html page
						            console.log("Successfully sent activation email");
						            $('.modal-backdrop').remove(); // Close the backdrop
						            $('#submit-registration-message').hide();
						            $("#activation-email-message").show();
						        };
					        }
				        );
			        } else {
			        	console.log("That username has already been taken");
			        	$("#registration-error-message").append('<label style="color: red;">That email has already been used, please use another email!</label>');
			        }
		        };
	        }
        ).fail(function(){
		    popUpInternetConnectionError();				    
		});
	}
	/*$.post(
    	"/accounts/register/",
        { 
          csrfmiddlewaretoken: "{{ csrf_token }}",
          username: inputRegistrationUsername,
          email: inputRegistrationEmail,
          password1: inputRegistrationPassword,
          password2: inputRegistrationPasswordConfirm
        },
        function(data,status){
            console.log("Status: " + status);
            if (status == "success") {
	            //refresh the page after login success, so the login would redirect to current page
	            console.log(data);
	        };
        }
    ).fail(function(){
	    popUpInternetConnectionError();				    
	});*/
});
/*Handle registration error message*/
$(document).on("click", "p.required input", function(){
	$("#registration-error-message label").remove();
});

/*Close activation email message*/
$(document).on("click", "#confirm-activation-email-button", function(){
	$("#activation-email-message").hide();
});
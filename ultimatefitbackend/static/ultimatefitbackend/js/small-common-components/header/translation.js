// This part is the javascript front-end for language change, 
// but the dictionary is saved in a python file
// var dictTranslationString = "{{dict_translation}}";
dictTranslationString = dictTranslationString.replace(/&quot;/g, '"');
dictTranslationString = dictTranslationString.replace(/&#39;/g, "'");
dictTranslationString = dictTranslationString.replace(/'}/g, '"}');
dictTranslationString = dictTranslationString.replace(/':/g, '":');
dictTranslationString = dictTranslationString.replace(/',/g, '",');
dictTranslationString = dictTranslationString.replace(/u'/g, '"');

var dict = JSON.parse(dictTranslationString);

/*Check if any wrong words, which not appear on dict, it's for developer use*/
$(".trn").each(function() {
	if (!dict[$(this).html()]) {
		throw new Error(`Key ${$(this).html()} doesnt exist in dictionary`);
	}
});
/****************************************************************************/

var translator = $('body').translate({lang: "vn", t: dict});

$(document).on("click", "li.english-language", function(){
	$("span#flag-icon-language").html('<span class="flag-icon-size"><img src="http://www.postkrieg.info/_assets/img/en_icon.png"/></span>&nbsp;English');

	translator.lang("en");
	localStorage.setItem('LANGUAGE', 'en');

	$(".en").css("display", "inline");
	$(".vn").css("display", "none");
	$('#calendar').fullCalendar('option', 'locale', 'en');
});
$(document).on("click", "li.vietnam-language", function(){
	$("span#flag-icon-language").html('<span class="flag-icon-size"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Flag_of_Vietnam.svg/1200px-Flag_of_Vietnam.svg.png"/></span>&nbsp;T . Việt');

	translator.lang("vn");
	localStorage.setItem('LANGUAGE', 'vn');

	$(".en").css("display", "none");
	$(".vn").css("display", "inline");
	$('#calendar').fullCalendar('option', 'locale', 'vi');
});

// Initially will load from localStorage
var currentLang = localStorage.getItem('LANGUAGE');
if (currentLang == "en") {
	$("li.english-language").click();
}
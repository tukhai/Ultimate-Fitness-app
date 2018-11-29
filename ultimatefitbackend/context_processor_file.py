from .dictionary import dictionary_translation

def common_header(request):
	return {
		"var_for_template" : "test_var",
	}


def translation_dictionary(request):
	dict_translation = dictionary_translation()
	return {
		'dict_translation': dict_translation
	}
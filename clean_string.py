import unicodedata

def cleanstr(input):
	input = input.replace('\\xa0',' ')
	input = input.replace(' \'\',','')
	input = input.replace('.','')
	return remove_accents(input)

def remove_accents(input):
    nfkd_form = unicodedata.normalize('NFKD', input)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii.decode("utf-8") 
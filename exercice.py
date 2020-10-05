#!/usr/bin/env python
# -*- coding: utf-8 -*-


def check_brackets(text, brackets):
	# ouvrants, fermants = brackets[0::2], brackets[1::2] # Permet d'obtenir juste les éléments d'index pair et impair, respectivement.
	opening_brackets = dict(zip(brackets[0::2], brackets[1::2]))
	closing_brackets = dict(zip(brackets[1::2], brackets[0::2]))
	bracket_stack = []
	for chr in text:
		# Chr est un caractère ouvrant
		if chr in opening_brackets:
			bracket_stack.append(chr)
		# Chr est un caractère fermant. Est-ce que la pile est vide ou le chr ouvrant associé n'est pas au top de la pile? Return False.
		elif chr in closing_brackets:
			if len(bracket_stack) == 0 or bracket_stack[-1] != closing_brackets[chr]:
				return False
			else:
				bracket_stack.pop()
	
	# Si bracket_stack n'est pas vide, faut retourner False.
	return len(bracket_stack) == 0

def remove_comments(full_text, comment_start, comment_end):
	# if comment_start not in full_text or comment_end not in full_text:
	# 	return None
	text = full_text
	while True:
		# Trouver le prochain début de commentaire
		start = text.find(comment_start)
		# Trouver la prochaine fin de commentaire
		end = text.find(comment_end)
		# Si aucun des deux trouvé
		if start == -1 and end == -1:
			# C'est bon
			return text
		# Si fermeture précède ouverture ou il mmanque soit un début ou une fin, return None
		if end < start or (start == -1) != (end == -1):
			return None
		# Enlever le commentaire de la string
		text = text[:start] + text[end + len(comment_end):]
		# C'est bon

def get_tag_prefix(text, opening_tags, closing_tags):
	# for t in opening_tags:
	# 	if text.startswith(t):
	# 		return(t, None)
	# for t in closing_tags:
	# 	if text.startswith(t)
	# 		return(None, t)
	for t in zip(opening_tags, closing_tags):
		if text.startswith(t[0]):
			return(t[0], None)
		if text.startswith(t[1]):
			return(None, t[1])
	return (None, None)

def check_tags(full_text, tag_names, comment_tags):
	text = remove_comments(full_text, *comment_tags) # whaaaaat? Ça déballe le tuple pour que chaque élément du tuple soit un argument de la fonction. Wow.
	if text is None:
		return False
	
	otags = {f"<{name}>": f"</{name}>" for name in tag_names}
	ctags = dict((v, k) for k, v in otags.items()) # Façon smart et usuelle d'inverser les éléments et les clés d'un dictionnaire dans un autre dictionnaire.

	tag_stack = []
	while len(text) != 0:
		tag = get_tag_prefix(text, otags.keys(), ctags.keys())
		# Quand on a un char ouvrant, on empile
		# Si ouvrant:
		if tag[0] is not None:
			# j'empile
			tag_stack.append(tag[0])
			text = text[len(tag[0]):]
		# Si fermant:
		elif tag[1] is not None:
			# Si pile vide OU match pas le haut de la pile:
			if len(tag_stack) == 0 or ctags[tag[1]] != tag_stack[-1]:
				# pas bon
				return False
			# On dépile et on avance.
			tag_stack.pop()
			text = text[len(tag[1]):]
		# Sinon
		else:
			# On avance de 1 caractère.
			text = text[1:]
	return len(tag_stack) == 0
	


if __name__ == "__main__":
	brackets = ("(", ")", "{", "}")
	yeet = "(yeet){yeet}"
	yeeet = "({yeet})"
	yeeeet = "({yeet)}"
	yeeeeet = "(yeet"
	print(check_brackets(yeet, brackets))
	print(check_brackets(yeeet, brackets))
	print(check_brackets(yeeeet, brackets))
	print(check_brackets(yeeeeet, brackets))
	print()

	spam = "Hello, /* OOGAH BOOGAH */world!"
	eggs = "Hello, /* OOGAH BOOGAH world!"
	parrot = "Hello, OOGAH BOOGAH*/ world!"
	print(remove_comments(spam, "/*", "*/"))
	print(remove_comments(eggs, "/*", "*/"))
	print(remove_comments(parrot, "/*", "*/"))
	print()

	otags = ("<head>", "<body>", "<h1>")
	ctags = ("</head>", "</body>", "</h1>")
	print(get_tag_prefix("<body><h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("<h1>Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("Hello!</h1></body>", otags, ctags))
	print(get_tag_prefix("</h1></body>", otags, ctags))
	print(get_tag_prefix("</body>", otags, ctags))
	print()

	spam = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    </title>"
		"  </head>"
		"  <body>"
		"    <h1>Hello, world</h1>"
		"    <!-- Les tags vides sont ignorés -->"
		"    <br>"
		"    <h1/>"
		"  </body>"
		"</html>"
	)
	eggs = (
		"<html>"
		"  <head>"
		"    <title>"
		"      <!-- Ici j'ai écrit qqch -->"
		"      Example"
		"    <!-- Il manque un end tag"
		"    </title>-->"
		"  </head>"
		"</html>"
	)
	parrot = (
		"<html>"
		"  <head>"
		"    <title>"
		"      Commentaire mal formé -->"
		"      Example"
		"    </title>"
		"  </head>"
		"</html>"
	)
	tags = ("html", "head", "title", "body", "h1")
	comment_tags = ("<!--", "-->")
	print(check_tags(spam, tags, comment_tags))
	print(check_tags(eggs, tags, comment_tags))
	print(check_tags(parrot, tags, comment_tags))
	print()


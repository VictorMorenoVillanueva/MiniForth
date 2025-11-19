ANTLR=antlr4
GRAMMAR=forth.g4

all: antlr

antlr: $(GRAMMAR)
	$(ANTLR) -Dlanguage=Python3 -no-listener -visitor $(GRAMMAR) 

test:
	python3 -m doctest -v test.txt

clean:
	rm -f *.interp *.tokens
	rm -f forthLexer.py forthParser.py forthListener.py forthVisitor.py

PEP := pep8
PYFLAKES := pyflakes
FLAKE8 := flake8

src := *.py

.PHONY: pep8 pyflakes flake8

pep8:
	-@ $(PEP) $(src)

pyflakes:
	-@ $(PYFLAKES) $(src)

flake8:
	-@ $(FLAKE8) $(src)


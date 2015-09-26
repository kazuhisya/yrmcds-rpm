NAME := yrmcds
VERSION := $(shell grep Version: $(NAME).spec | tr -s " "| cut -d " " -f 2)

CC = gcc
GCCVERSION_481 := $(shell expr `gcc -dumpversion | sed -e 's/\.\([0-9][0-9]\)/\1/g' -e 's/\.\([0-9]\)/0\1/g' -e 's/^[0-9]\{3,4\}$$/&00/'` \>= 40801)

rpm:
ifeq "$(GCCVERSION_481)" "1"
	spectool -g  $(NAME).spec
	mkdir -p dist/{BUILD,RPMS,SPECS,SOURCES,SRPMS,install}
	mv v$(VERSION).tar.gz dist/SOURCES/
	cp -pf *.patch dist/SOURCES/
	cp -pf $(NAME).service dist/SOURCES/
	rpmbuild -ba \
		--define "_topdir $(PWD)/dist" \
		--define "buildroot $(PWD)/dist/install" \
		--clean \
		$(NAME).spec
else
	@echo "C++ compiler too old..."
endif

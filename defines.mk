
-include my-defines.mk

DIST=dist

PLATFORM=$(shell uname)

#
# Handle multiple Python installs. What python are we using?
#

ifeq ($(PLATFORM), Linux)

TIME ?= $(shell which time)
YESTERDAY = $(shell date --date yesterday "%m/%d/%Y")
PYTHON2=$(shell which python)
PIP3=$(shell which pip3)
PYTHON3=$(shell which python3)

else ifeq ($(PLATFORM), Darwin) # MacOS

TIME ?= time
YESTERDAY = $(shell date -v-1d +"%m/%d/%Y")
PYTHON2=$(shell which python)
PIP3=$(shell which pip3)
PYTHON3=$(shell which python3)

else

TIME ?= $(shell which time)
PYTHON2=$(shell which python)
PIP3=$(shell which pip3)
PYTHON3=$(shell which python3)

endif

FLAKE8 ?= $(shell which flake8)
PYINSTALLER ?= $(shell which pyinstaller)



#PYTHON ?= ${PYTHON2}
PYTHON ?= $(PYTHON3)
PIP ?= $(PIP3)


#
# Install pip packages as user for devs and to system for pipeline runner
#
ifeq ($(USER), runner)

PIP_INSTALL_OPT ?=

else

PIP_INSTALL_OPT ?= --user

endif


ifeq ($(PYTHON),)
$(error Python not found)
endif
ifeq ($(PIP),)
$(error pip not found)
endif


export TIME PLATFORM PYTHON PIP PIP_INSTALL_OPT YESTERDAY PYINSTALLER FLAKE8

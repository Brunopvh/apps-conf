#!/usr/bin/env python3

from setuptools import setup
import os
import sys

file_setup = os.path.abspath(os.path.realpath(__file__))
dir_of_project = os.path.dirname(file_setup)

sys.path.insert(0, dir_of_project)

from apps_conf.__main__ import (
	__version__, 
	__author__,
	__repo__,
	__online_file__,
)

DESCRIPTION = 'Trabalha com a configuração de arquivos e diretórios de configuração.'
LONG_DESCRIPTION = 'Trabalha com a configuração de arquivos e diretórios de configuração.'

setup(
	name='apps_conf',
	version=__version__,
	description=DESCRIPTION,
	long_description=LONG_DESCRIPTION,
	author=__author__,
	author_email='brunodasill@gmail.com',
	license='MIT',
	packages=['apps_conf'],
	zip_safe=False,
	url='https://gitlab.com/bschaves/apps-conf',
	project_urls = {
		'Código fonte': __repo__,
		'Download': __online_file__,
	},
)



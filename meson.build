project('calculus',
          version: '0.1.0',
    meson_version: '>= 0.50.0',
  default_options: [ 'warning_level=2',
                   ],
)

i18n = import('i18n')


APPLICATION_ID = 'com.github.carlos157oliveira.Calculus'
PROJECT_RDNN_NAME = 'com.github.carlos157oliveira.Calculus'
PKGDATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), APPLICATION_ID)

#dependency('latex-base')


pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())

subdir('data')

#moduledir = join_paths(pkgdatadir, 'calculus')


python = import('python')
py_installation = python.find_installation('python3')


conf = configuration_data()
conf.set('PYTHON', py_installation.path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)


configure_file(
  input: 'calculus.in',
  output: 'calculus',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
)
'''
calculus_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'utils/dialogs.py'
]

install_data(
	calculus_sources,
	install_dir: moduledir
)
'''

install_subdir('calculus', install_dir: pkgdatadir)

subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')


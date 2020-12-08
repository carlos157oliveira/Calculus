project('calculus',
          version: '1.5.1',
    meson_version: '>= 0.50.0',
  default_options: [ 'warning_level=2',
                   ],
)

i18n = import('i18n')

APPLICATION_ID = 'com.github.carlos157oliveira.Calculus'
PROJECT_RDNN_NAME = 'com.github.carlos157oliveira.Calculus'
PKGDATA_DIR = join_paths(get_option('prefix'), get_option('datadir'), APPLICATION_ID)
PACKAGE_URL = 'https://carlos157oliveira.github.io/Calculus'
PACKAGE_URL_BUG = 'https://github.com/carlos157oliveira/Calculus/issues'

# dependency('latex-base')
pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())

subdir('data/ui/dialogs')
subdir('data')

python = import('python')
py_installation = python.find_installation('python3')

conf = configuration_data()
conf.set('app_id', APPLICATION_ID)
conf.set('PYTHON', py_installation.path())
conf.set('VERSION', meson.project_version())
conf.set('rdnn_name', PROJECT_RDNN_NAME)
conf.set('localedir', join_paths(get_option('prefix'), get_option('datadir'), 'locale'))
conf.set('pkgdatadir', pkgdatadir)


configure_file(
  input: 'calculus.in',
  output: 'calculus',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
)


install_subdir('calculus', install_dir: pkgdatadir)

subdir('po')

meson.add_install_script('build-aux/meson/postinstall.py')

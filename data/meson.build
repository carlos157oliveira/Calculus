#desktop_conf = configuration_data()
#desktop_conf.set('icon', 'integral')
'''
input: configure_file(
    output: PROJECT_RDNN_NAME + '.desktop.in',
    input: PROJECT_RDNN_NAME + '.desktop.in.in',
    configuration: desktop_conf)
'''
desktop_file = i18n.merge_file(
  input: 'org.example.App.desktop.in',
  #configuration: desktop_conf,
  output: 'org.example.App.desktop',
  type: 'desktop',
  po_dir: join_paths(meson.source_root(), 'po'),
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: true)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = i18n.merge_file(
  input: 'org.example.App.appdata.xml.in',
  output: 'org.example.App.appdata.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)


appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

install_data('org.example.App.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif

gnome = import('gnome')

gnome.compile_resources('calculus',
  'calculus.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

# Installing the default icon
icon_dir = 'icons/hicolor/48x48/apps'
install_data(
    join_paths(icon_dir, 'integral.png'),
    install_dir: join_paths(get_option('prefix'), get_option('datadir'), icon_dir)
)



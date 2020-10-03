desktop_conf = configuration_data()
desktop_conf.set('app_id', APPLICATION_ID)

desktop_file_in = configure_file(
  input: PROJECT_RDNN_NAME + '.desktop.in.in',
  output: PROJECT_RDNN_NAME + '.desktop.in',
  configuration: desktop_conf
)

desktop_file = i18n.merge_file(
  input: desktop_file_in,
  output: PROJECT_RDNN_NAME + '.desktop',
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

app_data = configuration_data()
app_data.set('app_id', APPLICATION_ID)

app_data_in = configure_file(
  input: PROJECT_RDNN_NAME + '.appdata.xml.in.in',
  output: PROJECT_RDNN_NAME + '.appdata.xml.in',
  configuration: app_data
)

appstream_file = i18n.merge_file(
  #input: PROJECT_RDNN_NAME + '.appdata.xml.in',
  input: app_data_in,
  output: PROJECT_RDNN_NAME + '.appdata.xml',
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

install_data(PROJECT_RDNN_NAME + '.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif

gnome = import('gnome')

gnome.compile_resources(PROJECT_RDNN_NAME,
  PROJECT_RDNN_NAME + '.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  source_dir: meson.current_build_dir()
)

# Installing the default icon
icon_dir = 'icons/hicolor/scalable/apps'
install_data(
    join_paths(icon_dir, 'com.github.carlos157oliveira.Calculus.svg'),
    install_dir: join_paths(get_option('prefix'), get_option('datadir'), icon_dir)
)

# prefix /app /icons/hicolor/scalable/apps
# datadir /app/share /icons/hicolor/scalable/apps



about_dialog_conf = configuration_data()
about_dialog_conf.set('version', meson.project_version())
about_dialog_conf.set('package_url', PACKAGE_URL)
about_dialog_conf.set('app_id', APPLICATION_ID)

about_dialog = configure_file(
  input: 'about_dialog.ui.in',
  output: 'about_dialog.ui',
  configuration: about_dialog_conf
)

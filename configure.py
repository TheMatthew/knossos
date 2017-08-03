## Copyright 2017 Knossos authors, see NOTICE file
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

import sys
import os.path
import subprocess
from codecs import open

os.chdir(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath('tools/common'))

from ninja_syntax import Writer
from configlib import *

UI_FILES = [
    'ui/flags.ui',
    'ui/gogextract.ui',
    'ui/hell.ui',
    'ui/install.ui',
    'ui/log_viewer.ui',
    'ui/mod_settings.ui',
    'ui/mod_versions.ui',
    'ui/select_list.ui'
]

JS_FILES = [
    'html/templates/kn-dev-mod.vue',
    'html/templates/kn-devel-page.vue',
    'html/templates/kn-drawer.vue',
    'html/templates/kn-dropdown.vue',
    'html/templates/kn-flag-editor.vue',
    'html/templates/kn-mod-buttons.vue',
    'html/templates/kn-mod.vue',
    'html/templates/kn-page.vue',
    'html/templates/kn-settings-page.vue',
    'html/js/translations.js',
    'html/js/main.js',
    'webpack.config.js'
]

RCC_FILES = [
    'knossos/data/hlp.png',
    'html/css/bootstrap.min.css',
    'html/css/font-awesome.min.css',
    'html/css/style.css',
    'html/fonts/fontawesome-webfont.woff',
    'html/fonts/fontawesome-webfont.ttf',
    'html/dist/bundle.js',
    'html/index.html',
    'html/images/dropdown-h.png',
    'html/images/modnotify_updating.png',
    'html/images/btn-blue-a.png',
    'html/images/icon-filter-a.png',
    'html/images/iconbtn-develop-h.png',
    'html/images/icon-update.png',
    'html/images/mod-retail.png',
    'html/images/icon-filter-h.png',
    'html/images/btn-green-h.png',
    'html/images/iconbtn-home-a.png',
    'html/images/btn-blue.png',
    'html/images/icon-settings.png',
    'html/images/modnotify_error.png',
    'html/images/scrollbtn-down-a.png',
    'html/images/btn-yellow.png',
    'html/images/scrollbtn-up-h.png',
    'html/images/modnotify_update.png',
    'html/images/btn-red-a.png',
    'html/images/scrollbtn-up.png',
    'html/images/btn-orange-a.png',
    'html/images/btn-red-h.png',
    'html/images/iconbtn-explore-h.png',
    'html/images/modnotify_ready.png',
    'html/images/iconbtn-explore-a.png',
    'html/images/scrollbtn-down.png',
    'html/images/btn-grey-a.png',
    'html/images/icon-settings-h.png',
    'html/images/btn-orange.png',
    'html/images/btn-link-red.png',
    'html/images/icon-help-h.png',
    'html/images/scrollbtn-down-h.png',
    'html/images/btn-link-blue-a.png',
    'html/images/icon-update-a.png',
    'html/images/iconbtn-home-h.png',
    'html/images/icon-filter.png',
    'html/images/btn-orange-h.png',
    'html/images/iconbtn-home.png',
    'html/images/iconbtn-develop.png',
    'html/images/modstock.jpg',
    'html/images/btn-link-red-a.png',
    'html/images/icon-settings-a.png',
    'html/images/icon-help.png',
    'html/images/btn-link-blue-h.png',
    'html/images/BG.png',
    'html/images/btn-link-blue.png',
    'html/images/icon-update-h.png',
    'html/images/iconbtn-develop-a.png',
    'html/images/dropdown.png',
    'html/images/btn-red.png',
    'html/images/dropdown-a.png',
    'html/images/btn-grey.png',
    'html/images/btn-link-red-h.png',
    'html/images/btn-blue-h.png',
    'html/images/btn-grey-h.png',
    'html/images/btn-yellow-h.png',
    'html/images/icon-help-a.png',
    'html/images/btn-green.png',
    'html/images/iconbtn-explore.png',
    'html/images/btn-green-a.png',
    'html/images/scrollbtn-up-a.png',
    'html/images/btn-yellow-a.png'
]

SRC_FILES = [
    'knossos/third_party/__init__.py',
    'knossos/third_party/cpuinfo.py',
    'knossos/ui/__init__.py',
    'knossos/__init__.py',
    'knossos/__main__.py',
    'knossos/bool_parser.py',
    'knossos/center.py',
    'knossos/clibs.py',
    'knossos/integration.py',
    'knossos/ipc.py',
    'knossos/launcher.py',
    'knossos/progress.py',
    'knossos/py2_compat.py',
    'knossos/qt.py',
    'knossos/repo.py',
    'knossos/runner.py',
    'knossos/settings.py',
    'knossos/tasks.py',
    'knossos/util.py',
    'knossos/web.py',
    'knossos/windows.py'
]

info('Checking Python version...')
if sys.hexversion < 0x20700 or (sys.hexversion > 0x30000 and sys.hexversion < 0x30200):
    fail('Need at least 2.7.0 or 3.2.0!')
else:
    info(' ok\n')

# Check if all required modules are available
check_module('setuptools')
check_module('PyQt5')
check_module('semantic_version')
check_module('six')
check_module('requests')
if sys.platform == 'win32':
    check_module('comtypes')

# We want to use the more modern QtWebEngine by default so we check for that first.
webkit = False
if not check_module('PyQt5.QtWebEngine', required=False):
    # If it's not available, we use QtWebKit as a fallback.
    check_module('PyQt5.QtWebKit')
    webkit = True
else:
    # We need QtWebChannel to communicate with the web page inside QtWebEngine.
    check_module('PyQt5.QtWebChannel')

# Look for the various programs we need.
pyuic = try_program([[sys.executable, '-mPyQt5.uic.pyuic'], ['pyuic5'], ['pyuic']], 'pyuic')
pylupdate = try_program([[sys.executable, '-mPyQt5.pylupdate_main'], ['pylupdate5'], ['pylupdate']], 'pylupdate', test_param='-version')

lupdate = find_program(['lupdate-qt5', 'lupdate'], 'lupdate')
# lrelease = find_program(['lrelease-qt5', 'lrelease'], 'lrelease')
rcc = find_program(['rcc-qt5', 'rcc'], 'rcc')
find_program(['7z', '7za'], '7zip')

node = find_program(['node', 'nodejs'], 'nodejs')
npm = find_program(['npm'], 'npm')

check_ctypes_lib(['libSDL2-2.0.so.0', 'SDL2', 'SDL2.dll', 'libSDL2.dylib'], 'SDL2')
check_ctypes_lib(['libopenal.so.1.15.1', 'openal', 'OpenAL', 'OpenAL32'], 'OpenAL')

info('Reading version...\n')
version = subprocess.check_output([sys.executable, 'setup.py', 'get_version']).decode('utf8').strip()

info('Writing knossos/data/resources.qrc...\n')

with open('knossos/data/resources.qrc', 'w') as stream:
    stream.write('<!DOCTYPE RCC><RCC version="1.0">\n')
    stream.write('<qresource>\n')

    for path in RCC_FILES:
        name = path
        if os.path.basename(path) == 'hlp.png':
            name = 'hlp.png'
        elif path.endswith('.out.js'):
            name = path[:-7] + '.js'

        stream.write('  <file alias="%s">%s</file>\n' % (name, os.path.abspath(path)))

    stream.write('</qresource>\n')
    stream.write('</RCC>')

info('Writing build.ninja...\n')

with open('build.ninja', 'w') as stream:
    n = Writer(stream)

    n.comment('Transformers')
    n.rule('uic', py_script('tools/common/uic.py', ['$in', '$out'] + pyuic), 'UIC $out')
    n.rule('rcc', cmd2str([rcc, '-binary', '$in', '-o', '$out']), 'RCC $out')
    n.rule('js_lupdate', py_script('tools/common/js_lupdate.py', ['-o', '$out', '$in']), 'JS-LUPDATE $out')
    n.rule('pylupdate', cmd2str(pylupdate + ['$in', '-ts', '$out']), 'PY-LUPDATE $out')
    n.rule('lupdate', cmd2str([lupdate, '$in', '-ts', '$out']), 'LUPDATE $out')
    n.rule('webpack', cmdenv([node, 'node_modules/webpack/bin/webpack.js'], {'USE_WEBKIT': webkit}), 'WEBPACK $out')

    n.rule('npm', cmd2str([npm, 'install']), 'NPM', pool='console')

    if sys.platform.startswith('linux'):
        n.rule('cat', 'cat $in > $out', 'CAT $out')

    n.comment('Files')
    ui_targets = build_targets(n, UI_FILES, 'uic', new_ext='py', new_path='knossos/ui')
    n.build('knossos/data/resources.rcc', 'rcc', 'knossos/data/resources.qrc', implicit=RCC_FILES)
    n.build('html/js/translations.js', 'js_lupdate', ['html/js/main.js'])
    n.build('locale/_py.ts', 'pylupdate', SRC_FILES)
    n.build('locale/_ui.ts', 'lupdate', ['locale/_py.ts', 'html/js/translations.js'] + UI_FILES)

    if webkit:
        n.comment('Install es6-shim for QtWebKit compatibility')
        n.rule('npm_es6', cmd2str([npm, 'install', 'es6-shim']), 'NPM es6-shim', pool='console')
        n.build('node_modules/es6-shim/package.json', 'npm_es6')

        JS_FILES.append('node_modules/es6-shim/package.json')

    n.comment("Install Webpack if it's missing")
    n.build('node_modules/webpack/bin/webpack.js', 'npm', implicit=['package.json', 'package-lock.json'])
    n.build('html/dist/bundle.js', 'webpack', JS_FILES, implicit=['node_modules/webpack/bin/webpack.js'])

    n.comment('Shortcuts')
    n.build('resources', 'phony', ui_targets + ['knossos/data/resources.rcc', 'html/js/translations.js'])

    n.comment('Scripts')
    n.rule('regen', py_script('configure.py', sys.argv[1:]), 'RECONFIGURE', generator=True)
    n.build('build.ninja', 'regen', ['configure.py', 'knossos/center.py'])

    setup_args = ['sdist']
    if check_module('wheel', required=False):
        setup_args.append('bdist_wheel')

    n.rule('dist', py_script('setup.py', setup_args), 'SDIST', pool='console')
    n.build('dist', 'dist', 'resources')

    n.rule('run', py_script('knossos/__main__.py'), 'RUN', pool='console')
    n.build('run', 'run', 'resources')

    n.rule('debug', cmdenv(py_script('knossos/__main__.py'), {'KN_DEBUG': 1, 'QTWEBENGINE_REMOTE_DEBUGGING': 4006}), 'DEBUG', pool='console')
    n.build('debug', 'debug', 'resources')

    if sys.platform == 'win32':
        n.comment('Win32')

        if check_module('PyInstaller', required=False):
            pyinstaller = 'cmd /C "cd releng\\windows && %s"' % cmd2str([sys.executable, '-OO', '-mPyInstaller', '-d', '--distpath=.\\dist', '--workpath=.\\build', 'Knossos.spec', '-y'])
            n.rule('pyinstaller', pyinstaller, 'PACKAGE', pool='console')
            n.build('pyi', 'pyinstaller', ['resources'] + SRC_FILES)

            nsis = find_program(['makensis', r'C:\Program Files (x86)\NSIS\makensis.exe', r'C:\Program Files\NSIS\makensis.exe'], 'NSIS', required=False)
            if nsis:
                n.rule('nsis', cmd2str([nsis, '/NOCD', '/DKNOSSOS_ROOT=.\\', '/DKNOSSOS_VERSION=%s' % version, '$in']), 'NSIS $out')
                n.build('releng/windows/dist/Knossos-%s.exe' % version, 'nsis', 'releng/windows/nsis/installer.nsi', implicit='pyi')
                n.build('releng/windows/dist/update-%s.exe' % version, 'nsis', 'releng/windows/nsis/updater.nsi', implicit='pyi')

                n.build('installer', 'phony', ['releng/windows/dist/Knossos-%s.exe' % version, 'releng/windows/dist/update-%s.exe' % version])

    if sys.platform == 'darwin':
        n.comment('macOS')

        if check_module('PyInstaller', required=False):
            pyinstaller = 'cd releng/macos && ' + cmd2str([sys.executable, '-OO', '-mPyInstaller', '-d', '--distpath=./dist', '--workpath=./build', 'Knossos.spec', '-y'])
            n.rule('pyinstaller', pyinstaller, 'PACKAGE', pool='console')
            n.build('pyi', 'pyinstaller', ['resources'] + SRC_FILES)

            dmgbuild = find_program(['dmgbuild'], 'dmgbuild', required=False)
            if dmgbuild:
                n.rule('dmgbuild', 'cd releng/macos && ' + cmd2str([dmgbuild, '-s', 'dmgbuild_cfg.py', 'Knossos', 'dist/Knossos-%s.dmg' % version]), 'DMG')
                n.build('releng/macos/dist/Knossos-%s.dmg' % version, 'dmgbuild', 'releng/macos/dmgbuild_cfg.py', implicit='pyi')

                n.build('dmg', 'phony', 'releng/macos/dist/Knossos-%s.dmg' % version)

info('\nDone! Use "ninja run" to start Knossos.\n')

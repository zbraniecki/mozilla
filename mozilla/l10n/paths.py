try:
    from configparser import ConfigParser, NoOptionError, NoSectionError
except ImportError:
    # python 2
    from ConfigParser import ConfigParser, NoOptionError, NoSectionError
import os

def get_modules(repo_path, app='browser'):
    inipath = os.path.join(repo_path,
                           app,
                           'locales',
                           'l10n.ini')
    dirs = _get_l10n_ini(inipath, repo_path)
    return dirs

def get_locales_path(code):
    if code == 'en-US':
        return os.path.join('locales', 'en-US')
    return ''

def _get_l10n_ini(path, repo_path):
    inipath = os.path.join(path)
    fh = open(inipath, 'r')
    cp = ConfigParser()
    cp.readfp(fh)
    fh.close()
    
    depth = cp.get('general', 'depth')
    try:
        all_url = os.path.join(repo_path, 
                               cp.get('general', 'all'))
    except (NoOptionError, NoSectionError):
        all_url = None
    base_url = os.path.join(repo_path, depth)

    includes = []
    try:
        for category, path in cp.items('includes'):
            includes.append((category, path))
    except NoSectionError:
        pass

    compares = []
    for path in cp.get('compare', 'dirs').split():
        compares.append(path)

    for c,p in includes:
        compares.extend(_get_l10n_ini(os.path.join(repo_path, p), repo_path))
    return compares

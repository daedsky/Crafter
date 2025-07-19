from enum import StrEnum


class AppInfo(StrEnum):
    VERSION = '0.0.2-dev'
    THEME_MODE_KEY = 'io.crafter.Crafter.ThemeMode'
    THEME_COLOR_KEY = 'io.crafter.Crafter.ThemeColor'
    LICENSE_AGREED_KEY = 'io.crafter.Crafter.LICENSE_AGREED'
    GIT_REPO_URL = 'https://github.com/daedsky/Crafter/'
    STORAGE_PERMS_DENIED = 'io.crafter.Crafter.StoragePermsDenied'
    PRIVACY_POLICY_URL = 'https://example.com'
    APP_LICENSE_URL = 'https://github.com/daedsky/Crafter/blob/master/LICENSE'

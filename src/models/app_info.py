from enum import StrEnum


class AppInfo(StrEnum):
    VERSION = '0.0.3'
    THEME_MODE_KEY = 'io.crafter.Crafter.ThemeMode'
    THEME_COLOR_KEY = 'io.crafter.Crafter.ThemeColor'
    LICENSE_AGREED_KEY = 'io.crafter.Crafter.LICENSE_AGREED'
    STORAGE_PERMS_DENIED = 'io.crafter.Crafter.StoragePermsDenied'
    GIT_REPO_URL = 'https://github.com/daedsky/Crafter/'
    PRIVACY_POLICY_URL = 'https://github.com/daedsky/Crafter/blob/master/docs/privacy_policy.md'
    APP_LICENSE_URL = 'https://github.com/daedsky/Crafter/blob/master/LICENSE'

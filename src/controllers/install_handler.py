from components import custom_controls as cc

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from views.install_layout import InstallLayout


# type hinting <end>

def install(install_layout: 'InstallLayout') -> None:
    cc.InfoAlertDialog(page=install_layout.page,
                       content_text='This is the FOSS version of the app. Please install PlayStore version of the the app to use this feature.',
                       title_text='FOSS').show()

import flet_permission_handler as fph
import flet as ft
from components.custom_controls import InfoAlertDialog
from models.app_info import AppInfo

# type hinting <start>
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app import CrafterApp
    from collections.abc import Callable


# type hinting <end>

class StoragePermsManager:
    def __init__(self, app: 'CrafterApp'):
        self.app = app
        self.page = app.page
        self.perms_handler = app.perms_handler
        self.PermTypeStorage = fph.PermissionType.MANAGE_EXTERNAL_STORAGE

    def check_ask_and_req_storage_perms(self, after_dialog_close_func: 'Callable' = None):
        if self.page.platform != ft.PagePlatform.ANDROID:
            if after_dialog_close_func is not None:
                after_dialog_close_func()
            return
        # if self.page.client_storage.get(AppInfo.STORAGE_PERMS_DENIED) is True:
        #     if after_dialog_close_func is not None:
        #         after_dialog_close_func()
        #     return
        status = self.perms_handler.check_permission(self.PermTypeStorage)

        if status == fph.PermissionStatus.GRANTED:
            if after_dialog_close_func is not None:
                after_dialog_close_func()
            return
        self.show_ask_perms_dialog(after_dialog_close_func=after_dialog_close_func)

    def show_ask_perms_dialog(self, after_dialog_close_func: 'Callable' = None):
        if self.page.platform != ft.PagePlatform.ANDROID:
            if after_dialog_close_func is not None:
                after_dialog_close_func()
            return
        dialog = InfoAlertDialog(page=self.page,
                                 content_text='''This application requires storage permissions to write files to "SELECTED DESTINATION FOLDER". Without this permission, the app may not work due to some permission issues with scoped storage.''',
                                 title_text='Permission Request')

        def close_dialog():
            self.page.close(dialog)
            if after_dialog_close_func is not None:
                after_dialog_close_func()

        def option_no():
            self.page.client_storage.set(AppInfo.STORAGE_PERMS_DENIED, True)
            close_dialog()

        def proceed_for_perms():
            self.request_storage_perms()
            close_dialog()

        dialog.actions = [ft.OutlinedButton('No (app may not work)', on_click=lambda _: option_no()),
                          ft.FilledButton('Grant', on_click=lambda _: proceed_for_perms())]
        dialog.show()

    def request_storage_perms(self) -> None | fph.PermissionStatus:
        if self.page.platform != ft.PagePlatform.ANDROID: return None
        req = self.perms_handler.request_permission(self.PermTypeStorage)
        if req != fph.PermissionStatus.GRANTED:
            InfoAlertDialog(page=self.page,
                            content_text="App may not work correctly.",
                            title_text="Storage Permission Denied").show()
            self.page.client_storage.set(AppInfo.STORAGE_PERMS_DENIED, True)
        return req

    def only_check_storage_perms(self):
        if self.page.platform != ft.PagePlatform.ANDROID:
            return type('MyClass', (), {'value': 'StoragePermission'})()
        return self.perms_handler.check_permission(self.PermTypeStorage)

    def is_storage_perms_granted(self):
        if self.page.platform != ft.PagePlatform.ANDROID:
            return 'StoragePerm'
        status = self.perms_handler.check_permission(self.PermTypeStorage)
        if status == fph.PermissionStatus.GRANTED:
            return True
        return status

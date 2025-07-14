import flet as ft


class ProcessDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page, title: str = 'Process Log', *args, **kwargs):
        self.page: ft.Page = page

        self.listile_prev_process: ft.ListTile | None = None
        self.prev_text: ft.Text | None = None

        title: ft.Text = ft.Text(title, color=ft.Colors.PRIMARY)

        self.done_btn: ft.TextButton = ft.TextButton('done', on_click=lambda _: page.close(self), disabled=True)
        self.column: ft.Column = ft.Column(scroll=ft.ScrollMode.ALWAYS, auto_scroll=True)

        super().__init__(*args, **kwargs, modal=True, title=title, content=self.column, scrollable=True,
                         actions=[self.done_btn])

    def add_text(self, text: str, *args, **kwargs):
        self.prev_text = ft.Text(text, *args, **kwargs)
        self.column.controls.append(self.prev_text)
        self.column.update()

    def edit_prev_text(self, msg: str, color: ft.Colors):
        self.prev_text.value += msg
        self.prev_text.color = color
        self.prev_text.update()

    def add_info_tile(self, title: str, subtitle: str):
        listile = ft.ListTile(title=ft.Text(title, color=ft.Colors.SECONDARY, height=15),
                              subtitle=ft.Text(subtitle, color=ft.Colors.TERTIARY),
                              leading=ft.Icon(ft.Icons.INFO_OUTLINED, color=ft.Colors.SECONDARY, size=20),
                              content_padding=0, visual_density=ft.VisualDensity.COMPACT, dense=True)
        self.column.controls.append(listile)
        self.column.update()

    def add_process_tile(self, title: str, subtitle: str):
        listile = ft.ListTile(title=ft.Text(title, color=ft.Colors.PRIMARY),
                              subtitle=ft.Text(subtitle, color=ft.Colors.SECONDARY),
                              trailing=ft.ProgressRing(width=10, height=10, stroke_width=2),
                              leading=ft.Icon(ft.Icons.API_ROUNDED, color=ft.Colors.PRIMARY),
                              content_padding=0, visual_density=ft.VisualDensity.COMPACT, dense=True)
        self.listile_prev_process = listile
        self.column.controls.append(listile)
        self.column.update()

    def prev_process_completed(self, code: int = 0, stderr: str = None):
        if code == 0:
            icon = ft.Icon(ft.Icons.DONE, size=20, color=ft.Colors.GREEN)
            self.listile_prev_process.leading.color = ft.Colors.GREEN_400
            self.listile_prev_process.title.color = ft.Colors.GREEN_700
            self.listile_prev_process.subtitle.color = ft.Colors.GREEN_400
        else:
            icon = ft.Icon(ft.Icons.ERROR_OUTLINE_OUTLINED, size=20, color=ft.Colors.RED)
            self.listile_prev_process.leading.color = ft.Colors.RED_400
            self.listile_prev_process.title.color = ft.Colors.RED_700
            self.listile_prev_process.subtitle.color = ft.Colors.RED_400
            self.listile_prev_process.subtitle.value += f'\n{stderr}'
        self.listile_prev_process.trailing = icon
        self.listile_prev_process.update()

    def enable_done_btn(self):
        self.done_btn.disabled = False
        self.done_btn.update()

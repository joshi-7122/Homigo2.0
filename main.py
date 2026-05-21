import flet as ft

def main(page: ft.Page):
    # Set the page background to match Onsitego
    page.bgcolor = "#fdfdfd"
    page.padding = 0
    page.title = "Homigo (Onsitego Replica)"

    # Build the Onsitego Navbar using pure Python controls
    navbar = ft.Container(
        bgcolor="#169ba6", 
        padding=ft.padding.symmetric(horizontal=40, vertical=15),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("onsitego", size=26, weight="bold", color="white"),
                ft.Row(
                    spacing=25,
                    controls=[
                        ft.Text("Device & Plans", color="white", weight="w500"),
                        ft.Text("Activate Plan", color="white", weight="w500"),
                        ft.ElevatedButton(
                            text="Sign In", 
                            bgcolor="white", 
                            color="#169ba6" 
                        )
                    ]
                )
            ]
        )
    )
    
    page.add(navbar)

ft.app(target=main, view=ft.AppView.WEB_BROWSER)

import flet as ft

def main(page: ft.Page):
    # --- Page Setup ---
    page.title = "Homigo UI"
    page.bgcolor = "#fdfdfd"
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO 

    # --- 1. Navigation Bar ---
    navbar = ft.Container(
        bgcolor="#169ba6",
        # FIX: Replaced symmetric with explicitly defining all sides
        padding=ft.padding.only(left=40, right=40, top=15, bottom=15),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(spacing=0, controls=[
                    ft.Text("onsite", size=26, weight="bold", color="white"),
                    ft.Text("go", size=26, weight="bold", color="#ffc107")
                ]),
                ft.Row(spacing=25, controls=[
                    ft.Text("Device & Plans", color="white", weight="w500"),
                    ft.Text("Activate Plan", color="white", weight="w500"),
                    ft.Text("Track Service Request", color="white", weight="w500"),
                    ft.ElevatedButton("Sign In", bgcolor="white", color="#169ba6", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))),
                    ft.Text("🛒", size=20)
                ])
            ]
        )
    )

    def create_testimonial(name, location, review):
        return ft.Container(
            bgcolor="white",
            padding=25,
            border_radius=8,
            border=ft.border.all(1, "#f0f0f0"),
            width=450, 
            shadow=ft.BoxShadow(blur_radius=15, color=ft.colors.with_opacity(0.03, "black")),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(width=60, height=60, bgcolor="#e0e0e0", border_radius=30),
                            ft.Text(name, weight="bold", size=13),
                            ft.Text(location, color="#777777", size=13)
                        ]
                    ),
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Text("5 ★★★★★", color="#f5b301", size=18),
                            ft.Text(f'"{review}"', italic=True, color="#555555", size=14),
                            ft.Text("Read more", color="#169ba6", size=13)
                        ]
                    )
                ]
            )
        )

    # --- 2. Testimonials Grid ---
    testimonials = ft.Row(
        wrap=True,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=30,
        controls=[
            create_testimonial("Snehan P Rajan", "Mumbai", "A friend recommended your InstaRepair service so I booked a service online for my water purifier and it was a good experience. Service was cashless and convenient."),
            create_testimonial("Shivani Choudhary", "New Delhi", "Good service. Your technician came with all tools and followed safety norms. He was polite and professional.")
        ]
    )

    def create_rating(icon_char, icon_color, text_color, count):
        return ft.Row(
            controls=[
                ft.Container(
                    width=45, height=45, border_radius=22.5, bgcolor="white",
                    alignment=ft.alignment.center,
                    border=ft.border.all(1, "#ddd") if icon_char == 'a' else None,
                    shadow=ft.BoxShadow(blur_radius=8, color=ft.colors.with_opacity(0.05, "black")),
                    content=ft.Text(icon_char, size=20, weight="bold", color=icon_color)
                ),
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Row(spacing=5, controls=[
                            ft.Text("4.5", size=18, weight="bold", color="#333"),
                            ft.Text("★★★★★", color="#f5b301", size=14)
                        ]),
                        ft.Text(f"{count} Reviews", color="#888888", size=13)
                    ]
                )
            ]
        )

    # --- 3. Aggregate Ratings Section ---
    ratings = ft.Container(
        border=ft.border.symmetric(horizontal=ft.border.BorderSide(1, "#f0f0f0")),
        # FIX: Replaced symmetric padding/margins
        padding=ft.padding.only(top=40, bottom=40),
        margin=ft.margin.only(top=40, bottom=40),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            wrap=True,
            controls=[
                create_rating("a", "black", "black", "6,000+"),
                create_rating("f", "#1877F2", "black", "1,500+"),
                create_rating("G", "#DB4437", "black", "2,200+")
            ]
        )
    )

    def create_partner(name, text_color, bg_color="white"):
        return ft.Container(
            bgcolor=bg_color,
            # FIX: Replaced symmetric padding
            padding=ft.padding.only(left=25, right=25, top=15, bottom=15),
            border_radius=6,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.with_opacity(0.04, "black")),
            content=ft.Text(name, size=24, weight="bold", color=text_color)
        )

    # --- 4. Partners Section ---
    partners = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("SPOTLIGHT", color="#169ba6", size=14, weight="bold"), 
            ft.Text("Our Partners", size=32, color="#222222", weight="bold"),
            ft.Container(height=20),
            ft.Row(
                wrap=True,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=40,
                controls=[
                    create_partner("amazon", "#444444"),
                    create_partner("croma", "white", "#111111"),
                    create_partner("vijay sales", "#d11212"),
                    create_partner("ICICI Bank", "#e36a25"),
                    create_partner("Delta", "#169ba6")
                ]
            )
        ]
    )

    # --- 5. Predictive Diagnostics Engine (Mockup) ---
    prediction_result = ft.Text("Awaiting input...", italic=True, color="#888888")

    def run_diagnostics(e):
        appliance = dd_appliance.value
        symptom = dd_symptom.value
        
        if appliance == "AC" and symptom == "Not Cooling":
            result = "Prediction: 85% chance of Low Refrigerant/Gas Leak. Recommended Action: Dispatch tech with R32 Gas cylinder."
            prediction_result.color = "red"
        elif appliance == "Washing Machine" and symptom == "Making Noise":
            result = "Prediction: 90% chance of Worn Drum Bearings. Recommended Action: Dispatch tech with replacement bearing kit."
            prediction_result.color = "orange"
        else:
            result = f"Analyzing {appliance} for '{symptom}'... (ML Model needs more data)"
            prediction_result.color = "#169ba6"
            
        prediction_result.value = result
        page.update() 

    dd_appliance = ft.Dropdown(
        label="Select Appliance",
        width=250,
        options=[
            ft.dropdown.Option("AC"),
            ft.dropdown.Option("Washing Machine"),
            ft.dropdown.Option("Water Purifier"),
        ],
    )
    
    dd_symptom = ft.Dropdown(
        label="Primary Symptom",
        width=250,
        options=[
            ft.dropdown.Option("Not Cooling"),
            ft.dropdown.Option("Making Noise"),
            ft.dropdown.Option("Won't Turn On"),
            ft.dropdown.Option("Leaking Water"),
        ],
    )

    diagnostics_section = ft.Container(
        bgcolor="#f4f9f9",
        padding=40,
        border_radius=10,
        # FIX: Replaced symmetric margin
        margin=ft.margin.only(top=40, bottom=40),
        border=ft.border.all(2, "#169ba6"),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("AI Predictive Diagnostics", size=28, weight="bold", color="#222222"),
                ft.Text("Identify the likely issue before the technician even arrives.", color="#555555"),
                ft.Container(height=20),
                ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[dd_appliance, dd_symptom]),
                ft.Container(height=10),
                ft.ElevatedButton("Run AI Analysis", bgcolor="#169ba6", color="white", on_click=run_diagnostics),
                ft.Container(height=20),
                ft.Container(
                    padding=15, 
                    bgcolor="white", 
                    border_radius=8, 
                    border=ft.border.all(1, "#ddd"),
                    content=prediction_result
                )
            ]
        )
    )

    # --- Assemble Everything onto the Page ---
    page.add(
        navbar,
        ft.Container(
            # FIX: Replaced symmetric padding
            padding=ft.padding.only(left=20, right=20, top=50, bottom=50),
            alignment=ft.alignment.center,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    diagnostics_section, 
                    testimonials,
                    ft.Container(
                        content=ft.Text("Read More...", color="#f5b301", weight="bold"),
                        margin=ft.margin.only(bottom=20)
                    ),
                    ratings,
                    partners
                ]
            )
        )
    )

# Run as a web app
ft.app(target=main, view=ft.AppView.WEB_BROWSER)

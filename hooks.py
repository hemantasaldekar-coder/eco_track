app_name = "eco_track"
app_title = "Eco Track"
app_publisher = "Developer"
app_description = "ESG Tracker"
app_email = "developer@example.com"
app_license = "MIT"

# Automatically triggers database setup when the app is installed
after_install = "eco_track.setup.after_install"

# Map the standard Delivery Note save event to your calculation logic
doc_events = {
    "Delivery Note": {
        "before_save": "eco_track.api.calculate_delivery_carbon"
    }
}

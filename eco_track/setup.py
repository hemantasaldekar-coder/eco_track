import frappe

MODULE_NAME = "Eco Track"
VEHICLE_EMISSION_FACTOR = "Vehicle Emission Factor"

def after_install():
    setup_eco_track()

def setup_eco_track():
    create_module_def()
    create_custom_doctype()
    create_custom_fields()
    create_workspace()

def create_module_def():
    """Creates the Desk module so Eco Track can have its own workspace."""
    if not frappe.db.exists("Module Def", MODULE_NAME):
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": MODULE_NAME,
            "app_name": "eco_track",
        }).insert(ignore_permissions=True)

def create_custom_doctype():
    """Programmatically creates the Vehicle Emission Factor Master DocType"""
    if not frappe.db.exists("DocType", VEHICLE_EMISSION_FACTOR):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": VEHICLE_EMISSION_FACTOR,
            "module": MODULE_NAME,
            "custom": 1,
            "autoname": "field:vehicle_type",
            "fields": [
                {"fieldname": "vehicle_type", "label": "Vehicle Type", "fieldtype": "Data", "reqd": 1, "in_list_view": 1},
                {"fieldname": "emission_factor", "label": "Emission Factor (g/km)", "fieldtype": "Float", "reqd": 1, "in_list_view": 1}
            ],
            "permissions": [
                {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1}
            ],
        })
        doc.insert(ignore_permissions=True)
    else:
        frappe.db.set_value("DocType", VEHICLE_EMISSION_FACTOR, "module", MODULE_NAME)

def create_custom_fields():
    """Programmatically injects custom ESG fields into Delivery Note"""
    fields = [
        {"dt": "Delivery Note", "fieldname": "custom_vehicle_type", "label": "Vehicle Type", "fieldtype": "Link", "options": VEHICLE_EMISSION_FACTOR, "insert_after": "customer"},
        {"dt": "Delivery Note", "fieldname": "custom_distance_km", "label": "Distance (KM)", "fieldtype": "Float", "insert_after": "custom_vehicle_type"},
        {"dt": "Delivery Note", "fieldname": "custom_carbon_footprint_kg", "label": "Carbon Footprint (kg CO2)", "fieldtype": "Float", "read_only": 1, "insert_after": "custom_distance_km"}
    ]
    for f in fields:
        if not frappe.db.exists("Custom Field", {"dt": f["dt"], "fieldname": f["fieldname"]}):
            frappe.get_doc({"doctype": "Custom Field", **f}).insert(ignore_permissions=True)

def create_workspace():
    """Creates the visible Eco Track workspace on Desk."""
    if frappe.db.exists("Workspace", MODULE_NAME):
        frappe.db.set_value("Workspace", MODULE_NAME, {
            "module": MODULE_NAME,
            "public": 1,
            "is_hidden": 0,
        })
        return

    frappe.get_doc({
        "doctype": "Workspace",
        "label": MODULE_NAME,
        "title": MODULE_NAME,
        "module": MODULE_NAME,
        "public": 1,
        "is_hidden": 0,
        "icon": "leaf",
        "indicator_color": "green",
        "content": "[]",
        "links": [
            {
                "label": VEHICLE_EMISSION_FACTOR,
                "link_type": "DocType",
                "link_to": VEHICLE_EMISSION_FACTOR,
                "type": "Link",
            }
        ],
    }).insert(ignore_permissions=True)

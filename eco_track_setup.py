import frappe

def after_install():
    create_custom_doctype()
    create_custom_fields()

def create_custom_doctype():
    """Programmatically creates the Vehicle Emission Factor Master DocType"""
    if not frappe.db.exists("DocType", "Vehicle Emission Factor"):
        doc = frappe.get_doc({
            "doctype": "DocType",
            "name": "Vehicle Emission Factor",
            "module": "Core",
            "custom": 1,
            "autoname": "field:vehicle_type",
            "fields": [
                {"fieldname": "vehicle_type", "label": "Vehicle Type", "fieldtype": "Data", "reqd": 1, "in_list_view": 1},
                {"fieldname": "emission_factor", "label": "Emission Factor (g/km)", "fieldtype": "Float", "reqd": 1, "in_list_view": 1}
            ]
        })
        doc.insert(ignore_permissions=True)

def create_custom_fields():
    """Programmatically injects custom ESG fields into Delivery Note"""
    fields = [
        {"dt": "Delivery Note", "fieldname": "custom_vehicle_type", "label": "Vehicle Type", "fieldtype": "Link", "options": "Vehicle Emission Factor", "insert_after": "customer"},
        {"dt": "Delivery Note", "fieldname": "custom_distance_km", "label": "Distance (KM)", "fieldtype": "Float", "insert_after": "custom_vehicle_type"},
        {"dt": "Delivery Note", "fieldname": "custom_carbon_footprint_kg", "label": "Carbon Footprint (kg CO2)", "fieldtype": "Float", "read_only": 1, "insert_after": "custom_distance_km"}
    ]
    for f in fields:
        if not frappe.db.exists("Custom Field", {"dt": f["dt"], "fieldname": f["fieldname"]}):
            frappe.get_doc({"doctype": "Custom Field", **f}).insert(ignore_permissions=True)

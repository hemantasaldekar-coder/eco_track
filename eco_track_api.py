import frappe
from frappe.utils import flt

def calculate_delivery_carbon(doc, method=None):
    """Triggered automatically before the Delivery Note saves"""
    doc.custom_carbon_footprint_kg = 0.0

    if doc.custom_vehicle_type and doc.custom_distance_km:
        # Fetch the baseline carbon configuration from the master DocType
        emission_factor = frappe.db.get_value(
            "Vehicle Emission Factor", 
            doc.custom_vehicle_type, 
            "emission_factor"
        )
        
        if emission_factor:
            # Formula: (Distance in KM * Grams per KM) / 1000 to output KG
            total_grams = flt(doc.custom_distance_km) * flt(emission_factor)
            doc.custom_carbon_footprint_kg = total_grams / 1000.0

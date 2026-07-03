# Eco Track

Eco Track is a custom Frappe/ERPNext app for tracking delivery-related carbon emissions. It adds ESG-focused fields to ERPNext Delivery Notes and calculates the carbon footprint based on vehicle type, distance, and configured emission factors.

## Features

- Adds an **Eco Track** workspace in the Frappe Desk.
- Creates a **Vehicle Emission Factor** master DocType.
- Adds custom carbon-tracking fields to **Delivery Note**:
  - Vehicle Type
  - Distance (KM)
  - Carbon Footprint (kg CO2)
- Automatically calculates delivery carbon footprint before a Delivery Note is saved.

## How The Calculation Works

Eco Track uses the following formula:

```text
Carbon Footprint (kg CO2) = Distance (KM) x Emission Factor (g/km) / 1000
```

The emission factor is read from the **Vehicle Emission Factor** master for the selected vehicle type.

## App Structure

```text
eco_track/
  pyproject.toml
  setup.py
  eco_track/
    __init__.py
    hooks.py
    api.py
    setup.py
    modules.txt
    patches.txt
    eco_track/
      __init__.py
    patches/
      __init__.py
      create_eco_track_workspace.py
```

## Installation

### Frappe Cloud

1. Push this repository to GitHub.
2. In Frappe Cloud, add this app from the GitHub repository:

   ```text
   https://github.com/hemantasaldekar-coder/eco_track
   ```

3. Install the app on your ERPNext site.
4. Run migration if required from Frappe Cloud.

### Local Bench

From your bench directory:

```bash
bench get-app https://github.com/hemantasaldekar-coder/eco_track
bench --site your-site-name install-app eco_track
bench --site your-site-name migrate
```

Replace `your-site-name` with your actual Frappe site name.

## Usage

1. Open the **Eco Track** workspace.
2. Create vehicle emission factor records in **Vehicle Emission Factor**.
3. Open or create a **Delivery Note**.
4. Select a vehicle type and enter the distance in kilometers.
5. Save the Delivery Note.
6. Eco Track calculates the carbon footprint automatically.

## Important Notes

- This app currently customizes the standard ERPNext **Delivery Note** DocType.
- Test on a staging site before installing on a production site.
- Make sure ERPNext is installed on the target site before installing this app.

## License

MIT

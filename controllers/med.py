# -*- coding: utf-8 -*-

"""
    Medical
    - Hospital Status Assessment and Request Management System
"""

if not settings.has_module(c):
    raise HTTP(404, body="Module disabled: %s" % c)

# -----------------------------------------------------------------------------
def index():
    """ Module's Home Page """

    from s3db.cms import cms_index
    return cms_index(c, alt_function="index_alt")

# -----------------------------------------------------------------------------
def index_alt():
    """
        Module homepage for non-Admin users when no CMS content found
    """

    # Just redirect to the Hospitals Map
    s3_redirect_default(URL(f = "hospital",
                            args = ["map"],
                            ))

# =============================================================================
def contact():
    """
        RESTful CRUD controller for Medical Contacts
    """

    return s3_rest_controller()

# =============================================================================
def hospital():
    """
        Main REST controller for Hospitals
    """

    # Custom Method to Assign HRs
    from s3db.hrm import hrm_AssignMethod
    s3db.set_method("med", "hospital",
                    method = "assign",
                    action = hrm_AssignMethod(component = "human_resource_site"),
                    )

    # Pre-processor
    def prep(r):
        from s3db.org import org_site_prep
        org_site_prep(r)

        if r.interactive:
            if r.component:
                # Configure tooltips and behaviors for specific components
                configure_component_tooltips(r.component_name, r.table)
            else:
                # General configurations for the main hospital table
                configure_hospital_table(r.table)

        elif r.representation == "plain":
            # Hide redundant location information in plain view
            r.table.location_id.readable = False

        return True
    s3.prep = prep

    from s3db.med import med_hospital_rheader
    return s3_rest_controller(rheader=med_hospital_rheader)

# =============================================================================

def configure_component_tooltips(component_name, table):
    """
    Configures tooltips and table settings for specific hospital components.
    """
    if component_name == "status":
        configure_status_tooltips(table)
    elif component_name == "bed_capacity":
        configure_bed_capacity_tooltips(table)
    elif component_name == "activity":
        configure_activity_tooltips(table)
    elif component_name == "image":
        disable_unnecessary_fields(table)
    elif component_name == "ctc":
        configure_ctc_tooltips(table)
        
# =============================================================================

def configure_status_tooltips(table):
    """
    Adds detailed tooltips for the hospital status component fields.
    """
    fields_tooltips = {
        "facility_status": ("Facility Status", "Status of the facility."),
        "facility_operations": ("Facility Operations", "Overall status of the facility operations."),
        "clinical_status": ("Clinical Status", "Status of the clinical departments."),
        "clinical_operations": ("Clinical Operations", "Overall status of the clinical operations."),
        "ems_status": ("Emergency Medical Services", "Status of operations/availability of emergency medical services at this facility."),
        "ems_reason": ("EMS Status Reasons", "Report the contributing factors for the current EMS status."),
        "or_status": ("OR Status", "Status of the operating rooms of this facility."),
        "or_reason": ("OR Status Reason", "Report the contributing factors for the current OR status."),
        "morgue_status": ("Morgue Status", "Status of morgue capacity."),
        "morgue_units": ("Morgue Units Available", "Number of vacant/available units to which victims can be transported immediately."),
        "security_status": ("Security Status", "Status of security procedures/access restrictions for the facility."),
        "staffing": ("Staffing Level", "Current staffing level at the facility."),
        "access_status": ("Road Conditions", "Describe the condition of the roads from/to the facility."),
    }
    apply_tooltips(table, fields_tooltips)
    
# =============================================================================

def configure_bed_capacity_tooltips(table):
    """
    Adds tooltips for the bed capacity component fields.
    """
    fields_tooltips = {
        "bed_type": ("Bed Type", "Specify the bed type of this unit."),
        "beds_baseline": ("Baseline Number of Beds", "Baseline number of beds of that type in this unit."),
        "beds_available": ("Available Beds", "Number of available/vacant beds of that type in this unit at the time of reporting."),
        "beds_add24": ("Additional Beds / 24hrs", "Number of additional beds of that type expected to become available in this unit within the next 24 hours."),
    }
    apply_tooltips(table, fields_tooltips)

# =============================================================================

def configure_activity_tooltips(table):
    """
    Adds tooltips for the hospital activity component fields.
    """
    fields_tooltips = {
        "date": ("Date & Time", "Date and time this report relates to."),
        "patients": ("Patients", "Number of in-patients at the time of reporting."),
        "admissions24": ("Admissions/24hrs", "Number of newly admitted patients during the past 24 hours."),
        "discharges24": ("Discharges/24hrs", "Number of discharged patients during the past 24 hours."),
        "deaths24": ("Deaths/24hrs", "Number of deaths during the past 24 hours."),
    }
    apply_tooltips(table, fields_tooltips)

# =============================================================================

def configure_ctc_tooltips(table):
    """
    Adds tooltips for the Cholera Treatment Center (CTC) component fields.
    """
    fields_tooltips = {
        "ctc": ("Cholera Treatment Center", "Does this facility provide a cholera treatment center?"),
        "number_of_patients": ("Current number of patients", "How many patients with the disease are currently hospitalized at this facility?"),
        "cases_24": ("New cases in the past 24h", "How many new cases have been admitted to this facility in the past 24h?"),
        "deaths_24": ("Deaths in the past 24h", "How many of the patients with the disease died in the past 24h at this facility?"),
        "icaths_available": ("Infusion catheters available", "Specify the number of available sets."),
        "icaths_needed_24": ("Infusion catheters need per 24h", "Specify the number of sets needed per 24h."),
        "infusions_available": ("Infusions available", "Specify the number of available units (litres) of Ringer-Lactate or equivalent solutions."),
        "infusions_needed_24": ("Infusions needed per 24h", "Specify the number of units (litres) of Ringer-Lactate or equivalent solutions needed per 24h."),
        "antibiotics_available": ("Antibiotics available", "Specify the number of available units (adult doses)."),
        "antibiotics_needed_24": ("Antibiotics needed per 24h", "Specify the number of units (adult doses) needed per 24h."),
        "problem_types": ("Current problems, categories", "Select all that apply."),
        "problem_details": ("Current problems, details", "Please specify any problems and obstacles with the proper handling of the disease in detail (in numbers, where appropriate)."),
    }
    apply_tooltips(table, fields_tooltips)

# =============================================================================

def apply_tooltips(table, fields_tooltips):
    """
    Applies tooltips to the fields of a table.
    """
    for field, (label, tooltip) in fields_tooltips.items():
        setattr(table[field], "comment", DIV(_class="tooltip", _title=f"{label}|{tooltip}"))

# =============================================================================

def disable_unnecessary_fields(table):
    """
    Disables fields irrelevant for the hospital image component.
    """
    for field in ["location_id", "organisation_id", "person_id"]:
        setattr(table[field], "readable", False)
        setattr(table[field], "writable", False)

# =============================================================================
def pharmacy():
    """
    RESTful CRUD controller for Pharmacies.
    """
    def prep(r):
        from s3db.org import org_site_prep
        org_site_prep(r)
        return True
    s3.prep = prep
    return s3_rest_controller()

# =============================================================================
def incoming():
    """
        Incoming Shipments for Sites

        Used from Requests rheader when looking at Transport Status
    """

    # @ToDo: Create this function!
    return s3db.inv_incoming()

# -----------------------------------------------------------------------------
def req_match():
    """ Match Requests """

    from s3db.inv import inv_req_match
    return inv_req_match()

# END =========================================================================


import arcpy
import os
from arcpy import env

env.workspace = 'C:/Users/cgate/Desktop/ArcPro_scratch/EEA_MLCA/EEA_MLCA_constraints.gdb'
env.overwriteOutput = True


arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="CDD_ZoningDistricts",
    selection_type="NEW_SELECTION",
    where_clause="ZONE_TYPE = 'C-1'",
    invert_where_clause=None
)
print(".")
arcpy.conversion.ExportFeatures(
    in_features="CDD_ZoningDistricts",
    out_features="Cambridge_C1_districts"
)
print(".")
arcpy.analysis.PairwiseClip(
    in_features="parcel_DB_statewide_zoning_join_largest_overlap",
    clip_features="Cambridge_C1_districts",
    out_feature_class="parcel_DB_Cambridge_C1_clip",
    cluster_tolerance=None,
    precision="MAX_PRECISION"
)
print(".")
arcpy.analysis.PairwiseErase(
    in_features="parcel_DB_Cambridge_C1_clip",
    erase_features="main_state_wide_urbansim_undevelopable_land_constraint",
    out_feature_class="parcel_Cambridge_C1_developable",
    cluster_tolerance=None
)
print(".")
arcpy.management.CalculateGeometryAttributes(
    in_features="parcel_Cambridge_C1_developable",
    geometry_property="lot_acres AREA",
    length_unit="",
    area_unit="ACRES_US",
    coordinate_system=None,
    coordinate_format="SAME_AS_INPUT"
)
print(".")
arcpy.management.CalculateGeometryAttributes(
    in_features="parcel_Cambridge_C1_developable",
    geometry_property="lot_sqft AREA",
    length_unit="",
    area_unit="SQUARE_FEET_US",
    coordinate_system=None,
    coordinate_format="SAME_AS_INPUT"
)
print(".")
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="parcel_Cambridge_C1_developable",
    selection_type="NEW_SELECTION",
    where_clause="POLY_TYPE NOT IN ('FEE', 'TAX')",
    invert_where_clause=None
)
print(".")
arcpy.management.CalculateField(
    in_table="parcel_Cambridge_C1_developable",
    field="max_dua",
    expression="0",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
print(".")
arcpy.management.CalculateField(
    in_table="parcel_Cambridge_C1_developable",
    field="max_far",
    expression="0",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
print(".")
arcpy.management.CalculateField(
    in_table="parcel_Cambridge_C1_developable",
    field="max_lot_units",
    expression="0",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
print(".")
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="parcel_Cambridge_C1_developable",
    selection_type="NEW_SELECTION",
    where_clause="POLY_TYPE IN ('FEE', 'TAX')",
    invert_where_clause=None
)
print(".")
arcpy.analysis.PairwiseBuffer(
    in_features="parcel_Cambridge_C1_developable",
    out_feature_class="Cambridge_C1_parcels_10ft_setback_poly",
    buffer_distance_or_field="-10 Feet",
    dissolve_option="NONE",
    dissolve_field=None,
    method="PLANAR",
    max_deviation="0 Meters"
)
print(".")
arcpy.management.CalculateGeometryAttributes(
    in_features="Cambridge_C1_parcels_10ft_setback_poly",
    geometry_property="bldg_footprint_sqft AREA",
    length_unit="",
    area_unit="SQUARE_FEET_US",
    coordinate_system=None,
    coordinate_format="SAME_AS_INPUT"
)
print(".")
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="Cambridge_C1_parcels_10ft_setback_poly",
    selection_type="NEW_SELECTION",
    where_clause="lot_sqft >= 5000",
    invert_where_clause=None
)
print(".")
arcpy.conversion.ExportFeatures(
    in_features="Cambridge_C1_parcels_10ft_setback_poly",
    out_features="Cambridge_C1_parcels_5000sqft"
)
print(".")
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="Cambridge_C1_parcels_10ft_setback_poly",
    selection_type="NEW_SELECTION",
    where_clause="lot_sqft < 5000 And bldg_footprint_sqft >= 1000",
    invert_where_clause=None
)
print(".")
arcpy.conversion.ExportFeatures(
    in_features="Cambridge_C1_parcels_10ft_setback_poly",
    out_features="Cambridge_C1_parcels_4story"
)
print(".")
arcpy.management.SelectLayerByAttribute(
    in_layer_or_view="parcel_DB_statewide_zoning_join_largest_overlap",
    selection_type="NEW_SELECTION",
    where_clause="POLY_TYPE NOT IN ('FEE', 'TAX')",
    invert_where_clause=None
)
print(".")
keep_fields = ["OBJECTID","geom","max_dua","max_far","zoning"] # Always keep geometry

# Create FieldMappings object
field_mappings = arcpy.FieldMappings()
field_mappings.addTable("parcel_DB_statewide_zoning_join_largest_overlap")

# Identify and remove fields NOT in your 'keep' list
for field in field_mappings.fields:
    if field.name not in keep_fields:
        field_mappings.removeFieldMap(field_mappings.findFieldMapIndex(field.name))
print(".")
arcpy.conversion.ExportFeatures(
    in_features="parcel_DB_statewide_zoning_join_largest_overlap",
    out_features="parcel_DB_ROW",
    field_mapping=field_mappings
)
print(".")
arcpy.management.CalculateField(
    in_table="parcel_DB_ROW",
    field="max_dua",
    expression="0",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
print(".")
arcpy.management.CalculateField(
    in_table="parcel_DB_ROW",
    field="max_far",
    expression="0",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
print(".")
arcpy.management.CalculateField(
    in_table="parcel_DB_ROW",
    field="zoning",
    expression="'parcel_ROW'",
    expression_type="PYTHON3",
    code_block="",
    field_type="TEXT",
    enforce_domains="NO_ENFORCE_DOMAINS"
)
print(".")
arcpy.analysis.PairwiseDissolve(
    in_features="parcel_DB_ROW",
    out_feature_class="parcel_DB_ROW_dissolve",
    dissolve_field="max_dua;max_far;zoning",
    statistics_fields=None,
    multi_part="MULTI_PART",
    concatenation_separator=""
)
print(".")
arcpy.analysis.PairwiseErase(
    in_features="statewide_zoning_3A_update_20260323_dissolve",
    erase_features="parcel_DB_ROW_dissolve",
    out_feature_class="statewide_zoning_3A_update_20260323_erase_ROW",
    cluster_tolerance=None
)
print(".")
arcpy.management.Merge(
    inputs="statewide_zoning_3A_update_20260323_erase_ROW;parcel_DB_ROW",
    output="statewide_zoning_ROW_adjusted",
    field_mappings=None,
    add_source="NO_SOURCE_INFO",
    field_match_mode="AUTOMATIC"
)
print("Complete")

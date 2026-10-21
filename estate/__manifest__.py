{
  "name": "Kenya Real Estate",
  "version": "19.0.0",
  "depends": ["base"],
  "application": True, #This line will say the module is an App, not a module
  "installable": True,
  "data": [
      "security/ir.model.access.csv",
      "views/estate_property_type_views.xml",
      "views/estate_property_tag_views.xml",
      "views/estate_property_offer_views.xml",
      "views/estate_property_views.xml",
      "views/estate_menus.xml"
  ]
}

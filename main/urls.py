from django.urls import path
from .views import (
    index,
    toggle_compatibility,
    list_components,
    add_to_build,
    show_build,
    component_detail,
    remove_from_build,
    export_build,
    import_build,
    ajax_search, 
    save_build_to_db, 
    my_builds,
    delete_build
)

app_name = "main"

urlpatterns = [
    path("", index, name="index"),
    path("toggle_compatibility/", toggle_compatibility, name="toggle_compatibility"),
    path("category/<str:category>/", list_components, name="list_components"),
    path("add/<str:category>/<int:item_id>/", add_to_build, name="add_to_build"),
    path("show_build/", show_build, name="show_build"),
    path(
        "detail/<str:category>/<int:item_id>/",
        component_detail,
        name="component_detail",
    ),
    path("remove/<str:category>/", remove_from_build, name="remove_from_build"),
    path("export_build/", export_build, name="export_build"),
    path("import_build/", import_build, name="import_build"),
    path('ajax_search/<str:category>/', ajax_search, name='ajax_search'),
    path('save_build_to_db/', save_build_to_db, name='save_build_to_db'),
    path('my_builds/', my_builds, name='my_builds'),
    path('delete_build/<int:build_id>/', delete_build, name='delete_build'),

]

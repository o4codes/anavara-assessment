REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "src.includes.helpers.drf_helpers.pagination.AppPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "src.includes.helpers.drf_helpers.permissions.AppModelPermissions",
    ],
    # "EXCEPTION_HANDLER": "src.includes.errors.exception_handler.api_exception_handler",
    "COMPONENT_SPLIT_REQUEST": True,
}

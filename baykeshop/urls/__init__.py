from .shop import app_name, path
from .shop import urlpatterns
from baykeshop.views.docs import index

urlpatterns += [
    path("docs/", index.HomeView.as_view(), name="doc_index")
]

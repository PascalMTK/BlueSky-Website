from django.urls import path

from . import views

app_name = "staffpanel"

urlpatterns = [
    path("", views.home, name="home"),
    path("transferts/", views.transfers_list, name="transfers"),
    path("transferts/<int:pk>/statut/<str:status>/", views.update_transfer_status, name="update_transfer_status"),
    path("comptes-epargne/", views.savings_accounts, name="savings_accounts"),
    path("comptes-epargne/<int:pk>/", views.savings_account_detail, name="savings_account_detail"),
    path("comptes-epargne/<int:pk>/activer/", views.activate_account, name="activate_account"),
    path("comptes-epargne/<int:pk>/refuser/", views.reject_account, name="reject_account"),
    path("operations/<int:pk>/confirmer/", views.confirm_operation, name="confirm_operation"),
    path("operations/<int:pk>/rejeter/", views.reject_operation, name="reject_operation"),
    path("messages/", views.messages_list, name="messages"),
    path("messages/<int:pk>/", views.message_detail, name="message_detail"),
    path("messages/<int:pk>/traiter/", views.toggle_message_handled, name="toggle_message_handled"),
    path("messages/<int:pk>/supprimer/", views.delete_message, name="delete_message"),
    path("publications/", views.posts, name="posts"),
    path("publications/nouvelle/", views.post_form, name="post_create"),
    path("publications/<int:pk>/modifier/", views.post_form, name="post_edit"),
    path("publications/<int:pk>/publier/", views.toggle_post_published, name="toggle_post_published"),
    path("publications/<int:pk>/supprimer/", views.delete_post, name="delete_post"),
]

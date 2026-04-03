from django.urls import path

from job import views

urlpatterns = [
    path("",views.JobListView.as_view(),name="job-list"),
    path("signup/",views.SignupView.as_view(),name="signup"),
    path("job-detail/<int:pk>/",views.JobDetailView.as_view(),name="job-detail"),
    path("create-job/",views.CreateJobView.as_view(),name="create"),
    path("apply-job/<int:pk>/",views.ApplyJobView.as_view(),name="apply-job"),
    path("dashboard/",views.DashboardView.as_view(),name="dashboard"),
    path("update-status/<int:pk>/<str:status>/",views.UpdateStatusView.as_view(),name='update')
]
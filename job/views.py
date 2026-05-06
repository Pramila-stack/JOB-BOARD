from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,DetailView,View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from job.forms import ApplicationForm, JobForm, SignupForm
from job.models import Application, Job
from django.db.models import Q
from django.contrib.auth import login
from .utils import send_notification_email



# Create your views here.
class JobListView(ListView):
    model = Job
    template_name = "job_list.html"
    context_object_name = "jobs"
    paginate_by = 3

    def get_queryset(self):
        queryset = Job.objects.all().order_by("-created_at")

        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)|
                Q(location__icontains=query)|
                Q(company__icontains=query)
            )
        return queryset

class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("job-list")

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return super().form_valid(form)
    
class JobDetailView(DetailView):
    model = Job
    template_name = "job_detail.html"
    context_object_name = "job"

class CreateJobView(LoginRequiredMixin,CreateView):
    model = Job
    template_name = "create_job.html"
    form_class = JobForm
    success_url = reverse_lazy("job-list")

    def form_valid(self, form):
        if self.request.user.profile.role != "employer":
            return redirect("job-list")
        form.instance.posted_by = self.request.user
        return super().form_valid(form)
    
class ApplyJobView(LoginRequiredMixin,CreateView):
    model = Application
    template_name = "apply_job.html"
    form_class = ApplicationForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        job = get_object_or_404(Job,pk=self.kwargs['pk'])
        user = self.request.user
        if Application.objects.filter(user=user,job=job).exists():
            return redirect("dashboard")
        form.instance.user=user
        form.instance.job = job
        response = super().form_valid(form)

        # Notify Employer
        send_notification_email(
            subject=f"New Applicant for {self.object.job.title}",
            template_name="new_applicant.html",
            context={'applicant': self.request.user, 'job': self.object.job},
            recipient_list=[self.object.job.posted_by.email]
        )
        return response

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.profile.role == "employer":
            context['jobs'] = Job.objects.filter(posted_by=user).order_by('-created_at')
        else:
            context['applications'] = Application.objects.filter(user=user).order_by('-applied_at')

        return context
    
class UpdateStatusView(LoginRequiredMixin,View):
    def get(self,request,pk,status):
        app = get_object_or_404(Application,pk=pk)

        if app.job.posted_by != request.user:
            return redirect("dashboard")
        app.status = status
        app.save()

        # Notify Seeker
        send_notification_email(
            subject=f"Update on your application for {app.job.title}",
            template_name="status_update.html",
            context={'status': status, 'job': app.job},
            recipient_list=[app.user.email]
        )

        return redirect("dashboard")
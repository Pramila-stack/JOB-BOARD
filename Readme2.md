<!-- JobCreateView -->
form.instance.posted_by = self.request.user 
→ assigns the logged-in user as the job’s poster.

<!-- ApplyJobView -->
job = get_object_or_404(Job, pk=self.kwargs['pk'])
user = self.request.user
👉 Means:
“Find the job the user is applying to from the URL and get the logged-in user who is applying to it.”

<!-- if Application.objects.filter(user=user,job=job).exists():
            return redirect("dashboard") -->
means checking if the same user has already applied to this job
left user and job is of model and right is from the above ->user = self.request.user

👉 It prevents duplicate applications
<!-- 🔹 What would happen WITHOUT it? -->
If you remove this:
Same user can click Apply multiple times

<!-- form.instance.user = user
form.instance.job = job -->
This line is needed because 
<!-- Your ApplicationForm only has: -->
fields = ["cv", "cover_letter"]

❗ It does NOT include:
user,job
But your model requires them.

🔹 So what you do
1️⃣
<!-- form.instance.user = user -->
👉 “Set the applicant (who is applying)”
<!-- form.instance.job = job -->
👉 “Set the job they are applying to”


<!-- context['jobs'] = Job.objects.filter(posted_by=user) -->
👉 Meaning:“Show all jobs posted by this user”




<!-- dashboard.html -->
<!-- {% for app in job.applications.all %} -->
. Without it, your dashboard for employers wouldn’t know which users applied for their jobs.

<!-- job = models.ForeignKey(Job, ..., related_name="applications_job") -->
→ This creates a reverse relationship from a Job to all its applications.
Django automatically allows you to do:
<!-- job.applications_job.all() -->
This fetches all Application objects where job = job.


<!-- 1️⃣ Looping through user applications
{% for app in applications %} -->
applications comes from your DashboardView context:
context['applications'] = Application.objects.filter(user=user)


<!-- Dashboard.html ko applications last part -->
Let’s break app.job.pk into tiny pieces:
How app.job.pk instead of job.pk

🔹 Step 1: What is app?
<!-- {% for app in applications %} -->
app = one Application object
Example:
Application object:
user = pramila
job = "Python Developer"

🔹 Step 2: What is app.job?
From your model:
job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications_job")

👉 This means:

Every Application belongs to one Job
So you can access that job using:
app.job

✔️ This gives you the Job object

🔹 Step 3: What is pk?
pk = primary key (ID) of any object
Every model object automatically has it

Example:

Job:
id (pk) = 5
title = "Django Developer"
🔹 Step 4: Combine it
app.job.pk

<!-- {% url 'update-status' app.id 'accepted' %} -->

👉 To build or this builds a URL like:
/update-status/5/accepted/
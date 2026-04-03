UpdateStatus by means "accepted","rejected" and "pending".
<!-- def get(self, request, pk, status): -->

This view only handles GET requests.
pk → the primary key of the Application you want to update.
status → the new status to set ("accepted" or "rejected").
Example URL might be: /status/5/accepted/.

<!-- app = get_object_or_404(Application, pk=pk) -->

Fetches the Application object with the given pk.
If no application exists with that ID, Django returns a 404 error.


<!-- if app.job.posted_by != request.user:
    return redirect("dashboard") -->

Checks if the logged-in user is the one who posted the job.
Only the employer who posted the job can update application statuses.
If not, it redirects to the dashboard (prevents unauthorized changes).

<!-- app.status = status
app.save() -->

Sets the application's status field to the new value (accepted or rejected).
Saves the change to the database.
return redirect("dashboard")
After updating, the user is redirected back to the dashboard.


<!-- if app.job.posted_by != request.user:
    return redirect("dashboard") -->
explanation of app.job.posted_by

<!-- app = get_object_or_404(Application, pk=pk) -->
app = one Application object
Example:
<!-- Application: -->
user = ram
job = "Django Developer"

🔹 Step 2: app.job
From your model:
job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications_job")

👉 This means:

Every Application belongs to one Job
So:
app.job
✔️ gives you the Job object

🔹 Step 3: posted_by

From your Job model:
posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobss")

👉 This means:
Every Job is created by a User (employer)


<!-- We use View instead of UpdateView because: -->

We are not updating through a form, we are just changing one field (status) quickly via URL.

🔹 What you’re doing now
<!-- app.status = status
app.save() -->
No form
No user input page
Just clicking a link like:
/update-status/5/accepted/
👉 This is a simple action, not a full update form.

🔹 Why NOT UpdateView
UpdateView is used when:
You show a form

<!-- SaveJobView -->
SavedJobs.objects.get_or_create(
    user=request.user,
    job=job
)

👉 It means:“Save this job for this user — but don’t duplicate it”

🔍 Break it:
request.user → currently logged-in user
job → the job we just fetched

So it tries to find:
(user = logged-in user, job = this job)

<!-- SavedJobs.objects.get_or_create -->
If Found,
Return the existing object.
Do NOT create a new one
Step 3: If NOT found ❌
Create new object:
SavedJobs.objects.create(user=request.user, job=job)
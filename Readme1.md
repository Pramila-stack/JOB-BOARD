🔹 1️⃣ posted_by = models.ForeignKey(...)
<!-- posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs") -->

one user can post many jobs so we can do user.jobs.all(jobs posted by this user)
👉 What it means:
Each Job is linked to a User
That user is the employer who posted the job

🔍 Parts:

<!-- ForeignKey(User) -->
👉 “Each Job is posted by one User, but one User can post many Jobs.”
So:
1 User → many Jobs
Each Job → 1 User

related_name="jobs"
→ Allows you to do this:
<!-- user.jobs.all() -->
👉 Example:
user = request.user
user.jobs.all()

<!-- is_active = models.BooleanField(default=True) -->
This means:
Show only jobs where is_active = True
Hide jobs where is_active = False

🔹 Model start
<!-- class Application(models.Model): -->
👉 This creates a table called Application
👉 It stores job applications submitted by users

<!-- user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications") -->
👉 The person who applied (job seeker)

Important:
<!-- Each Application belongs to ONE User
One User can have MANY Applications -->

🔥 In simple words-->👉 “This field stores who applied for the job.”
Reverse access:
user.applications.all()


<!-- job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name="applications") -->
Each Application belongs to ONE Job
One Job can have MANY Applications

<!-- class Meta:
    unique_together = ('user','job') -->
Prevents duplicate applications by the same user.


🔹 Model start
<!-- class SavedJob(models.Model): -->

👉 This creates a table called SavedJob
👉 It stores:➡️ which user saved which job

<!-- user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_jobs") -->
👉 Meaning:The user who saved the job
Each SavedJob belongs to ONE user
One user can have MANY saved jobs

<!-- user.saved_jobs.all() -->
👉 Gets all saved jobs (records) of that user

🔹 2️⃣ job (ForeignKey)
<!-- job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="saved_by") -->
👉 Meaning:
The job that was saved
Each SavedJob belongs to ONE job
One job can be saved by MANY users

<!-- job.saved_by.all() -->
👉 Gets all users who saved that job

{% if user.profiles.role == "" %}
<!-- user is a field inside Profile model and because the user has related names "profiles",we can do user.profiles.role -->
Super short explanation
<!-- Profile has a field-> user = OneToOneField(User, related_name="profiles") -->

That means from a User object, you get its Profile via user.profiles
Then you can access the role:
user.profiles.role
So it’s User → Profile → role.
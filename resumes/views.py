from django.shortcuts import render, redirect
from .forms import ResumeForm, JobApplicationForm, Resume, JobApplication
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from django.contrib import messages
from django.db import IntegrityError





def user_resume(request):
    resume = Resume.objects.filter(user=request.user).first()
    return render(request, 'user_resume.html', {'resume': resume})

@login_required
def create_resume(request):
    if hasattr(request.user, 'resume'):
        messages.info(request, "У вас уже есть резюме. Вы можете его редактировать.")
        return redirect('job_list')
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user  # устанавливаем текущего пользователя как владельца резюме
            resume.save()
            return redirect('user_resume')
    else:
        form = ResumeForm()
    return render(request, 'create_resume.html', {'form': form})

@login_required
def edit_resume(request, pk):
    resume = Resume.objects.get(pk=pk)
    if request.user != resume.user:
        return redirect('resume_detail', pk=resume.pk)  # если пользователь пытается редактировать чужое резюме

    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('user_resume')
    else:
        form = ResumeForm(instance=resume)
    return render(request, 'edit_resume.html', {'form': form})

from django.shortcuts import get_object_or_404

@login_required
def delete_resume(request, pk):
    try:
        # Получаем резюме текущего пользователя
        resume = Resume.objects.get(user=request.user)
        resume.delete()  # Удаляем резюме
        messages.success(request, "Ваше резюме успешно удалено.")
    except Resume.DoesNotExist:
        messages.error(request, "У вас нет резюме для удаления.")

    return redirect('job_list')



@login_required
def apply_for_job(request, job_id):
    job = Job.objects.get(id=job_id)
    resume = Resume.objects.filter(user=request.user).first()

    if not resume:
        messages.error(request, "У вас нет резюме. Создайте его, чтобы откликнуться.")
        return redirect('create_resume')

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                application.job = job
                application.user = request.user
                application.resume = resume
                application.save()
                messages.success(request, "Вы успешно откликнулись на вакансию.")
            except IntegrityError:
                messages.error(request, "Вы уже откликнулись на эту вакансию.")
            return redirect('job_detail', pk=job.id)
    else:
        form = JobApplicationForm()

    return render(request, 'apply_for_job.html', {'form': form, 'job': job, 'resume': resume})

@login_required
def view_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)  # Получаем вакансию, принадлежащую текущему работодателю
    applications = JobApplication.objects.filter(job=job)  # Все отклики на эту вакансию

    if request.method == 'POST':
        # Обработка действий (утверждение отклика или пометка как прочитанный)
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')

        if application_id:
            application = get_object_or_404(JobApplication, id=application_id, job=job)

            if action == 'approve':
                application.is_approved = True
                application.save()
                messages.success(request, f"Отклик кандидата {application.user.username} утвержден.")
            elif action == 'mark_read':
                application.is_read = True
                application.save()
                messages.success(request, f"Отклик кандидата {application.user.username} помечен как прочитанный.")

            return redirect('view_applications', job_id=job.id)

    return render(request, 'view_applications.html', {'job': job, 'applications': applications})
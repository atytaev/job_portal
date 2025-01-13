from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import Job
from .forms import JobForm, JobFilterForm
from django.contrib import messages

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def job_list(request):
    jobs = Job.objects.all()
    form = JobFilterForm(request.GET)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        company = form.cleaned_data.get('company')
        location = form.cleaned_data.get('location')

        if title:
            jobs = jobs.filter(title__icontains=title)
        if company:
            jobs = jobs.filter(company_name__icontains=company)
        if location:
            jobs = jobs.filter(location__icontains=location)

        salary_min = request.GET.get('salary_min')
        salary_max = request.GET.get('salary_max')
        if salary_min:
            jobs = jobs.filter(salary__gte=salary_min)
        if salary_max:
            jobs = jobs.filter(salary__lte=salary_max)
    return render(request, 'job_list.html',  {'jobs': jobs})


@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    similar_jobs = get_similar_jobs(pk)
    return render(request,
        'job_detail.html', {
        'job': job,
        'similar_jobs': similar_jobs,
    })


@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.company = request.user.company_name
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(
        request,
        'job_form.html',
        {'form': form}
    )

@login_required
def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm(instance=job)
    return render(request, 'job_detail.html', {'form': form})

def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    # Убедитесь, что текущий пользователь — это создатель вакансии
    if job.user == request.user:
        job.delete()
        messages.success(request, "Вакансия была успешно удалена.")
    else:
        messages.error(request, "Вы не можете удалить чужую вакансию.")
    return redirect('job_сompany')  # Перенаправление на список вакансий


@login_required
def job_сompany(request):
    jobs = Job.objects.filter(company=request.user.company_name)
    print(f"Found jobs: {jobs}")
    return render(request, 'job_сompany.html', {'jobs': jobs})


def get_similar_jobs(pk):
    # Получаем текущую вакансию
    current_job = Job.objects.get(id=pk)
    jobs = Job.objects.exclude(id=pk)  # Исключаем текущую вакансию

    # Получаем названия всех вакансий
    job_titles = [job.title for job in jobs]
    job_ids = [job.id for job in jobs]

    # Добавляем текущую вакансию в список для анализа
    job_titles.append(current_job.title)

    # Векторизация через TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(job_titles)

    # Считаем косинусное сходство
    similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Сортируем по схожести
    similar_indices = np.argsort(similarity[0])[::-1][:5]  # Топ-5 похожих вакансий
    similar_job_ids = [job_ids[i] for i in similar_indices]

    # Получаем объекты вакансий
    similar_jobs = Job.objects.filter(id__in=similar_job_ids)
    return similar_jobs
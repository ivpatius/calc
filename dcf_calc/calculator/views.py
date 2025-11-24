# calculator/views.py
from django.shortcuts import render
from .forms import DCFForm
from .logic import compute_dcf


def dcf_view(request):
    result = None

    if request.method == 'POST':
        form = DCFForm(request.POST)
        if form.is_valid():
            result = compute_dcf(form.cleaned_data)
    else:
        form = DCFForm()

    return render(request, 'calculator/dcf_form.html', {
        'form': form,
        'result': result,
    })

from django.shortcuts import render
from .forms import AnalysisForm
from .utils import process_data

def dashboard_view(request):
    results = None
    if request.method == 'POST':
        form = AnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            # End-to-end flow: Load -> Compute -> Flag -> Rank -> Visualize
            results = process_data(
                request.FILES['dataset'], 
                form.cleaned_data['silence_threshold']
            )
    else:
        form = AnalysisForm()

    context = {
        'form': form,
        'results': results,
    }
    return render(request, 'core/dashboard.html', context)

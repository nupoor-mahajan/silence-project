from django.shortcuts import render, redirect
from .forms import AnalysisForm
from .utils import process_data

# --- 1. STATIC PAGES ---
def index_view(request):
    return render(request, 'core/index.html')

def about_view(request):
    return render(request, 'core/about.html')

def working_view(request):
    return render(request, 'core/working.html')

# --- 2. LOGIC PAGES ---
def upload_view(request):
    """
    Combined Upload & Results View.
    """
    results = None
    
    if request.method == 'POST':
        form = AnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                dataset = request.FILES['dataset']
                # Use default threshold if hidden/missing
                threshold = form.cleaned_data.get('silence_threshold') or 0.5
                
                # Run Analysis
                results = process_data(dataset, threshold)
            except Exception as e:
                print(f"❌ Processing Error: {e}")
        else:
            print(f"❌ Form Error: {form.errors}")
    else:
        form = AnalysisForm()

    return render(request, 'core/upload.html', {'form': form, 'results': results})

def results_view(request):
    """
    If a user clicks 'Results' in the navbar, redirect them 
    to the Upload page (since that is where results appear now).
    """
    return redirect('upload')

# In core/views.py

# ... existing static pages ...
def working_view(request):
    return render(request, 'core/working.html')

# --- ADD THIS NEW FUNCTION ---
def guide_view(request):
    return render(request, 'core/guide.html')

# ... existing upload_view ...
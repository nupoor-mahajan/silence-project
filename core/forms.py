from django import forms

class AnalysisForm(forms.Form):
    # CSV Ingestion
    dataset = forms.FileField(label="Upload Complaint Dataset (CSV)")
    # Threshold Customization
    silence_threshold = forms.FloatField(
        initial=0.5, 
        min_value=0.1, 
        max_value=5.0,
        label="Silence Threshold (% of Avg Density)",
        widget=forms.NumberInput(attrs={'step': '0.1', 'class': 'civic-input'})
    )
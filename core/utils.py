import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Backend for server-side rendering
import matplotlib.pyplot as plt
import io
import base64

def process_data(file_obj, threshold_ratio):
    # 1. Ingestion
    df = pd.read_csv(file_obj)
    
    # 2. Compute Complaint Density (Complaints per 1000 people)
    df['density'] = (df['complaints'] / df['population']) * 1000
    
    # 3. Analytics: Summary Stats
    mean_density = df['density'].mean()
    median_density = df['density'].median()
    
    # 4. AI/ML: Statistical Anomaly Detection (Z-Score)
    if df['density'].std() == 0:
        df['density_z'] = 0
    else:
        df['density_z'] = (df['density'] - mean_density) / df['density'].std()
    
    # 5. Flagging Rules
    cutoff = mean_density * float(threshold_ratio)
    df['is_silent'] = df['density'] < cutoff
    
    # 6. AI: Early Warning & Fear Indicator
    df['trend_gap'] = df['history_avg'] - df['complaints']
    
    df['fear_score'] = np.where(
        (df['is_silent']) & (df['trend_gap'] > 0), 
        (df['trend_gap'] / df['population']) * 100, 
        0
    )

    # 7. Visualization: The Silence Map (Scatter Plot)
    plt.figure(figsize=(10, 6), facecolor='#F6F8FA')
    ax = plt.gca()
    ax.set_facecolor='#F6F8FA'
    
    normal = df[~df['is_silent']]
    if not normal.empty:
        plt.scatter(normal['population'], normal['complaints'], 
                    color='#4C6A85', alpha=0.6, s=50, label='Standard Reporting')
    
    silent = df[df['is_silent']]
    if not silent.empty:
        plt.scatter(silent['population'], silent['complaints'], 
                    color='#D97742', s=100, edgecolors='#1F3A5F', linewidth=1.5, label='Flagged Silence')

    plt.title('Silence Map: Population vs. Reported Issues', 
              color='#1F3A5F', pad=20)
    plt.xlabel('Population')
    plt.ylabel('Complaint Volume')
    plt.grid(True, linestyle='--', alpha=0.3, color='#4C6A85')
    plt.legend(frameon=False)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    chart_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    # 8. Ranking Pipeline
    ranked_silent = df[df['is_silent']].sort_values(by='density', ascending=True)
    
    # 9. Return Data
    return {
        'chart': chart_data,
        'stats': {
            'mean': float(mean_density),
            'median': float(median_density),
            'flagged_count': int(len(silent))
        },
        'ranked_regions': ranked_silent.to_dict('records'),
        'full_data': df.to_dict('records')
    }
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def load_and_prepare_data() -> pd.DataFrame:
    """데이터를 로드하고 전처리하는 함수"""
    df = pd.read_csv('website_wata.csv')
    return df

def analyze_traffic_sources(df: pd.DataFrame) -> Dict:
    """트래픽 소스별 주요 지표 분석"""
    metrics = {}
    
    for source in df['Traffic Source'].unique():
        source_data = df[df['Traffic Source'] == source]
        metrics[source] = {
            '평균 페이지뷰': source_data['Page Views'].mean(),
            '평균 세션시간': source_data['Session Duration'].mean(),
            '평균 이탈률': source_data['Bounce Rate'].mean(),
            '평균 체류시간': source_data['Time on Page'].mean(),
            '평균 이전방문': source_data['Previous Visits'].mean(),
            '평균 전환율': source_data['Conversion Rate'].mean()
        }
    
    return metrics

def create_visualizations(df: pd.DataFrame):
    """데이터 시각화 함수"""
    # 1. 트래픽 소스별 평균 지표 비교
    plt.figure(figsize=(15, 10))
    metrics = ['Page Views', 'Session Duration', 'Bounce Rate', 
              'Time on Page', 'Previous Visits', 'Conversion Rate']
    
    for i, metric in enumerate(metrics, 1):
        plt.subplot(2, 3, i)
        sns.boxplot(x='Traffic Source', y=metric, data=df)
        plt.title(f'트래픽 소스별 {metric}')
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('traffic_source_metrics.png')
    plt.close()
    
    # 2. 상관관계 히트맵 (수치형 데이터만)
    numeric_columns = ['Page Views', 'Session Duration', 'Bounce Rate', 
                      'Time on Page', 'Previous Visits', 'Conversion Rate']
    plt.figure(figsize=(10, 8))
    correlation = df[numeric_columns].corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
    plt.title('지표간 상관관계')
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png')
    plt.close()

def print_insights(metrics: Dict):
    """분석 결과 출력"""
    print("\n=== 트래픽 소스별 주요 지표 분석 ===\n")
    
    for source, data in metrics.items():
        print(f"\n[{source} 트래픽 분석]")
        for metric, value in data.items():
            print(f"{metric}: {value:.2f}")

def main():
    # 데이터 로드 및 전처리
    df = load_and_prepare_data()
    
    # 트래픽 소스별 분석
    metrics = analyze_traffic_sources(df)
    
    # 시각화 생성
    create_visualizations(df)
    
    # 분석 결과 출력
    print_insights(metrics)

if __name__ == "__main__":
    main() 
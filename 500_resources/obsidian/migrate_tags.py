"""
MECE 태그 체계 마이그레이션 스크립트
- 200_Books, .obsidian, Templates, .trash 폴더 제외
- frontmatter의 tags/tag 를 MECE 체계로 변환
- dry_run 모드로 미리보기 후 실행
"""

import os
import re
import sys

VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXCLUDE_DIRS = {
    '200_Books', '.obsidian', '.trash', 'Templates', '.git',
    'node_modules', '.stversions',
}

# ============================================================
# TAG MAPPING: old_tag → new_tag
#   None  = remove (무의미한 태그)
#   str   = 1:1 변환
#   tuple = 1:N 변환 (여러 태그로 분리)
# ============================================================

TAG_MAP = {
    # ── dev/ 소프트웨어 개발 ──────────────────────────
    'Java': 'dev/java',
    'java': 'dev/java',
    '자바개발': 'dev/java',
    'JavaSyntax': 'dev/java',
    'java문법': 'dev/java',
    'java-programming': 'dev/java',
    'java-projects': 'dev/java',
    'Java-Development': 'dev/java',
    'Java-Classes': 'dev/java',
    'Java-Objects': 'dev/java',
    'Java-Constructor': 'dev/java',
    'Java_best_practices': 'dev/java',
    'Javatutorial': 'dev/java',
    'java_tutorial': 'dev/java',
    'Java-vs-Python': 'dev/java',
    '자바문법': 'dev/java',
    '변수': 'dev/java',
    '타입': 'dev/java',
    '타입변환': 'dev/java',
    '자료형': 'dev/java',
    '변수범위': 'dev/java',
    '조건문': 'dev/java',
    '반복문': 'dev/java',
    '비교연산자': 'dev/java',
    '반복명령': 'dev/java',
    '흐름제어': 'dev/java',
    '객체지향프로그래밍': 'dev/java',
    '생성자': 'dev/java',
    '메소드': 'dev/java',
    '파라미터': 'dev/java',
    '오버로딩': 'dev/java',
    '식별자': 'dev/java',
    '기본값': 'dev/java',
    '메모리': 'dev/java',
    '클래스': 'dev/java',
    '클래스구현': 'dev/java',
    'ClassImplementation': 'dev/java',
    'Class': 'dev/java',
    'switchcase': 'dev/java',
    'weekday': 'dev/java',
    'memory': 'dev/java',
    'string': 'dev/java',
    'null': 'dev/java',
    'garbagecollection': 'dev/java',
    'arrays': 'dev/java',
    'data-structures': 'dev/java',
    'loops': 'dev/java',
    'average-calculation': 'dev/java',
    'element-access': 'dev/java',
    'basic-datatypes': 'dev/java',
    'data-storage': 'dev/java',
    'enumeration': 'dev/java',
    'category': None,  # too generic, often a book category
    'byte': 'dev/java',
    'short': 'dev/java',
    'memory_optimization': 'dev/java',
    'file_processing': 'dev/java',
    'network_communication': 'dev/java',
    'bitwise_operations': 'dev/java',
    'embedded_systems': 'dev/java',
    'operators': 'dev/java',
    'OperatorPrecedence': 'dev/java',
    'Inheritance': 'dev/java',
    'Polymorphism': 'dev/java',
    'Encapsulation': 'dev/java',
    'AbstractClasses': 'dev/java',
    'InterfaceVsAbstractClass': 'dev/java',
    'abstract-class': 'dev/java',
    'interface': 'dev/java',
    'reuse': 'dev/java',
    'maintenance': 'dev/java',
    'Parent/Children': 'dev/java',
    'Parent': 'dev/java',
    'DataTypes': 'dev/java',
    'Variables': 'dev/java',
    'datatype': 'dev/java',
    '프로그래밍입문': 'dev/java',
    '코드작성': 'dev/java',
    'input/output': 'dev/java',
    'input': 'dev/java',
    'systemIO': 'dev/java',
    '예외처리': 'dev/java',
    'try-catch-finally': 'dev/java',
    'exception-class': 'dev/java',
    '실행예외': 'dev/java',
    'exception-handling': 'dev/java',
    '예외떠넘기기': 'dev/java',
    'JDK': 'dev/java',
    'programming-language': 'dev/java',
    'development-environment': 'dev/java',
    'ErrorHandling': 'dev/java',
    'Python-Init': 'dev/python',
    'Object-Initialization': 'dev/java',
    'Parameter-Constructor': 'dev/java',
    'Method-vs-Constructor': 'dev/java',

    'Python': 'dev/python',
    'python': 'dev/python',
    '파이썬': 'dev/python',
    'Flask': 'dev/python',
    'Django': 'dev/python',
    'Unpacking': 'dev/python',
    'ForLoop': 'dev/python',
    'Tuple': 'dev/python',
    'Built-inFunctions': 'dev/python',
    'Errors': 'dev/python',

    'JavaScript': 'dev/js',
    'JS': 'dev/js',
    'HTML/JavaScript': 'dev/js',

    'SQL': 'dev/sql',
    'sql': 'dev/sql',
    'query': 'dev/sql',
    'SQLSyntax': 'dev/sql',
    'sqlSyntax': 'dev/sql',
    'storedprocedure': 'dev/sql',
    'mariadb': 'dev/sql',
    'MySQL': 'dev/sql',
    'inparameter': 'dev/sql',
    'outparameter': 'dev/sql',
    'inoutparameter': 'dev/sql',
    'case': 'dev/sql',
    'cte': 'dev/sql',
    'with': 'dev/sql',
    'join': 'dev/sql',
    'lead': 'dev/sql',
    'lag': 'dev/sql',
    'merge': 'dev/sql',
    'pivot': 'dev/sql',
    'unpivot': 'dev/sql',
    'subqueries': 'dev/sql',
    'view': 'dev/sql',
    'window': 'dev/sql',
    'SQLSTATE': 'dev/sql',
    'DatabaseErrors': 'dev/sql',
    'CustomCodes': 'dev/sql',
    'ErrorRange': 'dev/sql',
    'ErrorLimits': 'dev/sql',
    'UserDefinedErrors': 'dev/sql',
    'rdms': 'dev/db',

    'database': 'dev/db',
    '데이터베이스': 'dev/db',
    'indexing': 'dev/db',

    'OOP': 'dev/oop',
    'object-oriented-programming': 'dev/oop',
    'ObjectOrientedProgramming': 'dev/oop',
    'Object-Oriented Programming': 'dev/oop',
    'SOLID': 'dev/oop',
    'DIP': 'dev/oop',
    'ISP': 'dev/oop',
    'SRP': 'dev/oop',
    'LSP': 'dev/oop',
    'DesignPattern': 'dev/oop',
    'Software-Design': 'dev/oop',
    'software-design': 'dev/oop',
    'TemplateMethodPattern': 'dev/oop',
    'ReusableCode': 'dev/oop',
    'uml': 'dev/oop',
    'class-diagram': 'dev/oop',
    'object-oriented-design': 'dev/oop',
    'associations': 'dev/oop',
    'composition': 'dev/oop',
    'aggregation': 'dev/oop',
    'coupling': 'dev/oop',
    'maintainability': 'dev/oop',
    'testability': 'dev/oop',
    'convention': 'dev/oop',
    'conventions': 'dev/oop',

    'HTML': 'dev/web',
    'API': 'dev/web',
    'APIIntegration': 'dev/web',
    'api': 'dev/web',
    'websockets': 'dev/web',
    '웹사이트': 'dev/web',
    '웹디자인': 'dev/web',

    'Flutter': 'dev/mobile',
    'AndroidSDK': 'dev/mobile',
    'Setup': 'dev/mobile',
    'SDK': 'dev/mobile',
    'FlutterDoctor': 'dev/mobile',
    'CommandLineTools': 'dev/mobile',

    'JUnit': 'dev/test',

    'programming': 'dev',
    'ProgrammingLanguages': 'dev',
    'coding': 'dev',
    'development': 'dev',
    '개발': 'dev',
    '프로그래밍': 'dev',
    'IDE': 'dev',
    '개발도구': 'dev',
    'DevelopmentTools': 'dev',
    '소프트웨어공학': 'dev',
    '개발방법론': 'dev',
    'syntax': 'dev',

    # ── data/ 데이터 & 분석 ──────────────────────────
    'DataAnalysis': 'data/analysis',
    '데이터분석': 'data/analysis',
    'EDA': 'data/analysis',
    'analysis': 'data/analysis',
    'CohortAnalysis': 'data/analysis',
    '코호트분석': 'data/analysis',
    'FunnelAnalysis': 'data/analysis',
    '퍼널분석': 'data/analysis',
    'ABTesting': 'data/analysis',
    'ABTest': 'data/analysis',
    'AB테스트': 'data/analysis',
    'A/B테스팅': 'data/analysis',
    '게임데이터분석': 'data/analysis',
    'GameDataAnalysis': 'data/analysis',
    '게임분석방법론': 'data/analysis',
    'GameAnalyticsMethodology': 'data/analysis',
    '웹로그분석': 'data/analysis',
    'ProductAnalytics': 'data/analysis',
    '제품분석': 'data/analysis',
    '리텐션분석': 'data/analysis',
    'RetentionAnalysis': 'data/analysis',
    'ecommerce': 'data/analysis',
    'introduction': 'data/analysis',
    'variability': 'data/analysis',

    'Statistics': 'data/stats',
    'statistics': 'data/stats',
    'probability': 'data/stats',
    'Probability': 'data/stats',
    'HypothesisTesting': 'data/stats',
    '가설검정': 'data/stats',
    'ANOVA': 'data/stats',
    'anova': 'data/stats',
    'CentralLimitTheorem': 'data/stats',
    '중심극한정리': 'data/stats',
    '통계분석': 'data/stats',
    'StatisticalAnalysis': 'data/stats',
    '통계': 'data/stats',
    '기술통계': 'data/stats',
    'DescriptiveStatistics': 'data/stats',
    '확률분포': 'data/stats',
    'ProbabilityDistribution': 'data/stats',
    '회귀분석': 'data/stats',
    'RegressionAnalysis': 'data/stats',
    'rv': 'data/stats',
    'pmf': 'data/stats',
    'crv': 'data/stats',
    'pdf': 'data/stats',
    'cdf': 'data/stats',
    'ols': 'data/stats',
    'AIC': 'data/stats',
    'ModelSelection': 'data/stats',
    'InformationTheory': 'data/stats',
    'Bayes': 'data/stats',
    'KDE': 'data/stats',
    'LogLikelihood': 'data/stats',
    'MLE': 'data/stats',
    'Optimization': 'data/stats',
    'StatisticalMethods': 'data/stats',
    'StratifiedSampling': 'data/stats',
    'SamplingMethod': 'data/stats',
    'DataCollection': 'data/stats',
    'RepresentativeSample': 'data/stats',
    '분산분석': 'data/stats',

    'DataVisualization': 'data/viz',
    '데이터시각화': 'data/viz',
    '시각화': 'data/viz',
    'Visualization': 'data/viz',
    'Dashboard': 'data/viz',
    'PowerBI': 'data/viz',
    'Tableau': 'data/viz',
    'plotly': 'data/viz',
    'folium': 'data/viz',
    'seaborn': 'data/viz',

    'MachineLearning': 'data/ml',
    '머신러닝': 'data/ml',
    'DeepLearning': 'data/ml',
    '딥러닝': 'data/ml',
    'machine_learning': 'data/ml',
    'clustering': 'data/ml',
    'DBSCAN': 'data/ml',
    'density_based_clustering': 'data/ml',
    'unsupervised_learning': 'data/ml',
    'outlier_detection': 'data/ml',
    'k-means': 'data/ml',
    'segmentation': 'data/ml',
    '자연어처리': 'data/ml',
    '컴퓨터비전': 'data/ml',
    '이미지인식': 'data/ml',
    'DiscriminantAnalysis': 'data/ml',
    'ClusterAnalysis': 'data/ml',
    '군집분석': 'data/ml',
    'ConjointAnalysis': 'data/ml',

    'BigQuery': 'data/engineering',
    'bigquery': 'data/engineering',
    'DataWarehouse': 'data/engineering',
    'OLAP': 'data/engineering',

    'DataCleansing': 'data/preprocessing',
    'DataPreprocessing': 'data/preprocessing',
    '데이터전처리': 'data/preprocessing',
    '데이터프로세싱': 'data/preprocessing',
    'crawling': 'data/preprocessing',
    'scrapping': 'data/preprocessing',
    'selenium': 'data/preprocessing',
    'beautifulsoup': 'data/preprocessing',
    'beatufiulSoup': 'data/preprocessing',
    'pandas': 'data/preprocessing',
    'ListCleaning': 'data/preprocessing',
    'GDPR': 'data/preprocessing',

    'data': 'data',
    'data_analysis': 'data/analysis',
    '데이터과학': 'data',
    'DataScience': 'data',
    'DataMining': 'data',
    '데이터분석가': 'data',
    'DataAnalyst': 'data',
    'data analysis': 'data/analysis',

    # ── ai/ 인공지능 ─────────────────────────────────
    '생성AI': 'ai/genai',
    'GenerativeAI': 'ai/genai',
    'PromptEngineering': 'ai/prompt',
    'promptEngineering': 'ai/prompt',
    'prompt': 'ai/prompt',
    'AIAgent': 'ai/agent',
    'MCP': 'ai/mcp',
    'NotebookLM': 'ai/genai',
    'perplexity': 'ai/genai',
    '논문봇': 'ai/genai',
    'scispace': 'ai/genai',
    '플랏봇': 'ai/genai',
    '딴지봇': 'ai/genai',
    'Scopus': 'ai/genai',
    'opcua': 'ai',
    'plcdata': 'ai',
    'plc': 'ai',

    # ── infra/ 인프라 & DevOps ───────────────────────
    'Git': 'infra/git',
    '깃': 'infra/git',
    'GitWorkflow': 'infra/git',
    'GitCommands': 'infra/git',
    'git-branching': 'infra/git',
    'version-control': 'infra/git',
    'VersionControl': 'infra/git',
    '버전관리': 'infra/git',
    'GitHub': 'infra/git',
    'Github': 'infra/git',
    '깃허브': 'infra/git',
    '브랜치': 'infra/git',
    '코드리뷰': 'infra/git',
    'CodeReview': 'infra/git',
    'Pre-commit': 'infra/git',
    'PullRequest': 'infra/git',
    'IssueTracking': 'infra/git',
    'Release': 'infra/git',
    '풀리퀘스트': 'infra/git',
    '이슈트래킹': 'infra/git',
    '릴리즈': 'infra/git',
    '코드관리': 'infra/git',
    '개발워크플로우': 'infra/git',
    'software-development': 'infra/git',
    '협업': 'infra/git',
    '워크플로우': 'infra/git',
    '네이밍': 'infra/git',
    'devops': 'infra',

    'docker': 'infra/docker',
    'AWS': 'infra/aws',
    'cloud': 'infra/aws',
    'linux': 'infra/linux',
    'GithubActions': 'infra/cicd',
    'obsidian': 'infra/obsidian',
    '태그': 'infra/obsidian',

    # ── biz/ 비즈니스 & 경영 ─────────────────────────
    'CustomerSegmentation': 'biz/marketing',
    '고객세분화': 'biz/marketing',
    'CRM': 'biz/marketing',
    'CustomerBehavior': 'biz/marketing',
    'ConsumerBehavior': 'biz/marketing',
    '마케팅': 'biz/marketing',
    'MarketingStrategy': 'biz/marketing',
    'marketingdata': 'biz/marketing',
    '마케팅분석': 'biz/marketing',
    'MarketingAnalysis': 'biz/marketing',
    'MarketingAnalytics': 'biz/marketing',
    'Marketing': 'biz/marketing',
    'AARRR': 'biz/marketing',
    'STPAnalysis': 'biz/marketing',
    'STPStrategy': 'biz/marketing',
    'TargetMarketing': 'biz/marketing',
    'MarketSegmentation': 'biz/marketing',
    'TargetMarket': 'biz/marketing',
    'Positioning': 'biz/marketing',
    'Repositioning': 'biz/marketing',
    'MarketCoverage': 'biz/marketing',
    'UndifferentiatedMarketing': 'biz/marketing',
    'DifferentiatedMarketing': 'biz/marketing',
    'ConcentratedMarketing': 'biz/marketing',
    'Micromarketing': 'biz/marketing',
    'ProductLifeCycle': 'biz/marketing',
    'ProductClassification': 'biz/marketing',
    'ConsumerGoods': 'biz/marketing',
    'PricingStrategy': 'biz/marketing',
    'HighPricingStrategy': 'biz/marketing',
    'LowPricingStrategy': 'biz/marketing',
    'SkimmingPricing': 'biz/marketing',
    'PenetrationPricing': 'biz/marketing',
    'DistributionChannels': 'biz/marketing',
    'ConsumerDecisionProcess': 'biz/marketing',
    'MarketingInformationSystem': 'biz/marketing',
    'InboundMarketing': 'biz/marketing',
    'Upselling': 'biz/marketing',
    'CrossSelling': 'biz/marketing',
    'CustomerShare': 'biz/marketing',
    'MarketingMix': 'biz/marketing',
    '4P': 'biz/marketing',
    '4C': 'biz/marketing',
    'IMC': 'biz/marketing',
    'MassMedia': 'biz/marketing',
    'PrintMedia': 'biz/marketing',
    'Radio': 'biz/marketing',
    'Television': 'biz/marketing',
    'OutdoorAdvertising': 'biz/marketing',
    'Internet': 'biz/marketing',
    'CampaignManagement': 'biz/marketing',
    'PredictiveAnalytics': 'biz/marketing',
    'DeMarketing': 'biz/marketing',
    'DemandManagement': 'biz/marketing',
    'SocialResponsibility': 'biz/marketing',
    'EnvironmentalProtection': 'biz/marketing',
    'ResourceManagement': 'biz/marketing',
    'DecisionMaking': 'biz/marketing',
    'MultiAttributeDecisionMaking': 'biz/marketing',
    'CompensatoryModel': 'biz/marketing',
    'EvaluationModel': 'biz/marketing',
    '마케팅/세일즈': 'biz/marketing',
    '마케팅/브랜드': 'biz/marketing',
    '광고효과': 'biz/marketing',
    'AdvertisingEffect': 'biz/marketing',
    'A': None,  # broken tag from A/B테스팅
    '패션산업': 'biz/marketing',
    '타겟마케팅': 'biz/marketing',
    'purchasingbehavior': 'biz/marketing',
    'RFMAnalysis': 'biz/marketing',
    'LTV': 'biz/marketing',
    'CustomerLoyalty': 'biz/marketing',
    'RewardProgram': 'biz/marketing',
    'CustomerSatisfaction': 'biz/marketing',
    'CustomerPreferences': 'biz/marketing',
    'SWOTAnalysis': 'biz/strategy',
    'PESTAnalysis': 'biz/strategy',
    'PorterFiveForces': 'biz/strategy',
    'BCGMatrix': 'biz/strategy',
    'ValueChainAnalysis': 'biz/strategy',
    'BusinessStrategy': 'biz/strategy',
    '전략': 'biz/strategy',
    '경영': 'biz',

    'projectManagement': 'biz/pm',
    'project-management': 'biz/pm',
    'PM': 'biz/pm',
    'PMBOK': 'biz/pm',
    'PMP': 'biz/pm',
    'ProcessImprovement': 'biz/pm',
    'WorkflowVisualization': 'biz/pm',
    'VisioUsage': 'biz/pm',
    'Tags/Process': 'biz/pm',
    'Visio': 'biz/pm',
    'Microsoft': 'biz/pm',
    'Diagram': 'biz/pm',
    'documentManagement': 'biz/pm',
    'brainstorming': 'biz/pm',

    'HumanResources': 'biz/hr',
    'PerformanceEvaluation': 'biz/hr',
    'ManagementTechniques': 'biz/hr',
    'EmployeeAssessment': 'biz/hr',
    'OrganizationalDevelopment': 'biz/hr',
    'assessment': 'biz/hr',
    'PerformanceManagement': 'biz/hr',
    'MBO': 'biz/hr',
    'KPI': 'biz/hr',
    'CompetencyAssessment': 'biz/hr',
    'Incentives': 'biz/hr',
    'Motivation': 'biz/hr',
    'Monitoring': 'biz/hr',
    '360DegreeFeedback': 'biz/hr',
    'CallQuality': 'biz/hr',
    'SMARTGoals': 'biz/hr',
    'JobAnalysis': 'biz/hr',
    'JobDescription': 'biz/hr',
    'JobSpecification': 'biz/hr',
    'JobEvaluation': 'biz/hr',
    'Recruitment': 'biz/hr',
    'StructuredInterview': 'biz/hr',
    'UnstructuredInterview': 'biz/hr',
    'Training': 'biz/hr',
    'EmployeeBenefits': 'biz/hr',
    'CareerDevelopment': 'biz/hr',

    '정부지원사업': 'biz/startup',
    '창업준비': 'biz/startup',
    '사업계획서': 'biz/startup',
    '자금조달': 'biz/startup',

    # Telemarketing → biz/marketing
    'Telemarketing': 'biz/marketing',
    'Script': 'biz/marketing',
    'RolePlaying': 'biz/marketing',
    'MassCallHandling': 'biz/marketing',
    'InboundCallHandling': 'biz/marketing',
    'CallLoadForecasting': 'biz/marketing',
    'InnovativeOutboundTelemarketing': 'biz/marketing',
    'CustomerInformation': 'biz/marketing',
    'ACD': 'biz/marketing',
    'CTI': 'biz/marketing',
    'IVR': 'biz/marketing',
    'VOC': 'biz/marketing',
    'CustomerValue': 'biz/marketing',
    'PointProgram': 'biz/marketing',
    'VIPProgram': 'biz/marketing',
    '깨진유리창의법칙': 'biz/marketing',
    'CustomerTouchpoint': 'biz/marketing',
    'MOT': 'biz/marketing',
    'NonFaceToFaceCommunication': 'biz/marketing',
    'TelephoneCounseling': 'biz/marketing',
    'ChatCounseling': 'biz/marketing',
    'EmailCounseling': 'biz/marketing',
    'Rapport': 'biz/marketing',
    'ActiveListening': 'biz/marketing',
    'Maslow': 'biz/marketing',
    'OpenEndedQuestions': 'biz/marketing',
    'ClosedEndedQuestions': 'biz/marketing',
    'FABE': 'biz/marketing',
    'YesBut': 'biz/marketing',
    'Aronson': 'biz/marketing',
    'Laird': 'biz/marketing',
    'CustomerComplaint': 'biz/marketing',
    'ComplaintHandling': 'biz/marketing',
    'FairnessTheory': 'biz/marketing',
    'ConsumerBasicAct': 'biz/marketing',
    'CCMS': 'biz/marketing',
    'ProspectiveCustomer': 'biz/marketing',
    'NewCustomer': 'biz/marketing',
    'ExistingCustomer': 'biz/marketing',
    'KeyCustomer': 'biz/marketing',
    'ChurnedCustomer': 'biz/marketing',
    'ParetoAnalysis': 'biz/marketing',
    'CustomerService': 'biz/marketing',
    'TelephoneEtiquette': 'biz/marketing',
    'CustomerFeedback': 'biz/marketing',
    'HappyCall': 'biz/marketing',
    'ProductDevelopment': 'biz/marketing',
    'MarketResearch': 'biz/marketing',

    'CEO/비즈니스맨': 'biz',
    'CEO': 'biz',

    # ── career/ 커리어 ───────────────────────────────
    'resume': 'career/resume',
    'portfolio': 'career/portfolio',
    'engineer': 'career',

    # ── lang/ 언어 학습 ──────────────────────────────
    'english': 'lang/english',
    'englsih': 'lang/english',  # typo in vault
    '전화영어': 'lang/english',
    '전화영어후기': 'lang/english',
    'spicus': 'lang/english',
    'spicus후기': 'lang/english',

    # ── write/ 글쓰기 ────────────────────────────────
    'write': 'write',
    'daily': 'write/diary',
    'journal': 'write/diary',
    # write/essay, write/poem already in new format

    # ── finance/ 재무 ────────────────────────────────
    'insurance': 'finance/insurance',
    '주가분석': 'finance/invest',
    '금융데이터분석': 'finance/invest',
    '자산가격결정모델': 'finance/invest',
    '기술적분석': 'finance/invest',
    'StockAnalysis': 'finance/invest',
    'FinancialDataAnalysis': 'finance/invest',
    'AssetPricingModel': 'finance/invest',
    'TechnicalAnalysis': 'finance/invest',
    '포트폴리오분석': 'finance/invest',
    'PortfolioAnalysis': 'finance/invest',

    # ── life/ 생활 ───────────────────────────────────
    'TimeManagement': 'life/habit',
    'PersonalGrowth': 'life/habit',
    '자기계발': 'life/habit',
    'UI/UX': 'dev/web',
    'UI': 'dev/web',

    # ── 출처(src) 태그 ───────────────────────────────
    'Bootcamp': 'src/course',
    'BeyondSWCamp': 'src/course',
    'lesson': 'src/lecture',
    '학회발표': 'src/paper',
    '공공데이터': 'src/doc',
    'clippings': 'src/article',

    # ── 액션(action) 태그 ────────────────────────────
    'TODO': 'action/todo',
    'todo': 'action/todo',
    '톡도': 'action/todo',
    'issue': 'action/todo',
    'bug': 'action/todo',

    # ── 제거 (무의미하거나 다른 수단으로 표현) ────────
    'Notes': None,
    'notes': None,
    'Books': None,  # already handled
    'Tags': None,
    'LikeThis': None,
    '독서': None,

    # ── type property로 이동해야 하는 태그 ───────────
    # 스크립트에서 별도 처리
    'reference': '__type:reference',
    'process': '__type:reference',
    'output': '__type:output',
    'archive': '__status:archive',
    'project': '__type:project',

    # ── secondBrain 관련 ─────────────────────────────
    'secondBrain': 'infra/obsidian',
    'secondBrainArchitecture': 'infra/obsidian',
    'rhizome': 'biz/pm',
    'rhizomaticProject': 'biz/pm',

    # ── 기타 (package structure 등) ──────────────────
    'project-structure': 'dev/java',
    'maven-projects': 'dev/java',
    'gradle-projects': 'dev/java',
    'package-structure': 'dev/java',
    'java-libraries': 'dev/java',
    'automation': 'dev/python',
    '중고거래': 'biz',
    '게시판': 'dev/web',
    '유스케이스다이어그램': 'dev/oop',
    '온라인플랫폼': 'dev/web',

    # ── 미매핑 보완 (대소문자 변형, 공백 포함) ───────
    'git': 'infra/git',
    'DATABASE': 'dev/db',
    'Database': 'dev/db',
    'bootcamp': 'src/course',
    'inheritance': 'dev/java',
    'polymorphism': 'dev/java',
    'Pandas': 'data/preprocessing',
    'Programming': 'dev',
    'Syntax': 'dev',
    'eda': 'data/analysis',
    'Object-Oriented Design': 'dev/oop',
    'Object-Oriented-Programming': 'dev/oop',
    'GitHub Flow': 'infra/git',
    'Dependency Injection': 'dev/oop',
    'Unit Testing': 'dev/test',
    'Use Case Diagram': 'dev/oop',
    'Online Platform': 'dev/web',
    'confidence interval': 'data/stats',
    'hypothesis testing': 'data/stats',
    'machine learning': 'data/ml',
    'probability distribution': 'data/stats',
    'random variable': 'data/stats',
    'measures of central tendency': 'data/stats',
    'fraud detection': 'data/analysis',
    '손자병법': 'biz/strategy',
    '36계': 'biz/strategy',
    '주역': 'biz/strategy',
    'korail': None,  # specific topic, remove
    'tourism': None,
    'reviews': None,
    'HMM(은닉마르코프모형)': 'data/ml',

    # More variations found in vault
    'accessmodifier': 'dev/java',
    'package': 'dev/java',
    'class': 'dev/java',
    'accesslevel': 'dev/java',
    'OOP': 'dev/oop',
    'object': 'dev/java',
    'encapsulation': 'dev/java',
    'getter': 'dev/java',
    'setter': 'dev/java',
    'privatefield': 'dev/java',
    '상속': 'dev/java',
    '다형성': 'dev/java',
    '추상클래스': 'dev/java',
    '인터페이스': 'dev/java',
    '자바프로그래밍': 'dev/java',
    '메서드재정의': 'dev/java',
    '자동타입변환': 'dev/java',
    '강제타입변환': 'dev/java',
    'Objects': 'dev/java',
    'Classes': 'dev/java',
    'Constructors': 'dev/java',
    'HeapMemory': 'dev/java',
    'StackMemory': 'dev/java',
    'ObjectInstantiation': 'dev/java',
    'HashMap': 'dev/java',
    'dict': 'dev/python',
    'Key-Value-Store': 'dev',
    'Data-Structures': 'dev',
    'Comparison': 'dev',
    'EventAnalysis': 'data/analysis',
    'Dashboarding': 'data/viz',
    'DataExploration': 'data/analysis',
    'SqlFunctions': 'dev/sql',
    'StoredProcedures': 'dev/sql',
    'SqlLimitations': 'dev/sql',
    'AggregationFunctions': 'dev/sql',
    'DynamicSql': 'dev/sql',
    'ProcedureDesign': 'dev/sql',
    'DatabaseDevelopment': 'dev/sql',
    'SqlFundamentals': 'dev/sql',
    'LeapSeconds': None,
    'TimekeepingFailures': None,
    'SoftwareBugs': None,
    'FinancialDisruptions': None,
    'DNSOutages': None,
    'GPSNavigationErrors': None,
    'TimeSmearing': None,
    'LeapSecondReform': None,
    'TimekeepingStandards': None,

    # Monthly review tags
    '1월회고': None,
    '학습': None,
    '생활정비': None,
    '운동': 'life/health',
    '금주': 'life/health',
    '술': None,
    'english spicus 전화영어': 'lang/english',  # malformed compound entry
}


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None, content
    return match.group(1), content[match.end():]


def split_compound_tag(tag_str):
    """Split a malformed compound tag like 'Java #OOP #Classes' into individual tags."""
    tag_str = tag_str.strip()
    if '#' in tag_str and ' ' in tag_str:
        # Split by # and clean up
        parts = re.split(r'\s*#', tag_str)
        return [p.strip() for p in parts if p.strip()]
    return [tag_str]


def extract_tags(fm_text):
    """Extract tags from frontmatter text. Handles both formats."""
    tags = []
    fmt = None

    # Format 1: tags: (YAML array)
    m = re.search(r'^tags:\s*$', fm_text, re.MULTILINE)
    if m:
        fmt = 'yaml_array'
        for item in re.finditer(r'^\s+-\s+(.+)$', fm_text[m.end():], re.MULTILINE):
            val = item.group(1).strip().strip('"').strip("'")
            # Stop if we hit another property
            line_start = fm_text[m.end():][: item.start()]
            if re.search(r'^\S', line_start, re.MULTILINE):
                break
            # Handle compound tags like "Java #OOP #Classes"
            for t in split_compound_tag(val):
                tags.append(t)
        return tags, fmt

    # Format 1b: tags: [inline array]
    m = re.search(r'^tags:\s*\[([^\]]*)\]', fm_text, re.MULTILINE)
    if m:
        fmt = 'inline_array'
        for t in m.group(1).split(','):
            t = t.strip().strip('"').strip("'")
            if t:
                tags.append(t)
        return tags, fmt

    # Format 2: tag: value1 value2 (space-separated)
    m = re.search(r'^tag:\s+(.+)$', fm_text, re.MULTILINE)
    if m:
        fmt = 'space_separated'
        for t in m.group(1).split():
            t = t.strip().strip('"').strip("'")
            if t:
                tags.append(t)
        return tags, fmt

    # Format 3: tags: single_value or space-separated on same line
    m = re.search(r'^tags:\s+(\S.+)$', fm_text, re.MULTILINE)
    if m:
        val = m.group(1).strip()
        if not val.startswith('[') and not val.startswith('-'):
            fmt = 'single_value'
            # Could be space-separated or #-separated
            for t in split_compound_tag(val):
                for sub in t.split():
                    sub = sub.strip().strip('"').strip("'").lstrip('#')
                    if sub:
                        tags.append(sub)
            return tags, fmt

    return tags, fmt


def map_tags(old_tags):
    """Map old tags to new MECE tags. Returns (new_tags, type_changes, removed, unmapped)."""
    new_tags = []
    type_changes = {}  # property changes like type or status
    removed = []
    unmapped = []

    for tag in old_tags:
        clean = tag.lstrip('#').strip()
        if not clean:
            continue

        # Already in MECE format?
        if '/' in clean:
            parts = clean.split('/')
            valid_prefixes = {
                'dev', 'data', 'ai', 'infra', 'biz', 'career',
                'lang', 'write', 'finance', 'life', 'src', 'action',
            }
            if parts[0] in valid_prefixes:
                new_tags.append(clean)
                continue

        if clean in TAG_MAP:
            mapped = TAG_MAP[clean]
            if mapped is None:
                removed.append(clean)
            elif isinstance(mapped, str) and mapped.startswith('__'):
                # Property change
                prop, val = mapped[2:].split(':')
                type_changes[prop] = val
                removed.append(clean)
            elif isinstance(mapped, tuple):
                new_tags.extend(mapped)
            else:
                new_tags.append(mapped)
        else:
            unmapped.append(clean)

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for t in new_tags:
        if t not in seen:
            seen.add(t)
            deduped.append(t)

    return deduped, type_changes, removed, unmapped


def rebuild_frontmatter(fm_text, old_tags, new_tags, fmt, type_changes):
    """Rebuild frontmatter with new tags."""
    result = fm_text

    if fmt == 'yaml_array':
        # Remove old tags block
        pattern = r'^tags:\s*\n(?:\s+-\s+.+\n)*'
        result = re.sub(pattern, '', result, flags=re.MULTILINE)
        # Build new tags block
        if new_tags:
            tags_block = 'tags:\n' + ''.join(f'  - {t}\n' for t in new_tags)
        else:
            tags_block = 'tags: []\n'
        result = result.rstrip('\n') + '\n' + tags_block

    elif fmt == 'inline_array':
        pattern = r'^tags:\s*\[([^\]]*)\]'
        if new_tags:
            tags_str = 'tags:\n' + ''.join(f'  - {t}\n' for t in new_tags)
        else:
            tags_str = 'tags: []'
        result = re.sub(pattern, tags_str, result, flags=re.MULTILINE)

    elif fmt == 'space_separated':
        # Convert tag: -> tags: YAML array
        pattern = r'^tag:\s+.+$'
        if new_tags:
            tags_str = 'tags:\n' + ''.join(f'  - {t}\n' for t in new_tags)
        else:
            tags_str = 'tags: []'
        result = re.sub(pattern, tags_str, result, flags=re.MULTILINE)

    elif fmt == 'single_value':
        pattern = r'^tags:\s+\S.+$'
        if new_tags:
            tags_str = 'tags:\n' + ''.join(f'  - {t}\n' for t in new_tags)
        else:
            tags_str = 'tags: []'
        result = re.sub(pattern, tags_str, result, flags=re.MULTILINE)

    # Add type/status properties if needed
    for prop, val in type_changes.items():
        if not re.search(rf'^{prop}:', result, re.MULTILINE):
            result = result.rstrip('\n') + f'\n{prop}: {val}\n'

    return result


def process_file(fpath, dry_run=True):
    """Process a single file. Returns change info or None."""
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    fm_text, body = parse_frontmatter(content)
    if fm_text is None:
        return None

    old_tags, fmt = extract_tags(fm_text)
    if not old_tags:
        return None

    new_tags, type_changes, removed, unmapped = map_tags(old_tags)

    # Check if anything changed
    if old_tags == new_tags and not removed and not type_changes:
        return None

    if not dry_run:
        new_fm = rebuild_frontmatter(fm_text, old_tags, new_tags, fmt, type_changes)
        new_content = f'---\n{new_fm.strip()}\n---{body}'
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return {
        'file': fpath,
        'old_tags': old_tags,
        'new_tags': new_tags,
        'removed': removed,
        'unmapped': unmapped,
        'type_changes': type_changes,
        'fmt': fmt,
    }


def main():
    dry_run = '--apply' not in sys.argv
    mode = 'DRY RUN' if dry_run else 'APPLYING'
    print(f'=== MECE Tag Migration ({mode}) ===\n')

    changes = []
    errors = []
    total_files = 0

    for root, dirs, files in os.walk(VAULT_ROOT):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for fname in files:
            if not fname.endswith('.md'):
                continue
            total_files += 1
            fpath = os.path.join(root, fname)
            try:
                result = process_file(fpath, dry_run=dry_run)
                if result:
                    changes.append(result)
            except Exception as e:
                errors.append((fpath, str(e)))

    # Print results
    all_unmapped = set()
    for c in changes:
        rel = os.path.relpath(c['file'], VAULT_ROOT)
        print(f'[F] {rel}')
        print(f'   OLD: {c["old_tags"]}')
        print(f'   NEW: {c["new_tags"]}')
        if c['removed']:
            print(f'   DEL: {c["removed"]}')
        if c['type_changes']:
            print(f'   PROP: {c["type_changes"]}')
        if c['unmapped']:
            print(f'   ???: {c["unmapped"]}')
            all_unmapped.update(c['unmapped'])
        print()

    print(f'--- Summary ---')
    print(f'Total files scanned: {total_files}')
    print(f'Files to change: {len(changes)}')
    if errors:
        print(f'Errors: {len(errors)}')
        for f, e in errors:
            print(f'  {f}: {e}')
    if all_unmapped:
        print(f'\nUnmapped tags ({len(all_unmapped)}):')
        for t in sorted(all_unmapped):
            print(f'  - {t}')

    if dry_run:
        print(f'\nRun with --apply to execute changes.')


if __name__ == '__main__':
    main()

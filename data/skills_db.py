"""Skills knowledge base used for skill extraction, gap analysis, and
auto-categorization. Skills are normalized to lowercase for matching.
"""

SKILLS = {
    "programming_languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C", "C++", "C#",
        "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala", "R",
        "MATLAB", "Perl", "Bash", "Shell", "SQL", "HTML", "CSS",
        "Objective-C", "Dart", "Lua", "Haskell", "Clojure", "Elixir",
    ],
    "frameworks_libraries": [
        "React", "Next.js", "Vue", "Vue.js", "Angular", "Svelte", "Nuxt.js",
        "Node.js", "Express", "Express.js", "FastAPI", "Flask", "Django",
        "Spring", "Spring Boot", "Laravel", "Ruby on Rails", "ASP.NET",
        ".NET Core", "Gin", "Actix", "TensorFlow", "PyTorch", "Keras",
        "scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn",
        "Hugging Face", "LangChain", "LlamaIndex", "OpenCV", "spaCy",
        "NLTK", "jQuery", "Tailwind CSS", "Bootstrap", "Material UI",
        "Redux", "MobX", "Zustand", "RxJS", "Three.js", "D3.js",
    ],
    "databases": [
        "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Cassandra",
        "DynamoDB", "Firebase", "Firestore", "Elasticsearch", "Neo4j",
        "BigQuery", "Snowflake", "Redshift", "Oracle", "MariaDB",
        "InfluxDB", "Couchbase", "ClickHouse", "Supabase", "Pinecone",
        "Weaviate", "Chroma", "Milvus",
    ],
    "cloud_devops": [
        "AWS", "GCP", "Google Cloud", "Azure", "Heroku", "DigitalOcean",
        "Vercel", "Netlify", "Cloudflare", "Docker", "Kubernetes", "Helm",
        "Terraform", "Ansible", "Pulumi", "CloudFormation", "Jenkins",
        "GitHub Actions", "GitLab CI", "CircleCI", "Travis CI", "ArgoCD",
        "Prometheus", "Grafana", "Datadog", "New Relic", "Splunk",
        "ELK Stack", "Linux", "Nginx", "Apache", "Lambda", "EC2", "S3",
        "RDS", "ECS", "EKS", "GKE", "AKS", "Cloud Run", "Cloud Functions",
    ],
    "data_ml": [
        "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing",
        "Computer Vision", "Reinforcement Learning", "MLOps", "Data Engineering",
        "Data Analysis", "Data Visualization", "Statistics", "A/B Testing",
        "ETL", "ELT", "Apache Spark", "Hadoop", "Kafka", "Airflow", "dbt",
        "Databricks", "Snowflake", "Tableau", "Power BI", "Looker", "Mode",
        "Feature Engineering", "Model Deployment", "LLM", "RAG", "Prompt Engineering",
        "Fine-tuning", "Vector Databases", "Transformers", "BERT", "GPT",
    ],
    "tools": [
        "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Confluence",
        "Notion", "Slack", "Trello", "Asana", "Linear", "Figma", "Sketch",
        "Postman", "Insomnia", "VS Code", "IntelliJ", "PyCharm", "Vim",
        "Emacs", "Xcode", "Android Studio", "Webpack", "Vite", "Rollup",
        "ESLint", "Prettier", "Pytest", "Jest", "Mocha", "Cypress", "Selenium",
        "Playwright", "Storybook",
    ],
    "soft_skills": [
        "Leadership", "Communication", "Teamwork", "Problem Solving",
        "Critical Thinking", "Creativity", "Adaptability", "Time Management",
        "Collaboration", "Mentorship", "Public Speaking", "Negotiation",
        "Conflict Resolution", "Strategic Thinking", "Decision Making",
        "Emotional Intelligence", "Project Management", "Stakeholder Management",
        "Cross-functional Leadership", "Agile", "Scrum", "Kanban", "OKRs",
    ],
    "domain": [
        "FinTech", "HealthTech", "EdTech", "E-commerce", "SaaS", "B2B",
        "B2C", "Marketplace", "Cybersecurity", "Blockchain", "Web3",
        "IoT", "AR", "VR", "Robotics", "Gaming", "Ad Tech", "Mar Tech",
        "Real Estate", "Logistics", "Supply Chain", "Banking", "Insurance",
        "Compliance", "GDPR", "HIPAA", "SOC 2", "PCI DSS",
    ],
}


def all_skills() -> list[str]:
    """Flat, deduplicated, lowercase list of every known skill."""
    seen = set()
    out = []
    for bucket in SKILLS.values():
        for s in bucket:
            key = s.lower()
            if key not in seen:
                seen.add(key)
                out.append(s)
    return out


def categorize(skill: str) -> str:
    """Return the bucket name for a skill, or 'other'."""
    target = skill.lower().strip()
    for bucket, items in SKILLS.items():
        if any(target == s.lower() for s in items):
            return bucket
    return "other"


def extract_skills(text: str) -> list[str]:
    """Return every known skill mentioned in `text` (case-insensitive)."""
    if not text:
        return []
    lowered = text.lower()
    found = []
    seen = set()
    for skill in all_skills():
        s = skill.lower()
        # Word-boundary check for short skills (e.g. "R", "Go") to avoid false positives
        if len(s) <= 2:
            tokens = lowered.replace(",", " ").replace(".", " ").split()
            if s in tokens and skill not in seen:
                found.append(skill)
                seen.add(skill)
        else:
            if s in lowered and skill not in seen:
                found.append(skill)
                seen.add(skill)
    return found

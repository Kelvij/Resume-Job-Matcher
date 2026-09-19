from .jd_parser import parse_jd
from .resume_parser import parse_resume
from .report import build_report

DEMO_RESUME = """Aarav Sharma\nB.Tech Computer Science\n\nSkills\nC++, Python, SQL, Data Structures, Algorithms, JavaScript, React, FastAPI, PostgreSQL, Git, REST APIs\n\nProjects\nSmart Shopping Assistant: Built a product research assistant using React, FastAPI, PostgreSQL and third-party APIs. Added filtering and recommendation workflows.\nRepoLens: Developed a repository analysis tool in Python and FastAPI that summarizes code metadata and exposes REST APIs.\n\nExperience\nSoftware Engineering Intern — 1 year. Built backend features, wrote SQL queries, collaborated with a five-person engineering team.\n\nEducation\nB.Tech in Computer Science and Engineering\n\nAchievements\nSolved 400+ DSA problems and led a college technical project team.\n"""

DEMO_JD = """Software Engineer — Developer Platform at Nova Systems\n\nRequired qualifications: 1+ years of software engineering experience; strong C++ and Python; data structures and algorithms; REST APIs; SQL; Git; object-oriented programming.\n\nPreferred: Docker, AWS, Kubernetes, React, Machine Learning.\n\nEducation: Bachelor's degree in Computer Science, Engineering, or a related field.\n\nSoft skills: communication, collaboration, ownership.\n\nThe role focuses on building cloud tooling and developer-facing backend services.\n"""


def demo_report(model_name: str, weights: dict[str, float]) -> dict:
    return build_report(parse_resume(DEMO_RESUME), parse_jd(DEMO_JD), model_name, weights)

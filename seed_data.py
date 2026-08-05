# seed_data.py
"""
Seed data script for Student Guidance System.
Run with PowerShell: python -c "exec(open('seed_data.py').read())"
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_guidance_system.settings')  # <-- CHANGE TO YOUR PROJECT NAME
django.setup()

from django.db import transaction
from skill.models import Skill
from career.models import Career, CareerSkill, CareerPath
from course.models import Course, CourseCategory
from assessment.models import Assessment, AssessmentSkill
from authentication.models import User


@transaction.atomic
def seed_data():
    print("Creating seed data...")

    # =============================================================================
    # 1. SKILLS
    # =============================================================================
    print("\n[1/8] Creating Skills...")

    skills_data = [
        {"name": "Python Programming", "description": "Proficiency in Python including syntax, data structures, OOP, and standard libraries."},
        {"name": "JavaScript", "description": "Proficiency in JavaScript including ES6+, DOM manipulation, and async programming."},
        {"name": "SQL", "description": "Ability to write complex SQL queries, design databases, and optimize performance."},
        {"name": "Problem Solving", "description": "Analytical thinking, algorithmic design, and debugging capabilities."},
        {"name": "Communication", "description": "Clear written and verbal communication, active listening, and presentation skills."},
        {"name": "Teamwork", "description": "Collaboration, conflict resolution, and ability to work effectively in teams."},
        {"name": "Leadership", "description": "Team management, decision making, mentoring, and strategic thinking."},
        {"name": "Data Analysis", "description": "Data cleaning, statistical analysis, visualization, and insight generation."},
        {"name": "Java Programming", "description": "Proficiency in Java including OOP, collections, and enterprise frameworks."},
        {"name": "React.js", "description": "Building UI components, hooks, state management, and frontend architecture."},
        {"name": "Django", "description": "Web development with Django including ORM, views, templates, and REST APIs."},
        {"name": "Machine Learning", "description": "ML algorithms, model training, evaluation, and deployment."},
        {"name": "Project Management", "description": "Agile methodology, sprint planning, risk management, and stakeholder communication."},
        {"name": "Critical Thinking", "description": "Logical reasoning, evaluating arguments, and making informed decisions."},
    ]

    created_skills = {}
    for data in skills_data:
        obj, created = Skill.objects.get_or_create(
            name=data["name"],
            defaults={"description": data["description"]}
        )
        created_skills[data["name"]] = obj
        status = "Created" if created else "Exists"
        print(f"  [{status}] Skill: {obj.name} (ID: {obj.id})")

    # Build dynamic ID map so questions always point to correct skills
    skill_id_map = {name: obj.id for name, obj in created_skills.items()}
    print(f"  Skill ID Map: {skill_id_map}")

    # =============================================================================
    # 2. COURSE CATEGORIES
    # =============================================================================
    print("\n[2/8] Creating Course Categories...")

    categories_data = [
        {"title": "Programming", "description": "Programming languages and development"},
        {"title": "Database", "description": "Database design and management"},
        {"title": "Web Development", "description": "Frontend and backend web technologies"},
        {"title": "Data Science", "description": "Data analysis and machine learning"},
        {"title": "Soft Skills", "description": "Communication, leadership, and teamwork"},
        {"title": "Project Management", "description": "Project planning and execution"},
    ]

    created_categories = {}
    for data in categories_data:
        obj, created = CourseCategory.objects.get_or_create(
            title=data["title"],
            defaults={"description": data["description"]}
        )
        created_categories[data["title"]] = obj
        status = "Created" if created else "Exists"
        print(f"  [{status}] Category: {obj.title}")

    # =============================================================================
    # 3. COURSES
    # =============================================================================
    print("\n[3/8] Creating Courses...")

    courses_data = [
        {
            "title": "Python Fundamentals",
            "prefix": "PY",
            "description": "Learn Python basics, data structures, and OOP concepts",
            "categories": ["Programming"],
            "level": "beginner",
            "price": 99.99,
            "is_active": True,
            "duration": "4 weeks",
        },
        {
            "title": "Advanced Python",
            "prefix": "APY",
            "description": "Advanced Python concepts, decorators, generators, and design patterns",
            "categories": ["Programming"],
            "level": "intermediate",
            "price": 149.99,
            "is_active": True,
            "duration": "6 weeks",
        },
        {
            "title": "JavaScript Essentials",
            "prefix": "JS",
            "description": "Core JavaScript, ES6, DOM manipulation, and async programming",
            "categories": ["Programming", "Web Development"],
            "level": "beginner",
            "price": 99.99,
            "is_active": True,
            "duration": "3 weeks",
        },
        {
            "title": "React.js Mastery",
            "prefix": "RJ",
            "description": "Build modern web applications with React, hooks, and state management",
            "categories": ["Programming", "Web Development"],
            "level": "intermediate",
            "price": 199.99,
            "is_active": True,
            "duration": "5 weeks",
        },
        {
            "title": "SQL for Data",
            "prefix": "SQL",
            "description": "Master SQL queries, joins, aggregations, and database design",
            "categories": ["Database"],
            "level": "beginner",
            "price": 79.99,
            "is_active": True,
            "duration": "4 weeks",
        },
        {
            "title": "Advanced SQL",
            "prefix": "ASQ",
            "description": "Advanced SQL optimization, stored procedures, and performance tuning",
            "categories": ["Database"],
            "level": "advanced",
            "price": 129.99,
            "is_active": True,
            "duration": "4 weeks",
        },
        {
            "title": "Django Full Stack",
            "prefix": "DJ",
            "description": "Build full-stack web applications with Django and Django REST Framework",
            "categories": ["Programming", "Web Development"],
            "level": "intermediate",
            "price": 249.99,
            "is_active": True,
            "duration": "8 weeks",
        },
        {
            "title": "Java Programming",
            "prefix": "JV",
            "description": "Learn Java from basics to enterprise applications",
            "categories": ["Programming"],
            "level": "beginner",
            "price": 129.99,
            "is_active": True,
            "duration": "6 weeks",
        },
        {
            "title": "Data Analysis with Python",
            "prefix": "DA",
            "description": "Data cleaning, analysis, and visualization using Pandas, NumPy, and Matplotlib",
            "categories": ["Programming", "Data Science"],
            "level": "intermediate",
            "price": 179.99,
            "is_active": True,
            "duration": "5 weeks",
        },
        {
            "title": "Machine Learning Basics",
            "prefix": "ML",
            "description": "Introduction to ML algorithms, scikit-learn, and model evaluation",
            "categories": ["Data Science"],
            "level": "intermediate",
            "price": 199.99,
            "is_active": True,
            "duration": "7 weeks",
        },
        {
            "title": "Effective Communication",
            "prefix": "COM",
            "description": "Master communication skills, presentations, and professional writing",
            "categories": ["Soft Skills"],
            "level": "beginner",
            "price": 69.99,
            "is_active": True,
            "duration": "2 weeks",
        },
        {
            "title": "Leadership Development",
            "prefix": "LD",
            "description": "Develop leadership skills, team management, and strategic thinking",
            "categories": ["Soft Skills", "Project Management"],
            "level": "intermediate",
            "price": 149.99,
            "is_active": True,
            "duration": "4 weeks",
        },
        {
            "title": "Project Management Pro",
            "prefix": "PM",
            "description": "Agile, Scrum, risk management, and stakeholder communication",
            "categories": ["Project Management"],
            "level": "intermediate",
            "price": 229.99,
            "is_active": True,
            "duration": "5 weeks",
        },
        {
            "title": "Team Collaboration",
            "prefix": "TC",
            "description": "Build effective teams, resolve conflicts, and achieve collective goals",
            "categories": ["Soft Skills"],
            "level": "beginner",
            "price": 79.99,
            "is_active": True,
            "duration": "2 weeks",
        },
        {
            "title": "Critical Thinking Mastery",
            "prefix": "CT",
            "description": "Develop logical reasoning, analytical thinking, and decision-making skills",
            "categories": ["Soft Skills"],
            "level": "beginner",
            "price": 89.99,
            "is_active": True,
            "duration": "3 weeks",
        },
    ]

    created_courses = {}
    for data in courses_data:
        category_titles = data.pop("categories")
        obj, created = Course.objects.get_or_create(
            title=data["title"],
            defaults=data
        )
        if created:
            for cat_title in category_titles:
                obj.categories.add(created_categories[cat_title])
        created_courses[data["title"]] = obj
        status = "Created" if created else "Exists"
        print(f"  [{status}] Course: {obj.title}")

    # =============================================================================
    # 4. CAREERS
    # =============================================================================
    print("\n[4/8] Creating Careers...")

    careers_data = [
        {
            "title": "Software Developer",
            "description": "Design, develop, and maintain software applications. Write clean, efficient code and collaborate with cross-functional teams.",
            "average_salary": 85000.00,
            "industry": "Technology",
        },
        {
            "title": "Data Analyst",
            "description": "Analyze complex data, create reports, and provide actionable insights to support business decision-making.",
            "average_salary": 75000.00,
            "industry": "Technology",
        },
        {
            "title": "Project Manager",
            "description": "Lead and oversee projects from initiation to completion. Manage teams, timelines, budgets, and stakeholder expectations.",
            "average_salary": 95000.00,
            "industry": "Management",
        },
        {
            "title": "Web Developer",
            "description": "Build and maintain websites and web applications. Work with both frontend and backend technologies.",
            "average_salary": 80000.00,
            "industry": "Technology",
        },
        {
            "title": "DevOps Engineer",
            "description": "Manage CI/CD pipelines, cloud infrastructure, containerization, and automate deployment processes.",
            "average_salary": 100000.00,
            "industry": "Technology",
        },
        {
            "title": "Data Scientist",
            "description": "Apply machine learning algorithms, analyze complex datasets, and build predictive models to solve business problems.",
            "average_salary": 110000.00,
            "industry": "Data Science",
        },
        {
            "title": "Business Analyst",
            "description": "Bridge between business needs and technical solutions. Gather requirements, analyze processes, and recommend improvements.",
            "average_salary": 78000.00,
            "industry": "Business",
        },
    ]

    created_careers = {}
    for data in careers_data:
        obj, created = Career.objects.get_or_create(
            title=data["title"],
            defaults={
                "description": data["description"],
                "average_salary": data["average_salary"],
                "industry": data["industry"],
            }
        )
        created_careers[data["title"]] = obj
        status = "Created" if created else "Exists"
        print(f"  [{status}] Career: {obj.title}")

    # =============================================================================
    # 5. CAREER SKILLS
    # =============================================================================
    print("\n[5/8] Creating Career Skills...")

    career_skills_data = [
        # Software Developer
        {"career": "Software Developer", "skill": "Python Programming", "minimum_score": 70, "weightage": 25},
        {"career": "Software Developer", "skill": "SQL", "minimum_score": 60, "weightage": 20},
        {"career": "Software Developer", "skill": "Problem Solving", "minimum_score": 70, "weightage": 20},
        {"career": "Software Developer", "skill": "Communication", "minimum_score": 65, "weightage": 15},
        {"career": "Software Developer", "skill": "Teamwork", "minimum_score": 60, "weightage": 10},
        {"career": "Software Developer", "skill": "Critical Thinking", "minimum_score": 60, "weightage": 10},

        # Data Analyst
        {"career": "Data Analyst", "skill": "SQL", "minimum_score": 70, "weightage": 30},
        {"career": "Data Analyst", "skill": "Problem Solving", "minimum_score": 65, "weightage": 20},
        {"career": "Data Analyst", "skill": "Communication", "minimum_score": 60, "weightage": 15},
        {"career": "Data Analyst", "skill": "Data Analysis", "minimum_score": 70, "weightage": 25},
        {"career": "Data Analyst", "skill": "Critical Thinking", "minimum_score": 60, "weightage": 10},

        # Project Manager
        {"career": "Project Manager", "skill": "Communication", "minimum_score": 75, "weightage": 30},
        {"career": "Project Manager", "skill": "Teamwork", "minimum_score": 70, "weightage": 20},
        {"career": "Project Manager", "skill": "Leadership", "minimum_score": 70, "weightage": 25},
        {"career": "Project Manager", "skill": "Project Management", "minimum_score": 70, "weightage": 15},
        {"career": "Project Manager", "skill": "Critical Thinking", "minimum_score": 65, "weightage": 10},

        # Web Developer
        {"career": "Web Developer", "skill": "Python Programming", "minimum_score": 60, "weightage": 15},
        {"career": "Web Developer", "skill": "JavaScript", "minimum_score": 70, "weightage": 20},
        {"career": "Web Developer", "skill": "SQL", "minimum_score": 50, "weightage": 10},
        {"career": "Web Developer", "skill": "React.js", "minimum_score": 70, "weightage": 25},
        {"career": "Web Developer", "skill": "Django", "minimum_score": 65, "weightage": 20},
        {"career": "Web Developer", "skill": "Communication", "minimum_score": 60, "weightage": 10},

        # DevOps Engineer
        {"career": "DevOps Engineer", "skill": "Python Programming", "minimum_score": 70, "weightage": 25},
        {"career": "DevOps Engineer", "skill": "SQL", "minimum_score": 60, "weightage": 20},
        {"career": "DevOps Engineer", "skill": "Problem Solving", "minimum_score": 70, "weightage": 20},
        {"career": "DevOps Engineer", "skill": "Communication", "minimum_score": 65, "weightage": 15},
        {"career": "DevOps Engineer", "skill": "Teamwork", "minimum_score": 60, "weightage": 10},
        {"career": "DevOps Engineer", "skill": "Critical Thinking", "minimum_score": 60, "weightage": 10},

        # Data Scientist
        {"career": "Data Scientist", "skill": "Python Programming", "minimum_score": 65, "weightage": 15},
        {"career": "Data Scientist", "skill": "SQL", "minimum_score": 60, "weightage": 15},
        {"career": "Data Scientist", "skill": "Problem Solving", "minimum_score": 75, "weightage": 20},
        {"career": "Data Scientist", "skill": "Data Analysis", "minimum_score": 70, "weightage": 15},
        {"career": "Data Scientist", "skill": "Machine Learning", "minimum_score": 70, "weightage": 20},
        {"career": "Data Scientist", "skill": "Critical Thinking", "minimum_score": 70, "weightage": 15},

        # Business Analyst
        {"career": "Business Analyst", "skill": "Problem Solving", "minimum_score": 70, "weightage": 25},
        {"career": "Business Analyst", "skill": "Communication", "minimum_score": 70, "weightage": 25},
        {"career": "Business Analyst", "skill": "Data Analysis", "minimum_score": 60, "weightage": 15},
        {"career": "Business Analyst", "skill": "Project Management", "minimum_score": 65, "weightage": 20},
        {"career": "Business Analyst", "skill": "Critical Thinking", "minimum_score": 65, "weightage": 15},
    ]

    for data in career_skills_data:
        career = created_careers[data["career"]]
        skill = created_skills[data["skill"]]
        obj, created = CareerSkill.objects.get_or_create(
            career=career,
            skill=skill,
            defaults={
                "minimum_score": data["minimum_score"],
                "weightage": data["weightage"],
            }
        )
        status = "Created" if created else "Exists"
        print(f"  [{status}] CareerSkill: {career.title} -> {skill.name}")

    # =============================================================================
    # 6. CAREER PATHS
    # =============================================================================
    print("\n[6/8] Creating Career Paths...")

    career_paths_data = [
        # Software Developer
        {"career": "Software Developer", "course": "Python Fundamentals", "sequence": 1},
        {"career": "Software Developer", "course": "JavaScript Essentials", "sequence": 2},
        {"career": "Software Developer", "course": "SQL for Data", "sequence": 3},
        {"career": "Software Developer", "course": "Advanced Python", "sequence": 4},
        {"career": "Software Developer", "course": "Django Full Stack", "sequence": 5},

        # Data Analyst
        {"career": "Data Analyst", "course": "SQL for Data", "sequence": 1},
        {"career": "Data Analyst", "course": "Python Fundamentals", "sequence": 2},
        {"career": "Data Analyst", "course": "Data Analysis with Python", "sequence": 3},
        {"career": "Data Analyst", "course": "Advanced SQL", "sequence": 4},

        # Project Manager
        {"career": "Project Manager", "course": "Effective Communication", "sequence": 1},
        {"career": "Project Manager", "course": "Leadership Development", "sequence": 2},
        {"career": "Project Manager", "course": "Team Collaboration", "sequence": 3},
        {"career": "Project Manager", "course": "Project Management Pro", "sequence": 4},

        # Web Developer
        {"career": "Web Developer", "course": "JavaScript Essentials", "sequence": 1},
        {"career": "Web Developer", "course": "Python Fundamentals", "sequence": 2},
        {"career": "Web Developer", "course": "React.js Mastery", "sequence": 3},
        {"career": "Web Developer", "course": "Django Full Stack", "sequence": 4},
        {"career": "Web Developer", "course": "SQL for Data", "sequence": 5},

        # DevOps Engineer
        {"career": "DevOps Engineer", "course": "Python Fundamentals", "sequence": 1},
        {"career": "DevOps Engineer", "course": "SQL for Data", "sequence": 2},
        {"career": "DevOps Engineer", "course": "Django Full Stack", "sequence": 3},
        {"career": "DevOps Engineer", "course": "Advanced Python", "sequence": 4},

        # Data Scientist
        {"career": "Data Scientist", "course": "Python Fundamentals", "sequence": 1},
        {"career": "Data Scientist", "course": "SQL for Data", "sequence": 2},
        {"career": "Data Scientist", "course": "Data Analysis with Python", "sequence": 3},
        {"career": "Data Scientist", "course": "Machine Learning Basics", "sequence": 4},
        {"career": "Data Scientist", "course": "Advanced Python", "sequence": 5},

        # Business Analyst
        {"career": "Business Analyst", "course": "Effective Communication", "sequence": 1},
        {"career": "Business Analyst", "course": "Critical Thinking Mastery", "sequence": 2},
        {"career": "Business Analyst", "course": "Data Analysis with Python", "sequence": 3},
        {"career": "Business Analyst", "course": "Project Management Pro", "sequence": 4},
    ]

    for data in career_paths_data:
        career = created_careers[data["career"]]
        course = created_courses[data["course"]]
        obj, created = CareerPath.objects.get_or_create(
            career=career,
            course=course,
            defaults={"sequence_number": data["sequence"]}
        )
        status = "Created" if created else "Exists"
        print(f"  [{status}] CareerPath: {career.title} -> {course.title} (Seq {data['sequence']})")

       # =============================================================================
    # 7. ASSESSMENTS (All 5 Types)
    # =============================================================================
    print("\n[7/8] Creating Assessments...")

    # Skill ID shortcuts (dynamic)
    PY = skill_id_map["Python Programming"]
    JS = skill_id_map["JavaScript"]
    SQL = skill_id_map["SQL"]
    PS = skill_id_map["Problem Solving"]
    COM = skill_id_map["Communication"]
    TW = skill_id_map["Teamwork"]
    LD = skill_id_map["Leadership"]
    DA = skill_id_map["Data Analysis"]
    JV = skill_id_map["Java Programming"]
    RE = skill_id_map["React.js"]
    DJ = skill_id_map["Django"]
    ML = skill_id_map["Machine Learning"]
    PM = skill_id_map["Project Management"]
    CT = skill_id_map["Critical Thinking"]

    # -------------------------------------------------------------------------
    # 7.1 CAREER APTITUDE ASSESSMENT (Existing - kept for completeness)
    # -------------------------------------------------------------------------
    career_aptitude, created = Assessment.objects.get_or_create(
        title="Career Aptitude Assessment",
        defaults={
            "description": "Assess your career aptitude across multiple domains including programming, data analysis, management, and soft skills.",
            "passing_score": 70,
            "max_attempts": 3,
            "assessment_type": "career_aptitude",
            "target_level": "intermediate",
            "assessment_phase": "placement",
            "time_minutes": 60,
            "is_active": True,
            "questions": [
                {"id": 1, "skill_id": PY, "text": "What is the output of print(2 ** 3) in Python?", "options": ["6", "8", "9", "12"], "correct_answer": "8"},
                {"id": 2, "skill_id": PY, "text": "Which of the following is a valid Python variable name?", "options": ["2variable", "_variable", "var-iable", "var iable"], "correct_answer": "_variable"},
                {"id": 3, "skill_id": PY, "text": "What is the purpose of the 'self' keyword in Python?", "options": ["It refers to the current instance of the class", "It is used to define private methods", "It is used to import modules", "It is a built-in function"], "correct_answer": "It refers to the current instance of the class"},
                {"id": 4, "skill_id": JS, "text": "Which method is used to add an element to the end of a JavaScript array?", "options": ["append()", "push()", "add()", "insert()"], "correct_answer": "push()"},
                {"id": 5, "skill_id": JS, "text": "What does 'DOM' stand for in JavaScript?", "options": ["Document Object Model", "Data Object Model", "Document Oriented Model", "Dynamic Object Model"], "correct_answer": "Document Object Model"},
                {"id": 6, "skill_id": SQL, "text": "What is the correct SQL statement to select all columns from a table named 'employees'?", "options": ["SELECT * FROM employees", "SELECT ALL FROM employees", "SELECT employees FROM *", "SELECT columns FROM employees"], "correct_answer": "SELECT * FROM employees"},
                {"id": 7, "skill_id": SQL, "text": "Which SQL clause is used to filter rows in a query?", "options": ["WHERE", "FILTER", "HAVING", "CONDITION"], "correct_answer": "WHERE"},
                {"id": 8, "skill_id": PS, "text": "What is the first step in problem-solving?", "options": ["Define the problem", "Write the solution", "Test the solution", "Find the answer"], "correct_answer": "Define the problem"},
                {"id": 9, "skill_id": PS, "text": "Which approach is used to break a complex problem into smaller parts?", "options": ["Divide and conquer", "Greedy algorithm", "Brute force", "Randomization"], "correct_answer": "Divide and conquer"},
                {"id": 10, "skill_id": COM, "text": "What is the most important aspect of effective communication?", "options": ["Active listening", "Speaking loudly", "Using technical terms", "Writing long emails"], "correct_answer": "Active listening"},
                {"id": 11, "skill_id": COM, "text": "What is the best way to ensure clear communication in a team?", "options": ["Regular meetings and updates", "Sending emails only", "Avoiding direct communication", "Using complex terminology"], "correct_answer": "Regular meetings and updates"},
                {"id": 12, "skill_id": TW, "text": "What is the key to successful teamwork?", "options": ["Collaboration and trust", "Individual competition", "Strict hierarchy", "Limited communication"], "correct_answer": "Collaboration and trust"},
                {"id": 13, "skill_id": LD, "text": "What is a key trait of an effective leader?", "options": ["Empathy and vision", "Authoritarian control", "Micromanagement", "Avoiding decisions"], "correct_answer": "Empathy and vision"},
                {"id": 14, "skill_id": DA, "text": "What is data analysis?", "options": ["Process of inspecting, cleaning, and modeling data", "Storing data in databases", "Deleting unnecessary data", "Creating data visualizations only"], "correct_answer": "Process of inspecting, cleaning, and modeling data"},
                {"id": 15, "skill_id": DA, "text": "Which tool is commonly used for data analysis?", "options": ["Python (Pandas)", "Word", "PowerPoint", "Photoshop"], "correct_answer": "Python (Pandas)"},
            ]
        }
    )
    print(f"  [{'Created' if created else 'Exists'}] Assessment: {career_aptitude.title}")

    # -------------------------------------------------------------------------
    # 7.2 COURSE PLACEMENT ASSESSMENT (NEW)
    # -------------------------------------------------------------------------
    course_placement, created = Assessment.objects.get_or_create(
        title="Course Placement Assessment",
        defaults={
            "description": "Determine your starting level across programming and soft skills to place you in the right courses.",
            "passing_score": 60,
            "max_attempts": 2,
            "assessment_type": "course_placement",
            "target_level": "all_levels",
            "assessment_phase": "placement",
            "time_minutes": 45,
            "is_active": True,
            "questions": [
                {"id": 1, "skill_id": PY, "text": "What data type is the result of 10 / 3 in Python 3?", "options": ["int", "float", "double", "decimal"], "correct_answer": "float"},
                {"id": 2, "skill_id": PY, "text": "Which Python collection is ordered, mutable, and allows duplicate elements?", "options": ["Set", "Dictionary", "List", "Tuple"], "correct_answer": "List"},
                {"id": 3, "skill_id": PY, "text": "What does the 'def' keyword do in Python?", "options": ["Defines a variable", "Defines a function", "Defines a class", "Defines a module"], "correct_answer": "Defines a function"},
                {"id": 4, "skill_id": JS, "text": "What is the result of '5' + 3 in JavaScript?", "options": ["8", "'53'", "'8'", "NaN"], "correct_answer": "'53'"},
                {"id": 5, "skill_id": JS, "text": "Which operator checks both value and type equality in JavaScript?", "options": ["==", "===", "=", "!="], "correct_answer": "==="},
                {"id": 6, "skill_id": SQL, "text": "Which SQL keyword is used to remove duplicate rows from a result set?", "options": ["UNIQUE", "DISTINCT", "GROUP BY", "FILTER"], "correct_answer": "DISTINCT"},
                {"id": 7, "skill_id": SQL, "text": "What type of JOIN returns all records from the left table and matched records from the right?", "options": ["INNER JOIN", "RIGHT JOIN", "LEFT JOIN", "FULL JOIN"], "correct_answer": "LEFT JOIN"},
                {"id": 8, "skill_id": PS, "text": "If a program runs in O(n log n) time, what happens to runtime when input doubles?", "options": ["Doubles", "Quadruples", "Slightly more than doubles", "Stays the same"], "correct_answer": "Slightly more than doubles"},
                {"id": 9, "skill_id": PS, "text": "You have a bug that only appears in production. What is the best first step?", "options": ["Rewrite the entire module", "Check logs and reproduce locally", "Blame the infrastructure", "Add print statements everywhere"], "correct_answer": "Check logs and reproduce locally"},
                {"id": 10, "skill_id": COM, "text": "A teammate disagrees with your approach. What should you do first?", "options": ["Escalate to the manager", "Listen to their reasoning", "Defend your approach", "Ignore them"], "correct_answer": "Listen to their reasoning"},
                {"id": 11, "skill_id": CT, "text": "Which statement represents a logical fallacy?", "options": ["All birds can fly. Penguins are birds. Therefore penguins can fly.", "2 + 2 = 4", "Water boils at 100C at sea level", "The sun rises in the east"], "correct_answer": "All birds can fly. Penguins are birds. Therefore penguins can fly."},
                {"id": 12, "skill_id": CT, "text": "When evaluating a new technology for your team, what is most important?", "options": ["Hype and popularity", "Fit with current needs and constraints", "Number of GitHub stars", "Whether competitors use it"], "correct_answer": "Fit with current needs and constraints"},
            ]
        }
    )
    print(f"  [{'Created' if created else 'Exists'}] Assessment: {course_placement.title}")

    # -------------------------------------------------------------------------
    # 7.3 COURSE QUIZ - Python Fundamentals (NEW)
    # -------------------------------------------------------------------------
    python_quiz, created = Assessment.objects.get_or_create(
        title="Python Fundamentals - Mid-Course Quiz",
        defaults={
            "description": "Check your progress halfway through the Python Fundamentals course. Covers variables, loops, functions, and basic data structures.",
            "passing_score": 75,
            "max_attempts": 3,
            "assessment_type": "course_quiz",
            "target_level": "beginner",
            "assessment_phase": "progress",
            "time_minutes": 30,
            "is_active": True,
            "questions": [
                {"id": 1, "skill_id": PY, "text": "What is the correct way to create a function in Python?", "options": ["function myFunc():", "def myFunc():", "create myFunc():", "func myFunc():"], "correct_answer": "def myFunc():"},
                {"id": 2, "skill_id": PY, "text": "Which of these is a valid way to create a dictionary?", "options": ["dict = []", "dict = {}", "dict = ()", "dict = ||"], "correct_answer": "dict = {}"},
                {"id": 3, "skill_id": PY, "text": "What does the 'break' statement do in a loop?", "options": ["Skips to next iteration", "Exits the loop entirely", "Pauses the loop", "Restarts the loop"], "correct_answer": "Exits the loop entirely"},
                {"id": 4, "skill_id": PY, "text": "How do you create a list comprehension that squares numbers from 1 to 5?", "options": ["[x**2 for x in range(1, 6)]", "[x^2 for x in 1..5]", "map(lambda x: x**2, [1,2,3,4,5])", "[square(x) for x in range(5)]"], "correct_answer": "[x**2 for x in range(1, 6)]"},
                {"id": 5, "skill_id": PY, "text": "What does 'len([1, 2, 3])' return?", "options": ["2", "3", "4", "6"], "correct_answer": "3"},
                {"id": 6, "skill_id": PY, "text": "Which method adds an item to the end of a list?", "options": [".add()", ".append()", ".push()", ".insert()"], "correct_answer": ".append()"},
                {"id": 7, "skill_id": PY, "text": "What is the output of bool('') in Python?", "options": ["True", "False", "None", "Error"], "correct_answer": "False"},
                {"id": 8, "skill_id": PS, "text": "You need to find the largest number in a list. What is the most Pythonic approach?", "options": ["Write a manual for-loop", "Use the max() function", "Sort the list and pick first", "Use recursion"], "correct_answer": "Use the max() function"},
            ]
        }
    )
    print(f"  [{'Created' if created else 'Exists'}] Assessment: {python_quiz.title}")

    # -------------------------------------------------------------------------
    # 7.4 COURSE FINAL - Python Fundamentals (NEW)
    # -------------------------------------------------------------------------
    python_final, created = Assessment.objects.get_or_create(
        title="Python Fundamentals - Final Exam",
        defaults={
            "description": "Comprehensive final exam for Python Fundamentals. Covers OOP, file handling, error handling, and advanced concepts.",
            "passing_score": 70,
            "max_attempts": 2,
            "assessment_type": "course_final",
            "target_level": "beginner",
            "assessment_phase": "completion",
            "time_minutes": 60,
            "is_active": True,
            "questions": [
                {"id": 1, "skill_id": PY, "text": "What is the difference between a class and an object?", "options": ["They are the same", "A class is a blueprint, an object is an instance", "A class is faster", "An object is a blueprint"], "correct_answer": "A class is a blueprint, an object is an instance"},
                {"id": 2, "skill_id": PY, "text": "Which keyword is used to handle exceptions in Python?", "options": ["catch", "except", "handle", "error"], "correct_answer": "except"},
                {"id": 3, "skill_id": PY, "text": "What does the 'with' statement do when opening files?", "options": ["Makes code run faster", "Automatically closes the file", "Prevents file deletion", "Encrypts the file"], "correct_answer": "Automatically closes the file"},
                {"id": 4, "skill_id": PY, "text": "What is a lambda function?", "options": ["A named function", "An anonymous inline function", "A recursive function", "A built-in function"], "correct_answer": "An anonymous inline function"},
                {"id": 5, "skill_id": PY, "text": "Which of these is immutable in Python?", "options": ["List", "Dictionary", "Set", "Tuple"], "correct_answer": "Tuple"},
                {"id": 6, "skill_id": PY, "text": "What does @property decorator do?", "options": ["Makes a method private", "Turns a method into an attribute-like access", "Caches the result", "Makes it static"], "correct_answer": "Turns a method into an attribute-like access"},
                {"id": 7, "skill_id": PY, "text": "How do you inherit from a parent class in Python?", "options": ["class Child extends Parent:", "class Child(Parent):", "class Child inherits Parent:", "class Child: Parent"], "correct_answer": "class Child(Parent):"},
                {"id": 8, "skill_id": PY, "text": "What is the purpose of __init__.py in a package?", "options": ["It initializes variables", "It marks the directory as a Python package", "It runs on import", "It is required for all folders"], "correct_answer": "It marks the directory as a Python package"},
                {"id": 9, "skill_id": PS, "text": "You have a function that is O(n^2). For n=1000 it takes 1 second. About how long for n=2000?", "options": ["2 seconds", "4 seconds", "1 second", "8 seconds"], "correct_answer": "4 seconds"},
                {"id": 10, "skill_id": PS, "text": "Which data structure is best for checking if an item exists quickly?", "options": ["List", "Dictionary/Set", "Tuple", "String"], "correct_answer": "Dictionary/Set"},
                {"id": 11, "skill_id": CT, "text": "A junior dev suggests rewriting working code because it's 'not elegant'. What should you consider?", "options": ["Always rewrite for elegance", "Working code in production has value; weigh risk vs benefit", "Reject all suggestions from juniors", "Rewrite everything every sprint"], "correct_answer": "Working code in production has value; weigh risk vs benefit"},
                {"id": 12, "skill_id": CT, "text": "You find two libraries that solve the same problem. How do you choose?", "options": ["Pick the one with most stars", "Evaluate documentation, maintenance, license, and community", "Pick the newest one", "Use both simultaneously"], "correct_answer": "Evaluate documentation, maintenance, license, and community"},
            ]
        }
    )
    print(f"  [{'Created' if created else 'Exists'}] Assessment: {python_final.title}")

    # -------------------------------------------------------------------------
    # 7.5 SKILL ASSESSMENT - Full-Stack Development (NEW)
    # -------------------------------------------------------------------------
    fullstack_skill, created = Assessment.objects.get_or_create(
        title="Full-Stack Development Skill Assessment",
        defaults={
            "description": "Evaluate your readiness for full-stack development roles. Covers frontend, backend, databases, and system design thinking.",
            "passing_score": 65,
            "max_attempts": 3,
            "assessment_type": "skill_assessment",
            "target_level": "intermediate",
            "assessment_phase": "skill_evaluation",
            "time_minutes": 75,
            "is_active": True,
            "questions": [
                {"id": 1, "skill_id": PY, "text": "In Django, what is the purpose of a Model?", "options": ["Handles user interface", "Defines database schema and business logic", "Processes HTTP requests", "Manages static files"], "correct_answer": "Defines database schema and business logic"},
                {"id": 2, "skill_id": PY, "text": "What does a Django serializer do in DRF?", "options": ["Serializes Python objects to JSON/XML and vice versa", "Encrypts data", "Sorts querysets", "Validates HTML"], "correct_answer": "Serializes Python objects to JSON/XML and vice versa"},
                {"id": 3, "skill_id": DJ, "text": "What is the difference between FBV and CBV in Django?", "options": ["Function-Based Views vs Class-Based Views", "Fast Base View vs Cached Base View", "Frontend Backend View vs Client Backend View", "There is no difference"], "correct_answer": "Function-Based Views vs Class-Based Views"},
                {"id": 4, "skill_id": DJ, "text": "Which Django component handles URL routing?", "options": ["views.py", "urls.py", "models.py", "settings.py"], "correct_answer": "urls.py"},
                {"id": 5, "skill_id": RE, "text": "What is the purpose of useEffect in React?", "options": ["To create CSS effects", "To handle side effects in functional components", "To replace useState", "To optimize images"], "correct_answer": "To handle side effects in functional components"},
                {"id": 6, "skill_id": RE, "text": "What is the virtual DOM in React?", "options": ["A direct copy of the browser DOM", "A lightweight JavaScript representation of the DOM", "A database for components", "A CSS framework"], "correct_answer": "A lightweight JavaScript representation of the DOM"},
                {"id": 7, "skill_id": JS, "text": "What is a Promise in JavaScript?", "options": ["A guarantee that code will run", "An object representing eventual completion of an async operation", "A type of variable", "A design pattern"], "correct_answer": "An object representing eventual completion of an async operation"},
                {"id": 8, "skill_id": JS, "text": "What does 'async/await' simplify?", "options": ["CSS styling", "Asynchronous code readability", "Database queries", "HTML structure"], "correct_answer": "Asynchronous code readability"},
                {"id": 9, "skill_id": SQL, "text": "What is database normalization?", "options": ["Making data smaller", "Organizing data to reduce redundancy", "Encrypting the database", "Adding more tables"], "correct_answer": "Organizing data to reduce redundancy"},
                {"id": 10, "skill_id": SQL, "text": "What is an index in a database?", "options": ["A table of contents", "A data structure to speed up queries", "A primary key", "A foreign key constraint"], "correct_answer": "A data structure to speed up queries"},
                {"id": 11, "skill_id": PS, "text": "Your API is slow. What do you check first?", "options": ["Rewrite in a new language", "Check for N+1 queries and missing indexes", "Add more servers", "Disable authentication"], "correct_answer": "Check for N+1 queries and missing indexes"},
                {"id": 12, "skill_id": PS, "text": "A user reports a bug you can't reproduce. What is your approach?", "options": ["Close the ticket", "Ask for steps, environment details, and logs", "Blame the user's browser", "Fix random things hoping it helps"], "correct_answer": "Ask for steps, environment details, and logs"},
                {"id": 13, "skill_id": COM, "text": "How should you communicate a missed deadline to stakeholders?", "options": ["Hide it until the last minute", "Be transparent, explain why, and propose a new timeline", "Blame another team", "Promise it will never happen again without explanation"], "correct_answer": "Be transparent, explain why, and propose a new timeline"},
                {"id": 14, "skill_id": TW, "text": "In a code review, what is the most constructive approach?", "options": ["Approve everything to be nice", "Point out issues with suggestions for improvement", "Only comment on style", "Reject without explanation"], "correct_answer": "Point out issues with suggestions for improvement"},
                {"id": 15, "skill_id": CT, "text": "You need to choose between a monolith and microservices for a new project. What factors matter most?", "options": ["Always use microservices", "Team size, complexity, and scaling needs", "Always use monoliths", "What the CTO prefers"], "correct_answer": "Team size, complexity, and scaling needs"},
            ]
        }
    )
    print(f"  [{'Created' if created else 'Exists'}] Assessment: {fullstack_skill.title}")

    # =============================================================================
    # 8. ASSESSMENT SKILLS (All 5 Assessments)
    # =============================================================================
    print("\n[8/8] Creating Assessment Skills...")

    # 8.1 Career Aptitude Assessment Skills
    career_aptitude_skills = [
        {"skill": "Python Programming", "weightage": 25, "question_count": 3},
        {"skill": "JavaScript", "weightage": 10, "question_count": 2},
        {"skill": "SQL", "weightage": 15, "question_count": 2},
        {"skill": "Problem Solving", "weightage": 15, "question_count": 2},
        {"skill": "Communication", "weightage": 10, "question_count": 2},
        {"skill": "Teamwork", "weightage": 10, "question_count": 1},
        {"skill": "Leadership", "weightage": 5, "question_count": 1},
        {"skill": "Data Analysis", "weightage": 10, "question_count": 2},
    ]
    for data in career_aptitude_skills:
        skill = created_skills[data["skill"]]
        obj, created = AssessmentSkill.objects.get_or_create(
            assessment=career_aptitude,
            skill=skill,
            defaults={"weightage": data["weightage"], "question_count": data["question_count"]}
        )
        print(f"  [{'Created' if created else 'Exists'}] AssessmentSkill: {career_aptitude.title} -> {skill.name}")

    # 8.2 Course Placement Assessment Skills
    course_placement_skills = [
        {"skill": "Python Programming", "weightage": 25, "question_count": 3},
        {"skill": "JavaScript", "weightage": 15, "question_count": 2},
        {"skill": "SQL", "weightage": 20, "question_count": 2},
        {"skill": "Problem Solving", "weightage": 20, "question_count": 2},
        {"skill": "Communication", "weightage": 10, "question_count": 1},
        {"skill": "Critical Thinking", "weightage": 10, "question_count": 2},
    ]
    for data in course_placement_skills:
        skill = created_skills[data["skill"]]
        obj, created = AssessmentSkill.objects.get_or_create(
            assessment=course_placement,
            skill=skill,
            defaults={"weightage": data["weightage"], "question_count": data["question_count"]}
        )
        print(f"  [{'Created' if created else 'Exists'}] AssessmentSkill: {course_placement.title} -> {skill.name}")

    # 8.3 Python Fundamentals Quiz Skills
    python_quiz_skills = [
        {"skill": "Python Programming", "weightage": 85, "question_count": 7},
        {"skill": "Problem Solving", "weightage": 15, "question_count": 1},
    ]
    for data in python_quiz_skills:
        skill = created_skills[data["skill"]]
        obj, created = AssessmentSkill.objects.get_or_create(
            assessment=python_quiz,
            skill=skill,
            defaults={"weightage": data["weightage"], "question_count": data["question_count"]}
        )
        print(f"  [{'Created' if created else 'Exists'}] AssessmentSkill: {python_quiz.title} -> {skill.name}")

    # 8.4 Python Fundamentals Final Skills
    python_final_skills = [
        {"skill": "Python Programming", "weightage": 70, "question_count": 8},
        {"skill": "Problem Solving", "weightage": 20, "question_count": 2},
        {"skill": "Critical Thinking", "weightage": 10, "question_count": 2},
    ]
    for data in python_final_skills:
        skill = created_skills[data["skill"]]
        obj, created = AssessmentSkill.objects.get_or_create(
            assessment=python_final,
            skill=skill,
            defaults={"weightage": data["weightage"], "question_count": data["question_count"]}
        )
        print(f"  [{'Created' if created else 'Exists'}] AssessmentSkill: {python_final.title} -> {skill.name}")

    # 8.5 Full-Stack Skill Assessment Skills
    fullstack_skill_skills = [
        {"skill": "Python Programming", "weightage": 15, "question_count": 2},
        {"skill": "Django", "weightage": 15, "question_count": 2},
        {"skill": "React.js", "weightage": 15, "question_count": 2},
        {"skill": "JavaScript", "weightage": 15, "question_count": 2},
        {"skill": "SQL", "weightage": 15, "question_count": 2},
        {"skill": "Problem Solving", "weightage": 15, "question_count": 2},
        {"skill": "Communication", "weightage": 5, "question_count": 1},
        {"skill": "Teamwork", "weightage": 5, "question_count": 1},
    ]
    for data in fullstack_skill_skills:
        skill = created_skills[data["skill"]]
        obj, created = AssessmentSkill.objects.get_or_create(
            assessment=fullstack_skill,
            skill=skill,
            defaults={"weightage": data["weightage"], "question_count": data["question_count"]}
        )
        print(f"  [{'Created' if created else 'Exists'}] AssessmentSkill: {fullstack_skill.title} -> {skill.name}")
    # =============================================================================
    # 9. TEST STUDENT
    # =============================================================================
    print("\n[9/8] Creating Test Student...")

    student, created = User.objects.get_or_create(
        username="student1",
        defaults={
            "email": "student1@test.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "student",
            "is_active": True,
        }
    )
    # Always set/reset password
    student.set_password("Student@123")
    student.save()
    status = "Created" if created else "Updated password"
    print(f"  [{status}] Student: {student.username} / Password: Student@123")

    # =============================================================================
    # SUMMARY
    # =============================================================================
    print("\n" + "=" * 60)
    print("SEED DATA COMPLETE")
    print("=" * 60)
    print(f"Skills:          {Skill.objects.count()}")
    print(f"Categories:      {CourseCategory.objects.count()}")
    print(f"Courses:         {Course.objects.count()}")
    print(f"Careers:         {Career.objects.count()}")
    print(f"Career Skills:   {CareerSkill.objects.count()}")
    print(f"Career Paths:    {CareerPath.objects.count()}")
    print(f"Assessments:     {Assessment.objects.count()}")
    print(f"Assessment Skills: {AssessmentSkill.objects.count()}")
    print(f"Test Student:    student1 / Student@123")
    print(f"Superuser:       admin / admin@admin.com / Password: admin")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Login as student1")
    print("  2. POST /api/student-assessments/start/  -> assessment: {id}")
    print("  3. POST /api/student-assessments/{id}/submit/")
    print("  4. GET  /api/recommendations/careers/")
    print("=" * 60)


if __name__ == "__main__":
    try:
        seed_data()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    # =============================================================================
    # 10. SUPERUSER
    # =============================================================================
    print("\n[10/8] Creating Superuser...")

    superuser, created = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@admin.com",
            "first_name": "Admin",
            "last_name": "User",
            "role": "admin",
            "is_active": True,
            "is_staff": True,
            "is_superuser": True,
        }
    )
    # Always set/reset password
    superuser.set_password("admin")
    superuser.save()
    status = "Created" if created else "Updated password"
    print(f"  [{status}] Superuser: {superuser.username} / Email: {superuser.email} / Password: admin")

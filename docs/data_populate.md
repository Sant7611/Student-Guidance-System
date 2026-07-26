# COMPLETE DATA POPULATION FOR SKILLS, CAREERS, AND CAREER PATHS

Below is all the data you need to populate your system. **Follow this exact order** to maintain foreign key relationships.

---

## 📋 POPULATION ORDER

```
1. Create Skills (14 skills)
2. Create Courses (15 courses)
3. Create Career Categories/Industries (optional)
4. Create Careers (7 careers)
5. Create CareerSkill (Link careers to skills with scores & weightages)
6. Create CareerPath (Link careers to courses in sequence)
```

---

## 1. CREATE SKILLS

### POST `/api/skills/`

```json
[
    {
        "name": "Python Programming",
        "description": "Proficiency in Python including syntax, data structures, OOP, and standard libraries."
    },
    {
        "name": "JavaScript",
        "description": "Proficiency in JavaScript including ES6+, DOM manipulation, and async programming."
    },
    {
        "name": "SQL",
        "description": "Ability to write complex SQL queries, design databases, and optimize performance."
    },
    {
        "name": "Problem Solving",
        "description": "Analytical thinking, algorithmic design, and debugging capabilities."
    },
    {
        "name": "Communication",
        "description": "Clear written and verbal communication, active listening, and presentation skills."
    },
    {
        "name": "Teamwork",
        "description": "Collaboration, conflict resolution, and ability to work effectively in teams."
    },
    {
        "name": "Leadership",
        "description": "Team management, decision making, mentoring, and strategic thinking."
    },
    {
        "name": "Data Analysis",
        "description": "Data cleaning, statistical analysis, visualization, and insight generation."
    },
    {
        "name": "Java Programming",
        "description": "Proficiency in Java including OOP, collections, and enterprise frameworks."
    },
    {
        "name": "React.js",
        "description": "Building UI components, hooks, state management, and frontend architecture."
    },
    {
        "name": "Django",
        "description": "Web development with Django including ORM, views, templates, and REST APIs."
    },
    {
        "name": "Machine Learning",
        "description": "ML algorithms, model training, evaluation, and deployment."
    },
    {
        "name": "Project Management",
        "description": "Agile methodology, sprint planning, risk management, and stakeholder communication."
    },
    {
        "name": "Critical Thinking",
        "description": "Logical reasoning, evaluating arguments, and making informed decisions."
    }
]
```

---

## 2. CREATE COURSES

### POST `/api/courses/`

**Note:** You need to create CourseCategories first. Here are the categories:

#### Course Categories
```json
[
    {"title": "Programming", "description": "Programming languages and development"},
    {"title": "Database", "description": "Database design and management"},
    {"title": "Web Development", "description": "Frontend and backend web technologies"},
    {"title": "Data Science", "description": "Data analysis and machine learning"},
    {"title": "Soft Skills", "description": "Communication, leadership, and teamwork"},
    {"title": "Project Management", "description": "Project planning and execution"}
]
```

#### Courses

```json
[
    {
        "title": "Python Fundamentals",
        "prefix": "PY",
        "description": "Learn Python basics, data structures, and OOP concepts",
        "categories": [1],
        "level": "beginner",
        "price": 99.99,
        "is_active": true,
        "duration": "80:00:00"
    },
    {
        "title": "Advanced Python",
        "prefix": "APY",
        "description": "Advanced Python concepts, decorators, generators, and design patterns",
        "categories": [1],
        "level": "intermediate",
        "price": 149.99,
        "is_active": true,
        "duration": "120:00:00"
    },
    {
        "title": "JavaScript Essentials",
        "prefix": "JS",
        "description": "Core JavaScript, ES6, DOM manipulation, and async programming",
        "categories": [1, 3],
        "level": "beginner",
        "price": 99.99,
        "is_active": true,
        "duration": "60:00:00"
    },
    {
        "title": "React.js Mastery",
        "prefix": "RJ",
        "description": "Build modern web applications with React, hooks, and state management",
        "categories": [1, 3],
        "level": "intermediate",
        "price": 199.99,
        "is_active": true,
        "duration": "100:00:00"
    },
    {
        "title": "SQL for Data",
        "prefix": "SQL",
        "description": "Master SQL queries, joins, aggregations, and database design",
        "categories": [2],
        "level": "beginner",
        "price": 79.99,
        "is_active": true,
        "duration": "50:00:00"
    },
    {
        "title": "Advanced SQL",
        "prefix": "ASQ",
        "description": "Advanced SQL optimization, stored procedures, and performance tuning",
        "categories": [2],
        "level": "advanced",
        "price": 129.99,
        "is_active": true,
        "duration": "60:00:00"
    },
    {
        "title": "Django Full Stack",
        "prefix": "DJ",
        "description": "Build full-stack web applications with Django and Django REST Framework",
        "categories": [1, 3],
        "level": "intermediate",
        "price": 249.99,
        "is_active": true,
        "duration": "150:00:00"
    },
    {
        "title": "Java Programming",
        "prefix": "JV",
        "description": "Learn Java from basics to enterprise applications",
        "categories": [1],
        "level": "beginner",
        "price": 129.99,
        "is_active": true,
        "duration": "100:00:00"
    },
    {
        "title": "Data Analysis with Python",
        "prefix": "DA",
        "description": "Data cleaning, analysis, and visualization using Pandas, NumPy, and Matplotlib",
        "categories": [1, 4],
        "level": "intermediate",
        "price": 179.99,
        "is_active": true,
        "duration": "80:00:00"
    },
    {
        "title": "Machine Learning Basics",
        "prefix": "ML",
        "description": "Introduction to ML algorithms, scikit-learn, and model evaluation",
        "categories": [4],
        "level": "intermediate",
        "price": 199.99,
        "is_active": true,
        "duration": "100:00:00"
    },
    {
        "title": "Effective Communication",
        "prefix": "COM",
        "description": "Master communication skills, presentations, and professional writing",
        "categories": [5],
        "level": "beginner",
        "price": 69.99,
        "is_active": true,
        "duration": "40:00:00"
    },
    {
        "title": "Leadership Development",
        "prefix": "LD",
        "description": "Develop leadership skills, team management, and strategic thinking",
        "categories": [5, 6],
        "level": "intermediate",
        "price": 149.99,
        "is_active": true,
        "duration": "60:00:00"
    },
    {
        "title": "Project Management Pro",
        "prefix": "PM",
        "description": "Agile, Scrum, risk management, and stakeholder communication",
        "categories": [6],
        "level": "intermediate",
        "price": 229.99,
        "is_active": true,
        "duration": "80:00:00"
    },
    {
        "title": "Team Collaboration",
        "prefix": "TC",
        "description": "Build effective teams, resolve conflicts, and achieve collective goals",
        "categories": [5],
        "level": "beginner",
        "price": 79.99,
        "is_active": true,
        "duration": "40:00:00"
    },
    {
        "title": "Critical Thinking Mastery",
        "prefix": "CT",
        "description": "Develop logical reasoning, analytical thinking, and decision-making skills",
        "categories": [5],
        "level": "beginner",
        "price": 89.99,
        "is_active": true,
        "duration": "45:00:00"
    }
]
```

---

## 3. CREATE CAREERS

### POST `/api/careers/`

```json
[
    {
        "title": "Software Developer",
        "description": "Design, develop, and maintain software applications. Write clean, efficient code and collaborate with cross-functional teams.",
        "average_salary": "85000.00",
        "industry": "Technology",
        "skills": [1, 3, 4, 5, 6]
    },
    {
        "title": "Data Analyst",
        "description": "Analyze complex data, create reports, and provide actionable insights to support business decision-making.",
        "average_salary": "75000.00",
        "industry": "Technology",
        "skills": [3, 4, 8, 5, 14]
    },
    {
        "title": "Project Manager",
        "description": "Lead and oversee projects from initiation to completion. Manage teams, timelines, budgets, and stakeholder expectations.",
        "average_salary": "95000.00",
        "industry": "Management",
        "skills": [5, 6, 7, 13, 14]
    },
    {
        "title": "Web Developer",
        "description": "Build and maintain websites and web applications. Work with both frontend and backend technologies.",
        "average_salary": "80000.00",
        "industry": "Technology",
        "skills": [1, 2, 3, 10, 11]
    },
    {
        "title": "DevOps Engineer",
        "description": "Manage CI/CD pipelines, cloud infrastructure, containerization, and automate deployment processes.",
        "average_salary": "100000.00",
        "industry": "Technology",
        "skills": [1, 3, 4, 5, 6]
    },
    {
        "title": "Data Scientist",
        "description": "Apply machine learning algorithms, analyze complex datasets, and build predictive models to solve business problems.",
        "average_salary": "110000.00",
        "industry": "Data Science",
        "skills": [1, 3, 4, 8, 12, 14]
    },
    {
        "title": "Business Analyst",
        "description": "Bridge between business needs and technical solutions. Gather requirements, analyze processes, and recommend improvements.",
        "average_salary": "78000.00",
        "industry": "Business",
        "skills": [4, 5, 8, 13, 14]
    }
]
```

---

## 4. CREATE CAREER SKILLS (Link Skills to Careers)

### POST `/api/career-skills/`

**Replace the `career` and `skill` IDs with actual IDs from your database.**

```json
[
    {
        "career": 1,
        "skill": 1,
        "minimum_score": 70,
        "weightage": 25
    },
    {
        "career": 1,
        "skill": 3,
        "minimum_score": 60,
        "weightage": 20
    },
    {
        "career": 1,
        "skill": 4,
        "minimum_score": 70,
        "weightage": 20
    },
    {
        "career": 1,
        "skill": 5,
        "minimum_score": 65,
        "weightage": 15
    },
    {
        "career": 1,
        "skill": 6,
        "minimum_score": 60,
        "weightage": 10
    },
    {
        "career": 1,
        "skill": 14,
        "minimum_score": 60,
        "weightage": 10
    },
    {
        "career": 2,
        "skill": 3,
        "minimum_score": 70,
        "weightage": 30
    },
    {
        "career": 2,
        "skill": 4,
        "minimum_score": 65,
        "weightage": 20
    },
    {
        "career": 2,
        "skill": 5,
        "minimum_score": 60,
        "weightage": 15
    },
    {
        "career": 2,
        "skill": 8,
        "minimum_score": 70,
        "weightage": 25
    },
    {
        "career": 2,
        "skill": 14,
        "minimum_score": 60,
        "weightage": 10
    },
    {
        "career": 3,
        "skill": 5,
        "minimum_score": 75,
        "weightage": 30
    },
    {
        "career": 3,
        "skill": 6,
        "minimum_score": 70,
        "weightage": 20
    },
    {
        "career": 3,
        "skill": 7,
        "minimum_score": 70,
        "weightage": 25
    },
    {
        "career": 3,
        "skill": 13,
        "minimum_score": 70,
        "weightage": 15
    },
    {
        "career": 3,
        "skill": 14,
        "minimum_score": 65,
        "weightage": 10
    },
    {
        "career": 4,
        "skill": 1,
        "minimum_score": 60,
        "weightage": 15
    },
    {
        "career": 4,
        "skill": 2,
        "minimum_score": 70,
        "weightage": 20
    },
    {
        "career": 4,
        "skill": 3,
        "minimum_score": 50,
        "weightage": 10
    },
    {
        "career": 4,
        "skill": 10,
        "minimum_score": 70,
        "weightage": 25
    },
    {
        "career": 4,
        "skill": 11,
        "minimum_score": 65,
        "weightage": 20
    },
    {
        "career": 4,
        "skill": 5,
        "minimum_score": 60,
        "weightage": 10
    },
    {
        "career": 5,
        "skill": 1,
        "minimum_score": 70,
        "weightage": 25
    },
    {
        "career": 5,
        "skill": 3,
        "minimum_score": 60,
        "weightage": 20
    },
    {
        "career": 5,
        "skill": 4,
        "minimum_score": 70,
        "weightage": 20
    },
    {
        "career": 5,
        "skill": 5,
        "minimum_score": 65,
        "weightage": 15
    },
    {
        "career": 5,
        "skill": 6,
        "minimum_score": 60,
        "weightage": 10
    },
    {
        "career": 5,
        "skill": 14,
        "minimum_score": 60,
        "weightage": 10
    },
    {
        "career": 6,
        "skill": 1,
        "minimum_score": 65,
        "weightage": 15
    },
    {
        "career": 6,
        "skill": 3,
        "minimum_score": 60,
        "weightage": 15
    },
    {
        "career": 6,
        "skill": 4,
        "minimum_score": 75,
        "weightage": 20
    },
    {
        "career": 6,
        "skill": 8,
        "minimum_score": 70,
        "weightage": 15
    },
    {
        "career": 6,
        "skill": 12,
        "minimum_score": 70,
        "weightage": 20
    },
    {
        "career": 6,
        "skill": 14,
        "minimum_score": 70,
        "weightage": 15
    },
    {
        "career": 7,
        "skill": 4,
        "minimum_score": 70,
        "weightage": 25
    },
    {
        "career": 7,
        "skill": 5,
        "minimum_score": 70,
        "weightage": 25
    },
    {
        "career": 7,
        "skill": 8,
        "minimum_score": 60,
        "weightage": 15
    },
    {
        "career": 7,
        "skill": 13,
        "minimum_score": 65,
        "weightage": 20
    },
    {
        "career": 7,
        "skill": 14,
        "minimum_score": 65,
        "weightage": 15
    }
]
```

---

## 5. CREATE CAREER PATHS (Learning Paths)

### POST `/api/career-paths/`

**Replace the `career` and `course` IDs with actual IDs from your database.**

```json
[
    {
        "career": 1,
        "course": 1,
        "sequence_number": 1
    },
    {
        "career": 1,
        "course": 3,
        "sequence_number": 2
    },
    {
        "career": 1,
        "course": 5,
        "sequence_number": 3
    },
    {
        "career": 1,
        "course": 2,
        "sequence_number": 4
    },
    {
        "career": 1,
        "course": 7,
        "sequence_number": 5
    },
    {
        "career": 2,
        "course": 5,
        "sequence_number": 1
    },
    {
        "career": 2,
        "course": 1,
        "sequence_number": 2
    },
    {
        "career": 2,
        "course": 9,
        "sequence_number": 3
    },
    {
        "career": 2,
        "course": 6,
        "sequence_number": 4
    },
    {
        "career": 3,
        "course": 11,
        "sequence_number": 1
    },
    {
        "career": 3,
        "course": 12,
        "sequence_number": 2
    },
    {
        "career": 3,
        "course": 14,
        "sequence_number": 3
    },
    {
        "career": 3,
        "course": 13,
        "sequence_number": 4
    },
    {
        "career": 4,
        "course": 3,
        "sequence_number": 1
    },
    {
        "career": 4,
        "course": 1,
        "sequence_number": 2
    },
    {
        "career": 4,
        "course": 4,
        "sequence_number": 3
    },
    {
        "career": 4,
        "course": 7,
        "sequence_number": 4
    },
    {
        "career": 4,
        "course": 5,
        "sequence_number": 5
    },
    {
        "career": 5,
        "course": 1,
        "sequence_number": 1
    },
    {
        "career": 5,
        "course": 5,
        "sequence_number": 2
    },
    {
        "career": 5,
        "course": 7,
        "sequence_number": 3
    },
    {
        "career": 5,
        "course": 2,
        "sequence_number": 4
    },
    {
        "career": 6,
        "course": 1,
        "sequence_number": 1
    },
    {
        "career": 6,
        "course": 5,
        "sequence_number": 2
    },
    {
        "career": 6,
        "course": 9,
        "sequence_number": 3
    },
    {
        "career": 6,
        "course": 10,
        "sequence_number": 4
    },
    {
        "career": 6,
        "course": 2,
        "sequence_number": 5
    },
    {
        "career": 7,
        "course": 11,
        "sequence_number": 1
    },
    {
        "career": 7,
        "course": 15,
        "sequence_number": 2
    },
    {
        "career": 7,
        "course": 9,
        "sequence_number": 3
    },
    {
        "career": 7,
        "course": 13,
        "sequence_number": 4
    }
]
```

---

## 6. COMPLETE DATA FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────┐
│                     COMPLETE DATA FLOW                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. SKILLS (14)                                                     │
│     ├── Python Programming                                          │
│     ├── JavaScript                                                  │
│     ├── SQL                                                         │
│     ├── Problem Solving                                             │
│     ├── Communication                                               │
│     ├── Teamwork                                                    │
│     ├── Leadership                                                  │
│     ├── Data Analysis                                               │
│     ├── Java Programming                                            │
│     ├── React.js                                                    │
│     ├── Django                                                      │
│     ├── Machine Learning                                            │
│     ├── Project Management                                          │
│     └── Critical Thinking                                           │
│                                                                     │
│  2. CAREERS (7)                                                     │
│     ├── Software Developer                                          │
│     ├── Data Analyst                                                │
│     ├── Project Manager                                             │
│     ├── Web Developer                                               │
│     ├── DevOps Engineer                                             │
│     ├── Data Scientist                                              │
│     └── Business Analyst                                            │
│                                                                     │
│  3. CAREER SKILLS (40+ mappings)                                   │
│     └── Links careers → skills with minimum_score & weightage     │
│                                                                     │
│  4. COURSES (15)                                                    │
│     ├── Python Fundamentals                                         │
│     ├── Advanced Python                                             │
│     ├── JavaScript Essentials                                       │
│     ├── React.js Mastery                                            │
│     ├── SQL for Data                                                │
│     ├── Advanced SQL                                                │
│     ├── Django Full Stack                                           │
│     ├── Java Programming                                            │
│     ├── Data Analysis with Python                                   │
│     ├── Machine Learning Basics                                     │
│     ├── Effective Communication                                     │
│     ├── Leadership Development                                      │
│     ├── Project Management Pro                                      │
│     ├── Team Collaboration                                          │
│     └── Critical Thinking Mastery                                   │
│                                                                     │
│  5. CAREER PATHS (30+ sequences)                                   │
│     └── Links careers → courses in sequence_number                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. SAMPLE STUDENT ASSESSMENT WITH SKILL RESULTS

### Student Assessment Submission Response

```json
{
    "success": true,
    "data": {
        "id": 1,
        "student": {
            "id": 1,
            "username": "student1"
        },
        "assessment": {
            "id": 1,
            "title": "Career Aptitude Assessment"
        },
        "answers": {
            "answers": [
                {"question_id": 1, "answer": "8"},
                {"question_id": 2, "answer": "_variable"},
                {"question_id": 3, "answer": "It refers to the current instance of the class"},
                {"question_id": 4, "answer": "push()"},
                {"question_id": 5, "answer": "Document Object Model"},
                {"question_id": 6, "answer": "SELECT * FROM employees"},
                {"question_id": 7, "answer": "WHERE"},
                {"question_id": 8, "answer": "Define the problem"},
                {"question_id": 9, "answer": "Divide and conquer"},
                {"question_id": 10, "answer": "Active listening"},
                {"question_id": 11, "answer": "Regular meetings and updates"},
                {"question_id": 12, "answer": "Collaboration and trust"},
                {"question_id": 13, "answer": "Empathy and vision"},
                {"question_id": 14, "answer": "Process of inspecting, cleaning, and modeling data"},
                {"question_id": 15, "answer": "Python (Pandas)"}
            ]
        },
        "score": 85,
        "has_passed": true,
        "weak_skills": [
            {
                "skill_id": 3,
                "skill__name": "SQL",
                "score": 50
            },
            {
                "skill_id": 7,
                "skill__name": "Leadership",
                "score": 30
            }
        ],
        "attempt_number": 1,
        "status": "completed",
        "time_taken_seconds": 1200,
        "completed_at": "2024-01-15T10:50:00Z"
    }
}
```

---

## 8. STUDENT SKILL RESULTS (For Career Matching)

When a student completes an assessment, these `StudentSkillResult` records are created:

```json
[
    {
        "student_assessment": 1,
        "skill": 1,
        "score": 100
    },
    {
        "student_assessment": 1,
        "skill": 2,
        "score": 100
    },
    {
        "student_assessment": 1,
        "skill": 3,
        "score": 50
    },
    {
        "student_assessment": 1,
        "skill": 4,
        "score": 100
    },
    {
        "student_assessment": 1,
        "skill": 5,
        "score": 100
    },
    {
        "student_assessment": 1,
        "skill": 6,
        "score": 100
    },
    {
        "student_assessment": 1,
        "skill": 7,
        "score": 30
    },
    {
        "student_assessment": 1,
        "skill": 8,
        "score": 50
    }
]
```

---

## 9. POSTMAN COLLECTION VARIABLES

Set these variables for easy testing:

```json
{
    "base_url": "http://localhost:9009/api",
    "student_token": "your_jwt_token_here",
    "assessment_id": 1,
    "attempt_id": 1,
    "career_id": 1,
    "skill_id": 1,
    "course_id": 1
}
```

---

## 📊 DATA SUMMARY

| Type | Count | Description |
|------|-------|-------------|
| Skills | 14 | Technical and soft skills |
| Careers | 7 | Career options |
| Career Skills | 40+ | Skill mappings with scores & weightages |
| Courses | 15 | Learning courses |
| Career Paths | 30+ | Course sequences per career |
| Assessment | 1 | Career Aptitude Assessment |
| Questions | 15 | MCQ questions across all skills |

---

**💾 Save this as `career_data_population.json` for future reference!**
import json
import os
import uuid
import sys
from datetime import datetime, timedelta

def generate_environment(out_path):
    env = {
        "id": "ipb-tracker-env-id",
        "name": "Laras IPB Internship & Career Tracker API Environment Variables",
        "values": [
            {
                "key": "base_url",
                "value": "http://127.0.0.1:8000",
                "type": "default",
                "enabled": True
            },
            {
                "key": "admin_token",
                "value": "",
                "type": "secret",
                "enabled": True
            },
            {
                "key": "student_token",
                "value": "",
                "type": "secret",
                "enabled": True
            }
        ],
        "_postman_variable_scope": "environment"
    }
    with open(out_path, "w") as f:
        json.dump(env, f, indent=2)

def create_request(name, method, path, headers=None, body=None, test_script=""):
    req = {
        "name": name,
        "event": [
            {
                "listen": "test",
                "script": {
                    "exec": test_script.strip().split("\n") if test_script else [],
                    "type": "text/javascript"
                }
            }
        ],
        "request": {
            "method": method.upper(),
            "header": headers or [],
            "url": {
                "raw": "{{base_url}}" + path,
                "host": ["{{base_url}}"],
                "path": [p for p in path.split("/") if p]
            }
        },
        "response": []
    }
    
    if body:
        req["request"]["body"] = {
            "mode": "raw",
            "raw": json.dumps(body, indent=2),
            "options": {"raw": {"language": "json"}}
        }
    return req

def get_base_test(success_code_extra=""):
    return f"""
pm.test("Status code is successful 200 or 201", function () {{
    pm.expect(pm.response.code).to.be.oneOf([200, 201]);
}});
{success_code_extra}
"""

def generate_integration_collection(out_path):
    # Base data
    admin_email = "admin@example.com"
    student_email = f"student_{uuid.uuid4().hex[:6]}@example.com"
    admin_password = "Password123!"
    student_password = "Password123!"
    
    items = []
    
    # 1. Login Admin (using the seeded initial admin)
    items.append(create_request(
        "1. Login Admin", "POST", "/api/v1/auth/login",
        body={"email": admin_email, "password": admin_password},
        test_script=get_base_test("""
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("admin_token", jsonData.access_token);
}
""")
    ))
    
    admin_auth = [{"key": "Authorization", "value": "Bearer {{admin_token}}", "type": "text"}]
    student_auth = [{"key": "Authorization", "value": "Bearer {{student_token}}", "type": "text"}]

    # 2. Create Department
    items.append(create_request(
        "2. Create Department", "POST", "/api/v1/admin/departments",
        headers=admin_auth,
        body={"code": f"IL{uuid.uuid4().hex[:3].upper()}", "name": "Ilmu Komputer Admin", "faculty": "FMIPA"},
        test_script=get_base_test()
    ))
    
    # 3. Create Skill
    items.append(create_request(
        "3. Create Skill", "POST", "/api/v1/admin/skills",
        headers=admin_auth,
        body={"name": f"Integration Python {uuid.uuid4().hex[:4]}", "category": "Programming"},
        test_script=get_base_test("""
if (pm.response.code === 200 || pm.response.code === 201) {
    var jsonData = pm.response.json();
    pm.environment.set("integration_skill_id", jsonData.id);
}
""")
    ))
    
    # 4. Create Company
    items.append(create_request(
        "4. Create Company", "POST", "/api/v1/admin/companies",
        headers=admin_auth,
        body={
            "name": f"Integration Corp {uuid.uuid4().hex[:4]}",
            "industry": "Technology",
            "website_url": "https://integration.com",
            "address": "Bogor"
        },
        test_script=get_base_test("""
if (pm.response.code === 200 || pm.response.code === 201) {
    var jsonData = pm.response.json();
    pm.environment.set("integration_company_id", jsonData.id);
}
""")
    ))
    
    # 5. Create Vacancy
    items.append(create_request(
        "5. Create Vacancy", "POST", "/api/v1/vacancies",
        headers=admin_auth,
        body={
            "company_id": "{{integration_company_id}}",
            "title": "Integration Software Engineer Intern",
            "description": "This is an integration test description with minimum 20 chars.",
            "type": "INTERNSHIP_GENERAL",
            "open_date": (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z",
            "close_date": (datetime.utcnow() + timedelta(days=30)).isoformat() + "Z",
            "payment_type": "PAID",
            "compensation_min": 1500000.0,
            "compensation_max": 3000000.0,
            "skills": [
                {
                    "skill_id": "{{integration_skill_id}}",
                    "is_mandatory": True
                }
            ]
        },
        test_script=get_base_test("""
if (pm.response.code === 200 || pm.response.code === 201) {
    var jsonData = pm.response.json();
    pm.environment.set("integration_vacancy_id", jsonData.id);
}
""")
    ))
    
    # 6. Register Student
    items.append(create_request(
        "6. Register Student", "POST", "/api/v1/auth/register/student",
        body={
            "email": student_email,
            "password": student_password,
            "nim": f"G6419{uuid.uuid4().hex[:4].upper()}",
            "full_name": "Integration Student",
            "semester": 5
        },
        test_script=get_base_test()
    ))
    
    # 7. Login Student
    items.append(create_request(
        "7. Login Student", "POST", "/api/v1/auth/login",
        body={"email": student_email, "password": student_password},
        test_script=get_base_test("""
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("student_token", jsonData.access_token);
}
""")
    ))
    
    # 8. Get Student Profile
    items.append(create_request(
        "8. Get Student Profile", "GET", "/api/v1/profile/me",
        headers=student_auth,
        test_script=get_base_test()
    ))
    
    # 9. Update CV Data
    items.append(create_request(
        "9. Update CV Data", "PUT", "/api/v1/profile/cv-data",
        headers=student_auth,
        body={
            "phone_number": "+6281234567890",
            "linkedin_url": "https://linkedin.com/in/integration",
            "cv_url": "https://drive.google.com/file/1abc",
            "skills": [
                {
                    "skill_id": "{{integration_skill_id}}",
                    "level": 4
                }
            ]
        },
        test_script=get_base_test()
    ))
    
    # 10. Add Vacancy To Wishlist
    items.append(create_request(
        "10. Add Wishlist", "POST", "/api/v1/wishlist",
        headers=student_auth,
        body={
            "vacancy_id": "{{integration_vacancy_id}}",
            "notes": "Great internship."
        },
        test_script=get_base_test()
    ))
    
    # 11. Apply For Vacancy
    items.append(create_request(
        "11. Apply Vacancy", "POST", "/api/v1/applications",
        headers=student_auth,
        body={
            "vacancy_id": "{{integration_vacancy_id}}"
        },
        test_script=get_base_test()
    ))
    
    collection = {
        "info": {
            "name": "Laras IPB Internship & Career Tracker API Test",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": items
    }
    
    with open(out_path, "w") as f:
        json.dump(collection, f, indent=2)

if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(__file__), "..", "tests", "postman")
    os.makedirs(base_dir, exist_ok=True)
    
    env_path = os.path.join(base_dir, "Laras_IPB_Internship_API_Environment.postman_environment.json")
    coll_path = os.path.join(base_dir, "Laras_IPB_Internship_API_Test.postman_collection.json")
    
    generate_environment(env_path)
    generate_integration_collection(coll_path)
    
    print(f"Integration Postman collection generated at: {coll_path}")
    print(f"Integration Postman environment generated at: {env_path}")

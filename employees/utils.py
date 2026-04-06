import spacy
from .models import Employee
import re

nlp = spacy.load("en_core_web_sm")


def ai_to_sql(query):
    query = query.lower()

    # OLDEST 
    if "oldest" in query or "maximum age" in query:
        return Employee.objects.order_by('-age')[:1]

    # YOUNGEST
    if "youngest" in query or "minimum age" in query:
        return Employee.objects.order_by('age')[:1]

    # HIGHEST SALARY
    if ("highest" in query or "maximum" in query or "top" in query) and "salary" in query:
        return Employee.objects.order_by('-salary')[:1]

    # LOWEST SALARY
    if ("lowest" in query or "minimum" in query) and "salary" in query:
        return Employee.objects.order_by('salary')[:1]

    #  SHOW ALL EMPLOYEES
    if "show" in query or "all employees" in query:
        return Employee.objects.all()

    filters = {}

    # 
    numbers = [int(n) for n in re.findall(r'\d+', query)]

    # Salary filter
    if ("salary" in query or "earn" in query):
        if "more than" in query or "greater than" in query:
            if numbers:
                filters['salary__gt'] = numbers[0]
        elif "less than" in query:
            if numbers:
                filters['salary__lt'] = numbers[0]

    # Age filter (second number if exists)
    if "older than" in query or "age" in query:
        if len(numbers) > 1:
            filters['age__gt'] = numbers[1]
        elif numbers:
            filters['age__gt'] = numbers[0]

    # Location filter
    for emp in Employee.objects.all():
        if emp.location.lower() in query:
            filters['location__iexact'] = emp.location
            break

    # Apply filters
    if filters:
        return Employee.objects.filter(**filters)

    return None

#MAIN NLP FUNCTION
def process_query(user_input):
    user_input_lower = user_input.lower()
    doc = nlp(user_input)

    
    result = ai_to_sql(user_input)

    if result is not None:
      if result.exists():
        emp_list = [f"{emp.name} (Age: {emp.age}, Salary: {emp.salary})" for emp in result]
        return "\n".join(emp_list)
      else:   
        return "No employees found"
      
    words = user_input.split()

    for word in words:
        try:
            emp = Employee.objects.get(emp_id__iexact=word)
            return f"{emp.emp_id} | {emp.name} | {emp.department} | {emp.salary}"
        except:
            continue
#Step 2: name detection
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    emp= None

    if names:
        try:
            emp = Employee.objects.get(name__iexact=names[0])
        except:
            emp = None

    #Step 3: Fallback
    if not emp:
        words = user_input.split()
        for word in words:
            try:
                emp = Employee.objects.get(name__iexact=word)
                break
            except:
                continue

    if not emp:
        return "Employee not found"


   
    if "salary" in user_input_lower:
        return f"{emp.name}'s salary is {emp.salary}"

    
    if "location" in user_input_lower or "live" in user_input_lower or "where" in user_input_lower:
        return f"{emp.name} lives in {emp.location}"

    if "age" in user_input_lower or "old" in user_input_lower:
        return f"{emp.name} is {emp.age} years old"

    return "Try asking about salary, age, or location"
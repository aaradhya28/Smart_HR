from django.shortcuts import render,redirect
from .utils import process_query
import pandas as pd
from .models import Employee
# Create your views here.

chat_history = []

def home(request):
    if request.method == "POST":
        user_input = request.POST.get("query")
        response = process_query(user_input)

        chat_history.append({
            "user": user_input,
            "bot": response
        })

    return render(request, "home.html", {"chats": chat_history})

def upload_csv(request):
    if request.method == "POST":
        file = request.FILES.get("file")

        if not file:
            return render(request, "upload.html", {"error": "No file uploaded"})

        try:
           
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)

            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file, engine='openpyxl')

            elif file.name.endswith('.xls'):
                df = pd.read_excel(file, engine='xlrd')

            else:
                return render(request, "upload.html", {
                    "error": "Unsupported file format. Use CSV, XLSX, or XLS"
                })

           
            df.columns = df.columns.str.strip().str.lower()

            
            required_cols = ['emp_id', 'name', 'salary', 'age', 'location', 'department']
            for col in required_cols:
                if col not in df.columns:
                    return render(request, "upload.html", {
                        "error": f"Missing column: {col}"
                    })

            
            df['department'] = df['department'].astype(str).str.strip()

           
            for _, row in df.iterrows():
                Employee.objects.update_or_create(
                    emp_id=row['emp_id'],
                    defaults={
                        "name": row['name'],
                        "salary": int(row['salary']),
                        "age": int(row['age']),
                        "location": row['location'],
                        "department": row['department']
                    }
                )

            return redirect('home')

        except Exception as e:
            return render(request, "upload.html", {"error": str(e)})

    return render(request, "upload.html")




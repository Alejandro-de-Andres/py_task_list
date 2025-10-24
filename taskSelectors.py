from common import *

console = Console()
TASK_FILE = "task.json"

def idTitleList():
    with open(TASK_FILE, "r", encoding="utf-8") as archive:
        data = json.load(archive)
        
        for task in data["tasks"]:
            print(f"{task['title']}")
    
def idTitleOption():
    with open(TASK_FILE, "r", encoding="utf-8") as archive:
        data = json.load(archive)
        
        choices_list = [{"name": "Salir", "value": "0"}]
        for task in data['tasks']:
            choices_list.append({
                "name": f"{task['title']}", 
                "value": task['id']})
                        
        return(choices_list)

def idMax():
    with open(TASK_FILE, "r", encoding="utf-8") as archive:
        data = json.load(archive)
        
        idList = []        
        for task in data["tasks"]:
            idList.append(task["id"])
            
        if not idList:
            return 0
        
        return max(idList)

def dateFormat():
    today = date.today()
    
    month_dict = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }
    
    while True:
        year = inquirer.select(
            message = "Seleccion un año: ",
            choices = (i for i in range(today.year, today.year + 5))
        ).execute()
        
        month = inquirer.select(
            message = "Seleccione un mes: ",
            choices = [
                {"name": name, "value": key}
                for key, name in month_dict.items()
            ]
        ).execute()
        
        console.print("[bold cyan] Seleccione un día: [/]\n")
        for i in range(1, 32):
            console.print(f"{i:2}", end="  ") # {i:2} Space between numbers
            if i % 7 == 0:
                console.print()
        console.print("\n") 

        max_days = 31
        if month == 4 or month == 6 or month == 9 or month == 11:
            max_days = 30
        elif month == 2 and calendar.isleap(year):
            max_days = 29
        elif month == 2 and not calendar.isleap(year):
            max_days = 28

        day = inquirer.number(
            message="Introduce el número del día:",
            min_allowed = 1,
            max_allowed = 31,
        ).execute()
    
        try:
            endDate = datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d')
            if endDate.date() >= today:
                return endDate.date()
            else:
                console.print(f"[red]❌ La fecha debe ser igual o superior a la actual [/]\nFecha actual: {today.year}-{today.month}-{today.day}")
                time.sleep(3)
        except:
            console.print("[red]❌ Fecha no válida [/]")
            time.sleep(3)


import json
from datetime import date
import time
# Drawing prints - Needs 'console = Console()'
from rich.console import Console # python -m pip install rich
# Menu selectors
from InquirerPy import inquirer # pip install inquirerpy

console = Console()
TASK_FILE = "task.json"

#TODO: Añadir el resto de elementos a las listas

def idTitleList():
    with open(TASK_FILE, "r", encoding="utf-8") as archive:
        data = json.load(archive)
        
        for task in data["tasks"]:
            print(f"{task['id']} - {task['title']}")
    
def idTitleOption():
    with open(TASK_FILE, "r", encoding="utf-8") as archive:
        data = json.load(archive)
        
        choices_list = [{"name": "0 - Salir", "value": "0"}]
        for task in data['tasks']:
            print("Hola")
            choices_list.append({
                "name": f"{task['id']} - {task['title']}", 
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
        
        return idList

def create():
    #TODO: Meterlo todo en un diccionario o algo así para que sea más fácil
    values = {}
    values["id"] = idMax() + 1
    values["title"] = input("Título: ")
    values["description"] = input("Descripción: ")
    values["state"] = inquirer.select(
        message = "Estado: ",
        choices = ("⏳ Pendiente", "🔄 En progreso", "✅ Realizado")
    ).execute()
    values["startDate"] = date.today()
    values["finalDate"] = date.today() #TODO: Implementar menú para elección de fecha. Debe ser superior a la actual
    
    print(values)
    
    #TODO: Debe actualizar el JSON

def read():
    choices_list = idTitleOption()
    id_task = inquirer.select(
        message = "¿Qué tarea quiere visualizar? :",
        choices = choices_list
    ).execute()
    
    print(type(id_task))
    
    if id_task != "0":
        with open(TASK_FILE, "r", encoding="utf-8") as archive:
            data = json.load(archive)
            
            # Recorre el apartado tasks del JSON en busca del id seleccionado
            tarea = next((task for task in data["tasks"] if task["id"] == id_task), None)
            if tarea:
                console.print(f"[bold red]Título:[/bold red] {tarea['title']}\n[bold magenta]Description: [/bold magenta]{tarea['description']}\n[bold yellow]Estado: [/bold yellow]{tarea['state']}\n[bold blue]Fecha inicio: [/bold blue]{tarea['startDate']}\n[bold dark_blue]Fecha fin: [/bold dark_blue]{tarea['finalDate']}")
                time.sleep(7)
                 
def update():
    choices_list = idTitleOption()
    id_task = inquirer.select(
        message = "¿Qué tarea quiere actualizar? :",
        choices = choices_list
    ).execute()
    
    with open(TASK_FILE, "r+", encoding="utf-8") as archive:
        data = json.load(archive)
        if id_task != 0:
            tarea = next((task for task in data["tasks"] if task["id"] == id_task), None)
            
            #TODO: Implementar while para quitar el update() de debajo del sleep()
            if tarea:
                update_option = inquirer.select(
                    message = "Selecciona una acción:",
                    choices = [
                        {"name": "Salir", "value": 0},
                        {"name": f"Título -> {tarea['title']}", "value": 1},
                        {"name": f"Descripción -> {tarea['description']}", "value": 2},
                        {"name": f"Estado -> {tarea['state']}", "value": 3}, 
                        {"name": f"Fecha fin -> {tarea['finalDate']}", "value": 4}
                    ]
                ).execute()
                
                if update_option == 0:
                    return False
                elif update_option == 1:
                    new_title = input("Nuevo título: ")
                    tarea["title"] = new_title
                elif update_option == 2:
                    input("Nueva descripción: ")
                    new_description = input("Nuevo título: ")
                    tarea["description"] = new_description
                elif update_option == 3:
                    new_state = inquirer.select(
                        message = "Actualizar estado :",
                        choices = ["⏳ Pendiente", "🔄 En progreso", "✅ Realizado"]
                    ).execute()
                    tarea["state"] = new_state
                else:
                    #TODO: Implementar modo de codificar fecha de forma cómoda para el usuario
                    print("Acción en desarrollo")
                
                archive.seek(0) # Pointer in line 0
                json.dump(data, archive, indent=4, ensure_ascii=False)
                archive.truncate() # Deletes the last JSON
                idTitleList()
            else:
                print("Esa tarea no existe")
                time.sleep(5)
                update()
        else:
            return False

def delete():
    choices_list = idTitleOption()
    id_delete = inquirer.select(
        message = "¿Qué tarea quiere eliminar? :",
        choices = choices_list
    ).execute()
    
    with open(TASK_FILE, "r+", encoding="utf-8") as archive:
        data = json.load(archive)
        if id_delete != 0:
            # Con next, buscamos la primera tarea que cumpla lo que estamos buscando, si no encuentra nada, 
            # en vez de devolver una excepción, devuelve none.
            tarea = next((task for task in data["tasks"] if task["id"] == id_delete), None)
            
            if tarea:
                delete_confirm = inquirer.select(
                    message = f"Se va a eliminar {tarea['id']} - {tarea['title']}. ¿Es correcto?",
                    choices = [
                        {"name": "No", "value": 0},
                        {"name": "Sí", "value": 1}
                    ]
                ).execute()
                
                if delete_confirm == 1:
                    data["tasks"] = [t for t in data["tasks"] if t["id"] != id_delete]
                    
                    archive.seek(0) #Puntero en línea 0
                    json.dump(data, archive, indent=4, ensure_ascii=False)
                    archive.truncate() #Eliminar fichero anterior
                    idTitleList()
      
# idTitleList()
# idTitleOption()
# idMax()
# create()
read()
# update()
# delete()
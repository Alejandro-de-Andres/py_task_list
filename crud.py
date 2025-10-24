from common import *
from taskSelectors import *

#TODO: Añadir el resto de elementos a las listas

def create():
    with open(TASK_FILE, "r", encoding="utf-8") as archive:
        data = json.load(archive)
        
        values = {}
        values["id"] = idMax() + 1
        values["title"] = input("Título: ")
        values["description"] = input("Descripción: ")
        values["state"] = inquirer.select(
            message = "Estado: ",
            choices = [
                {"name": "⏳ Pendiente", "value": ":hourglass_not_done: Pendiente"},
                {"name": "🔄 En progreso", "value": ":arrows_counterclockwise: En progreso"},
                {"name": "✅ Realizado", "value": ":white_check_mark: Realizado"}
            ]
        ).execute()
        values["startDate"] = str(date.today())
        values["endDate"] = str(dateFormat())
    
        data["tasks"].append(values)
        # Sobreescribe el documento
    with open(TASK_FILE, "w", encoding="utf-8") as archive:
        json.dump(data, archive, indent=4, ensure_ascii = False)
        
    console.print("[green] Tarea creada con éxito [/]")
    time.sleep(3)

def read():
    # TODO: Habría que poner el salir al final
    choices_list = idTitleOption()
    id_task = inquirer.select(
        message = "¿Qué tarea quiere visualizar? :",
        choices = choices_list
    ).execute()
    
    if id_task != "0":
        with open(TASK_FILE, "r", encoding="utf-8") as archive:
            data = json.load(archive)
            
            # Recorre el apartado tasks del JSON en busca del id seleccionado
            tarea = next((task for task in data["tasks"] if task["id"] == id_task), None)
            if tarea:
                console.print(f"[bold red]Título:[/] {tarea['title']}\n[bold color(166)]Descripción: [/]{tarea['description']}\n[bold yellow]Estado: [/]{tarea['state']}\n[bold blue]Fecha inicio: [/]{tarea['startDate']}\n[bold color(165)]Fecha fin: [/]{tarea['endDate']}")
                time.sleep(5)
                 
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
                        {"name": f"Fecha fin -> {tarea['endDate']}", "value": 4}
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
                json.dump(data, archive, indent=4, ensure_ascii = False)
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
        message = "\n¿Qué tarea quiere eliminar? :",
        choices = choices_list
    ).execute()
    
    with open(TASK_FILE, "r", encoding="utf-8") as archive:
        data = json.load(archive)
        if id_delete != 0:
            # With next, it searchs the first task which has what we are looking for. And if it doesn't find anything, return None, not an exception.
            tarea = next((task for task in data["tasks"] if task["id"] == id_delete), None)
            
            if tarea:
                delete_confirm = inquirer.select(
                    message = f"Se va a eliminar {tarea['title']} - {tarea['description']}. ¿Es correcto?",
                    choices = [
                        {"name": "No", "value": 0},
                        {"name": "Sí", "value": 1}
                    ]
                ).execute()
                
                if delete_confirm == 1:
                    data["tasks"] = [t for t in data["tasks"] if t["id"] != id_delete]
                    
                    with open(TASK_FILE, "w", encoding="utf-8") as archive:
                        json.dump(data, archive, indent=4, ensure_ascii = False)
                    console.print(f"[b green]Se ha eliminado la tarea {tarea['title']}[/]\n")
                    time.sleep(2)
                else:
                    time.sleep(1)
                    delete()
      
# create()
# read()
# update()
# delete()
import json
from datetime import date
import time
from InquirerPy import inquirer # pip install InquirerPy


#TODO: Añadir el resto de elementos a las listas

def create():
    #TODO: Meterlo todo en un diccionario o algo así para que sea más fácil
    id = 0 #TODO: Debe tomar el ID máximo y sumarle 1
    title = input("Título: ")
    description = input("Descripción: ")
    state = "⏳ Pendiente"
    startDate = date.today()
    finalDate = date.today() #TODO: Implementar menú para elección de fecha. Debe ser superior a la actual

def read():
    #TODO: Listar todas las tareas en bonito
    with open("proyects/taskList/task.json", "r", encoding="utf-8") as archive:
        data = json.load(archive)

    print(data)


def update():
    choices_list = idTitleOption()
    id_task = inquirer.select(
        message = "¿Qué tarea quiere actualizar? :",
        choices = choices_list
    ).execute()
    
    with open("proyects/taskList/task.json", "r+", encoding="utf-8") as archive:
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
                
                archive.seek(0) #Puntero en línea 0
                json.dump(data, archive, indent=4, ensure_ascii=False)
                archive.truncate() #Eliminar fichero anterior
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
    
    with open("proyects/taskList/task.json", "r+", encoding="utf-8") as archive:
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

def idTitleList():
    with open("proyects/taskList/task.json", "r", encoding="utf-8") as archive:
        data = json.load(archive)
        
        for task in data["tasks"]:
            print(f"{task['id']} - {task['title']}")
    
def idTitleOption():
    with open("proyects/taskList/task.json", "r", encoding="utf-8") as archive:
        data = json.load(archive)
        
        choices_list = [{"name": "0 - Salir", "value": "0"}]
        for task in data["tasks"]:
            choices_list.append({
                "name": f"{task['id']} - {task['title']}", 
                "value": task["id"]})
            
        return(choices_list)
# main.py

# ---------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------
from db.projects_crud import (
    list_projects,
    get_project_by_id,
    get_all_projects,
    create_project,
    update_project_partial,
    delete_project_interactive
)


# ---------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------
def main_menu():
    while True:
        print("\n=== MAIN MENU ===")
        print("1. Projects")
        print("2. People")
        print("3. Experiments")
        print("4. Mice")
        print("5. Cells")
        print("6. Drugs")
        print("7. ACSF Types")
        print("8. Internal Types")
        print("9. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            projects_menu()
        elif choice == "2":
            people_menu()
        elif choice == "3":
            experiments_menu()
        elif choice == "4":
            mice_menu()
        elif choice == "5":
            cells_menu()
        elif choice == "6":
            drugs_menu()
        elif choice == "7":
            acsf_menu()
        elif choice == "8":
            internal_menu()
        elif choice == "9":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")



# ---------------------------------------------------------
# IMPORTS FOR PROJECTS
# ---------------------------------------------------------
from db.projects_crud import (
    list_projects,
    get_project_by_id,
    create_project,
    update_project_partial,
    delete_project_interactive
)

# ---------------------------------------------------------
# PROJECTS MENU
# ---------------------------------------------------------
def projects_menu():
    while True:
        print("\n=== PROJECTS MENU ===")
        print("1. List all projects")
        print("2. View a project")
        print("3. Create a project")
        print("4. Update a project")
        print("5. Delete a project")
        print("6. Back to main menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            list_projects()

        elif choice == "2":
            view_project_interactive()

        elif choice == "3":
            create_project_interactive()

        elif choice == "4":
            update_project_interactive()

        elif choice == "5":
            delete_project_interactive_prompt()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")


# ---------------------------------------------------------
# VIEW PROJECT
# ---------------------------------------------------------
def view_project_interactive():
    print("\n=== VIEW PROJECT ===")
    print("Search by:")
    print("1. ID")
    print("2. Name")
    print("3. PI")
    print("4. Start date (YYYY-MM-DD)")
    print("5. Notes")
    print("6. Cancel")

    choice = input("Select an option: ").strip()

    if choice == "1":
        value = input("Enter project ID: ").strip()
        results = [get_project_by_id(value)]

    else:
        # Load all projects once
        projects = get_all_projects()

        if choice == "2":
            value = input("Enter name (partial ok): ").strip().lower()
            results = [p for p in projects if value in p["name"].lower()]

        elif choice == "3":
            value = input("Enter PI (partial ok): ").strip().lower()
            results = [p for p in projects if p["pi"] and value in p["pi"].lower()]

        elif choice == "4":
            value = input("Enter start date (YYYY-MM-DD): ").strip()
            results = [p for p in projects if p["start_date"] == value]

        elif choice == "5":
            value = input("Enter notes text (partial ok): ").strip().lower()
            results = [p for p in projects if p["notes"] and value in p["notes"].lower()]

        elif choice == "6":
            return

        else:
            print("Invalid choice.")
            return

    # Filter out None results (ID search may return None)
    results = [r for r in results if r]

    if not results:
        print("\nNo matching projects found.")
        return

    print(f"\n=== {len(results)} PROJECT(S) FOUND ===")
    for project in results:
        print("\n----------------------")
        for key, value in project.items():
            print(f"{key}: {value}")


# ---------------------------------------------------------
# CREATE PROJECT
# ---------------------------------------------------------
def create_project_interactive():
    print("\n=== CREATE PROJECT ===")
    name = input("Project name: ").strip()
    description = input("Description (optional): ").strip() or None
    pi = input("PI / Owner (optional): ").strip() or None
    start_date = input("Start date (YYYY-MM-DD, optional): ").strip() or None
    notes = input("Notes (optional): ").strip() or None

    try:
        project_id = create_project(
            name=name,
            description=description,
            pi=pi,
            start_date=start_date,
            notes=notes
        )
        print(f"Project created with ID {project_id}.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# UPDATE PROJECT
# ---------------------------------------------------------
def update_project_interactive():
    project_id = input("Enter project ID to update: ").strip()
    if not project_id.isdigit():
        print("Invalid ID.")
        return

    project_id = int(project_id)
    project = get_project_by_id(project_id)
    if project is None:
        print("Project not found.")
        return

    print("\nLeave fields blank to keep current values.\n")

    name = input(f"Name [{project['name']}]: ").strip() or project['name']
    description = input(f"Description [{project['description']}]: ").strip() or project['description']
    pi = input(f"PI [{project['pi']}]: ").strip() or project['pi']
    start_date = input(f"Start date [{project['start_date']}]: ").strip() or project['start_date']
    notes = input(f"Notes [{project['notes']}]: ").strip() or project['notes']

    try:
        update_project_partial(
            project_id,
            name=name,
            description=description,
            pi=pi,
            start_date=start_date,
            notes=notes
        )
        print("Project updated.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# DELETE PROJECT
# ---------------------------------------------------------
def delete_project_interactive_prompt():
    project_id = input("Enter project ID to delete: ").strip()
    if not project_id.isdigit():
        print("Invalid ID.")
        return

    delete_project_interactive(int(project_id))



# ---------------------------------------------------------
# IMPORTS FOR EXPERIMENTS
# ---------------------------------------------------------
from db.experiments_crud import (
    list_experiments,
    get_experiment_by_id,
    create_experiment,
    update_experiment_partial,
    delete_experiment_interactive
)

from db.projects_crud import list_projects
from db.people_crud import list_people
from db.mouse_strains_crud import list_mouse_strains
from db.acsf_types_crud import list_acsf_types
from db.internal_types_crud import list_internal_types


# ---------------------------------------------------------
# EXPERIMENTS MENU
# ---------------------------------------------------------
def experiments_menu():
    while True:
        print("\n=== EXPERIMENTS MENU ===")
        print("1. List all experiments")
        print("2. View an experiment")
        print("3. Create an experiment")
        print("4. Update an experiment")
        print("5. Delete an experiment")
        print("6. Back to main menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            list_experiments()

        elif choice == "2":
            view_experiment_interactive()

        elif choice == "3":
            create_experiment_interactive()

        elif choice == "4":
            update_experiment_interactive()

        elif choice == "5":
            delete_experiment_interactive_prompt()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")


# ---------------------------------------------------------
# VIEW EXPERIMENT
# ---------------------------------------------------------
def view_experiment_interactive():
    exp_id = input("Enter experiment ID: ").strip()
    if not exp_id.isdigit():
        print("Invalid ID.")
        return

    exp = get_experiment_by_id(int(exp_id))
    if exp is None:
        print("Experiment not found.")
        return

    print("\n=== EXPERIMENT DETAILS ===")
    for key, value in exp.items():
        print(f"{key}: {value}")


# ---------------------------------------------------------
# CREATE EXPERIMENT (Hybrid)
# ---------------------------------------------------------
def create_experiment_interactive():
    print("\n=== CREATE EXPERIMENT ===")

    name = input("Experiment name: ").strip()

    print("\nAvailable projects:")
    list_projects()
    project_id = input("Project ID: ").strip()
    if not project_id.isdigit():
        print("Invalid project ID.")
        return

    print("\nAvailable experimenters:")
    list_people()
    person_id = input("Experimenter (person) ID: ").strip()
    if not person_id.isdigit():
        print("Invalid person ID.")
        return

    # Important scientific metadata
    min_mice = input("Minimum mice required (optional): ").strip() or None
    min_mice = int(min_mice) if min_mice and min_mice.isdigit() else None

    cells_per_mouse = input("Cells per mouse (optional): ").strip() or None
    cells_per_mouse = int(cells_per_mouse) if cells_per_mouse and cells_per_mouse.isdigit() else None

    print("\nAvailable mouse strains:")
    list_mouse_strains()
    mouse_strain_id = input("Mouse strain ID (optional): ").strip() or None
    mouse_strain_id = int(mouse_strain_id) if mouse_strain_id and mouse_strain_id.isdigit() else None

    print("\nAvailable ACSF types:")
    list_acsf_types()
    acsf_type_id = input("ACSF type ID (optional): ").strip() or None
    acsf_type_id = int(acsf_type_id) if acsf_type_id and acsf_type_id.isdigit() else None

    print("\nAvailable internal solution types:")
    list_internal_types()
    internal_type_id = input("Internal type ID (optional): ").strip() or None
    internal_type_id = int(internal_type_id) if internal_type_id and internal_type_id.isdigit() else None

    ideal_min = input("Ideal mouse age MIN (days, optional): ").strip() or None
    ideal_min = int(ideal_min) if ideal_min and ideal_min.isdigit() else None

    ideal_max = input("Ideal mouse age MAX (days, optional): ").strip() or None
    ideal_max = int(ideal_max) if ideal_max and ideal_max.isdigit() else None

    drugs_summary = input("Drugs summary (optional): ").strip() or None
    notes = input("Notes (optional): ").strip() or None

    try:
        exp_id = create_experiment(
            name=name,
            min_mice=min_mice,
            cells_per_mouse=cells_per_mouse,
            drugs_summary=drugs_summary,
            acsf_type_id=acsf_type_id,
            internal_type_id=internal_type_id,
            mouse_strain_id=mouse_strain_id,
            ideal_mouse_age_min=ideal_min,
            ideal_mouse_age_max=ideal_max,
            experiment_for_person_id=int(person_id),
            project_id=int(project_id),
            notes=notes
        )
        print(f"Experiment created with ID {exp_id}.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# UPDATE EXPERIMENT (Hybrid)
# ---------------------------------------------------------
def update_experiment_interactive():
    exp_id = input("Enter experiment ID to update: ").strip()
    if not exp_id.isdigit():
        print("Invalid ID.")
        return

    exp_id = int(exp_id)
    exp = get_experiment_by_id(exp_id)
    if exp is None:
        print("Experiment not found.")
        return

    print("\nLeave fields blank to keep current values.\n")

    name = input(f"Name [{exp['name']}]: ").strip() or exp['name']

    print("\nAvailable projects:")
    list_projects()
    project_id = input(f"Project ID [{exp['project_id']}]: ").strip() or exp['project_id']

    print("\nAvailable experimenters:")
    list_people()
    person_id = input(f"Person ID [{exp['experiment_for_person_id']}]: ").strip() or exp['experiment_for_person_id']

    min_mice = input(f"Min mice [{exp['min_mice']}]: ").strip() or exp['min_mice']
    min_mice = int(min_mice) if str(min_mice).isdigit() else None

    cells_per_mouse = input(f"Cells per mouse [{exp['cells_per_mouse']}]: ").strip() or exp['cells_per_mouse']
    cells_per_mouse = int(cells_per_mouse) if str(cells_per_mouse).isdigit() else None

    print("\nAvailable mouse strains:")
    list_mouse_strains()
    mouse_strain_id = input(f"Mouse strain ID [{exp['mouse_strain_id']}]: ").strip() or exp['mouse_strain_id']

    print("\nAvailable ACSF types:")
    list_acsf_types()
    acsf_type_id = input(f"ACSF type ID [{exp['acsf_type_id']}]: ").strip() or exp['acsf_type_id']

    print("\nAvailable internal types:")
    list_internal_types()
    internal_type_id = input(f"Internal type ID [{exp['internal_type_id']}]: ").strip() or exp['internal_type_id']

    ideal_min = input(f"Ideal age MIN [{exp['ideal_mouse_age_min']}]: ").strip() or exp['ideal_mouse_age_min']
    ideal_min = int(ideal_min) if str(ideal_min).isdigit() else None

    ideal_max = input(f"Ideal age MAX [{exp['ideal_mouse_age_max']}]: ").strip() or exp['ideal_mouse_age_max']
    ideal_max = int(ideal_max) if str(ideal_max).isdigit() else None

    drugs_summary = input(f"Drugs summary [{exp['drugs_summary']}]: ").strip() or exp['drugs_summary']
    notes = input(f"Notes [{exp['notes']}]: ").strip() or exp['notes']

    try:
        update_experiment_partial(
            exp_id,
            name=name,
            min_mice=min_mice,
            cells_per_mouse=cells_per_mouse,
            drugs_summary=drugs_summary,
            acsf_type_id=int(acsf_type_id) if acsf_type_id else None,
            internal_type_id=int(internal_type_id) if internal_type_id else None,
            mouse_strain_id=int(mouse_strain_id) if mouse_strain_id else None,
            ideal_mouse_age_min=ideal_min,
            ideal_mouse_age_max=ideal_max,
            experiment_for_person_id=int(person_id),
            project_id=int(project_id),
            notes=notes
        )
        print("Experiment updated.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# DELETE EXPERIMENT
# ---------------------------------------------------------
def delete_experiment_interactive_prompt():
    exp_id = input("Enter experiment ID to delete: ").strip()
    if not exp_id.isdigit():
        print("Invalid ID.")
        return

    delete_experiment_interactive(int(exp_id))




# ---------------------------------------------------------
# IMPORTS FOR MICE
# ---------------------------------------------------------
from db.mice_crud import (
    list_mice,
    get_mouse_by_id,
    create_mouse,
    update_mouse_partial,
    delete_mouse_interactive
)

from db.experiments_crud import list_experiments
from db.mouse_strains_crud import list_mouse_strains


# ---------------------------------------------------------
# IMPORTS FOR MICE
# ---------------------------------------------------------
from db.mice_crud import (
    list_mice,
    get_mouse_by_id,
    create_mouse,
    update_mouse_partial,
    delete_mouse_interactive
)

from db.experiments_crud import list_experiments
from db.mouse_strains_crud import list_mouse_strains


# ---------------------------------------------------------
# MICE MENU
# ---------------------------------------------------------
def mice_menu():
    while True:
        print("\n=== MICE MENU ===")
        print("1. List all mice")
        print("2. View a mouse")
        print("3. Create a mouse")
        print("4. Update a mouse")
        print("5. Delete a mouse")
        print("6. Back to main menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            list_mice()

        elif choice == "2":
            view_mouse_interactive()

        elif choice == "3":
            create_mouse_interactive()

        elif choice == "4":
            update_mouse_interactive()

        elif choice == "5":
            delete_mouse_interactive_prompt()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")


# ---------------------------------------------------------
# VIEW MOUSE
# ---------------------------------------------------------
def view_mouse_interactive():
    mouse_id = input("Enter mouse ID: ").strip()
    if not mouse_id.isdigit():
        print("Invalid ID.")
        return

    mouse = get_mouse_by_id(int(mouse_id))
    if mouse is None:
        print("Mouse not found.")
        return

    print("\n=== MOUSE DETAILS ===")
    for key, value in mouse.items():
        print(f"{key}: {value}")


# ---------------------------------------------------------
# CREATE MOUSE (Hybrid, user enters mouse_id_code)
# ---------------------------------------------------------
def create_mouse_interactive():
    print("\n=== CREATE MOUSE ===")

    print("\nAvailable experiments:")
    list_experiments()
    experiment_id = input("Experiment ID: ").strip()
    if not experiment_id.isdigit():
        print("Invalid experiment ID.")
        return

    print("\nAvailable mouse strains:")
    list_mouse_strains()
    strain_id = input("Strain ID: ").strip()
    if not strain_id.isdigit():
        print("Invalid strain ID.")
        return

    mouse_id_code = input("Mouse ID code (e.g., A1, M123): ").strip()
    if not mouse_id_code:
        print("Mouse ID code is required.")
        return

    sex = input("Sex (M/F): ").strip().upper()
    if sex not in ("M", "F"):
        print("Invalid sex. Must be M or F.")
        return

    dob = input("Date of birth (YYYY-MM-DD): ").strip()
    if not dob:
        print("DOB is required.")
        return

    virus_injected = input("Virus injected? (yes/no): ").strip().lower()
    if virus_injected not in ("yes", "no"):
        print("Invalid input. Must be yes or no.")
        return

    if virus_injected == "yes":
        virus_name = input("Virus name: ").strip()
        virus_date = input("Virus injection date (YYYY-MM-DD): ").strip()
    else:
        virus_name = None
        virus_date = None

    notes = input("Notes (optional): ").strip() or None

    try:
        mouse_id = create_mouse(
            experiment_id=int(experiment_id),
            mouse_id_code=mouse_id_code,
            strain_id=int(strain_id),
            sex=sex,
            dob=dob,
            virus_injected=virus_injected,
            virus_name=virus_name,
            virus_injection_date=virus_date,
            notes=notes
        )
        print(f"Mouse created with ID {mouse_id}.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# UPDATE MOUSE (Hybrid)
# ---------------------------------------------------------
def update_mouse_interactive():
    mouse_id = input("Enter mouse ID to update: ").strip()
    if not mouse_id.isdigit():
        print("Invalid ID.")
        return

    mouse_id = int(mouse_id)
    mouse = get_mouse_by_id(mouse_id)
    if mouse is None:
        print("Mouse not found.")
        return

    print("\nLeave fields blank to keep current values.\n")

    print("\nAvailable experiments:")
    list_experiments()
    experiment_id = input(f"Experiment ID [{mouse['experiment_id']}]: ").strip() or mouse['experiment_id']

    print("\nAvailable mouse strains:")
    list_mouse_strains()
    strain_id = input(f"Strain ID [{mouse['strain_id']}]: ").strip() or mouse['strain_id']

    mouse_id_code = input(f"Mouse ID code [{mouse['mouse_id_code']}]: ").strip() or mouse['mouse_id_code']

    sex = input(f"Sex [{mouse['sex']}]: ").strip().upper() or mouse['sex']
    dob = input(f"DOB [{mouse['dob']}]: ").strip() or mouse['dob']

    virus_injected = input(f"Virus injected? (yes/no) [{mouse['virus_injected']}]: ").strip().lower()
    if virus_injected == "":
        virus_injected = mouse["virus_injected"]
        virus_name = mouse["virus_name"]
        virus_date = mouse["virus_injection_date"]
    elif virus_injected == "yes":
        virus_name = input(f"Virus name [{mouse['virus_name']}]: ").strip() or mouse['virus_name']
        virus_date = input(f"Virus injection date [{mouse['virus_injection_date']}]: ").strip() or mouse['virus_injection_date']
    else:
        virus_name = None
        virus_date = None

    notes = input(f"Notes [{mouse['notes']}]: ").strip() or mouse['notes']

    try:
        update_mouse_partial(
            mouse_id,
            experiment_id=int(experiment_id),
            strain_id=int(strain_id),
            mouse_id_code=mouse_id_code,
            sex=sex,
            dob=dob,
            virus_injected=virus_injected,
            virus_name=virus_name,
            virus_injection_date=virus_date,
            notes=notes
        )
        print("Mouse updated.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# DELETE MOUSE
# ---------------------------------------------------------
def delete_mouse_interactive_prompt():
    mouse_id = input("Enter mouse ID to delete: ").strip()
    if not mouse_id.isdigit():
        print("Invalid ID.")
        return

    delete_mouse_interactive(int(mouse_id))


# ---------------------------------------------------------
# IMPORTS FOR CELLS
# ---------------------------------------------------------
from db.cells_crud import (
    list_cells,
    get_cell_by_id,
    create_cell,
    update_cell_partial,
    delete_cell_interactive
)

from db.mice_crud import list_mice
from db.experiments_crud import list_experiments


# ---------------------------------------------------------
# CELLS MENU
# ---------------------------------------------------------
def cells_menu():
    while True:
        print("\n=== CELLS MENU ===")
        print("1. List all cells")
        print("2. View a cell")
        print("3. Create a cell")
        print("4. Update a cell")
        print("5. Delete a cell")
        print("6. Back to main menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            list_cells()

        elif choice == "2":
            view_cell_interactive()

        elif choice == "3":
            create_cell_interactive()

        elif choice == "4":
            update_cell_interactive()

        elif choice == "5":
            delete_cell_interactive_prompt()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")


# ---------------------------------------------------------
# VIEW CELL
# ---------------------------------------------------------
def view_cell_interactive():
    cell_id = input("Enter cell ID: ").strip()
    if not cell_id.isdigit():
        print("Invalid ID.")
        return

    cell = get_cell_by_id(int(cell_id))
    if cell is None:
        print("Cell not found.")
        return

    print("\n=== CELL DETAILS ===")
    for key, value in cell.items():
        print(f"{key}: {value}")


# ---------------------------------------------------------
# CREATE CELL (Hybrid)
# ---------------------------------------------------------
def create_cell_interactive():
    print("\n=== CREATE CELL ===")

    print("\nAvailable experiments:")
    list_experiments()
    experiment_id = input("Experiment ID: ").strip()
    if not experiment_id.isdigit():
        print("Invalid experiment ID.")
        return

    print("\nAvailable mice for this experiment:")
    list_mice()
    mouse_id = input("Mouse ID: ").strip()
    if not mouse_id.isdigit():
        print("Invalid mouse ID.")
        return

    cell_number = input("Cell number (e.g., 1, 2, 3): ").strip()
    if not cell_number.isdigit():
        print("Invalid cell number.")
        return

    recording_type = input("Recording type (e.g., whole-cell, cell-attached): ").strip() or None
    notes = input("Notes (optional): ").strip() or None

    try:
        cell_id = create_cell(
            mouse_id=int(mouse_id),
            cell_number=int(cell_number),
            recording_type=recording_type,
            notes=notes
        )
        print(f"Cell created with ID {cell_id}.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# UPDATE CELL (Hybrid)
# ---------------------------------------------------------
def update_cell_interactive():
    cell_id = input("Enter cell ID to update: ").strip()
    if not cell_id.isdigit():
        print("Invalid ID.")
        return

    cell_id = int(cell_id)
    cell = get_cell_by_id(cell_id)
    if cell is None:
        print("Cell not found.")
        return

    print("\nLeave fields blank to keep current values.\n")

    print("\nAvailable mice:")
    list_mice()
    mouse_id = input(f"Mouse ID [{cell['mouse_id']}]: ").strip() or cell['mouse_id']

    cell_number = input(f"Cell number [{cell['cell_number']}]: ").strip() or cell['cell_number']
    recording_type = input(f"Recording type [{cell['recording_type']}]: ").strip() or cell['recording_type']
    notes = input(f"Notes [{cell['notes']}]: ").strip() or cell['notes']

    try:
        update_cell_partial(
            cell_id,
            mouse_id=int(mouse_id),
            cell_number=int(cell_number),
            recording_type=recording_type,
            notes=notes
        )
        print("Cell updated.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# DELETE CELL
# ---------------------------------------------------------
def delete_cell_interactive_prompt():
    cell_id = input("Enter cell ID to delete: ").strip()
    if not cell_id.isdigit():
        print("Invalid ID.")
        return

    delete_cell_interactive(int(cell_id))



# ---------------------------------------------------------
# IMPORTS FOR PEOPLE
# ---------------------------------------------------------
from db.people_crud import (
    list_people,
    get_person_by_id,
    create_person,
    update_person_partial,
    delete_person_interactive
)


# ---------------------------------------------------------
# PEOPLE MENU
# ---------------------------------------------------------
def people_menu():
    while True:
        print("\n=== PEOPLE MENU ===")
        print("1. List all people")
        print("2. View a person")
        print("3. Create a person")
        print("4. Update a person")
        print("5. Delete a person")
        print("6. Back to main menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            list_people()

        elif choice == "2":
            view_person_interactive()

        elif choice == "3":
            create_person_interactive()

        elif choice == "4":
            update_person_interactive()

        elif choice == "5":
            delete_person_interactive_prompt()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")


# ---------------------------------------------------------
# VIEW PERSON
# ---------------------------------------------------------
def view_person_interactive():
    person_id = input("Enter person ID: ").strip()
    if not person_id.isdigit():
        print("Invalid ID.")
        return

    person = get_person_by_id(int(person_id))
    if person is None:
        print("Person not found.")
        return

    print("\n=== PERSON DETAILS ===")
    for key, value in person.items():
        print(f"{key}: {value}")


# ---------------------------------------------------------
# CREATE PERSON
# ---------------------------------------------------------
def create_person_interactive():
    print("\n=== CREATE PERSON ===")

    name = input("Name: ").strip()
    email = input("Email (optional): ").strip() or None
    role = input("Role (optional): ").strip() or None
    notes = input("Notes (optional): ").strip() or None

    try:
        person_id = create_person(
            name=name,
            email=email,
            role=role,
            notes=notes
        )
        print(f"Person created with ID {person_id}.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# UPDATE PERSON
# ---------------------------------------------------------
def update_person_interactive():
    person_id = input("Enter person ID to update: ").strip()
    if not person_id.isdigit():
        print("Invalid ID.")
        return

    person_id = int(person_id)
    person = get_person_by_id(person_id)
    if person is None:
        print("Person not found.")
        return

    print("\nLeave fields blank to keep current values.\n")

    name = input(f"Name [{person['name']}]: ").strip() or person['name']
    email = input(f"Email [{person['email']}]: ").strip() or person['email']
    role = input(f"Role [{person['role']}]: ").strip() or person['role']
    notes = input(f"Notes [{person['notes']}]: ").strip() or person['notes']

    try:
        update_person_partial(
            person_id,
            name=name,
            email=email,
            role=role,
            notes=notes
        )
        print("Person updated.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# DELETE PERSON
# ---------------------------------------------------------
def delete_person_interactive_prompt():
    person_id = input("Enter person ID to delete: ").strip()
    if not person_id.isdigit():
        print("Invalid ID.")
        return

    delete_person_interactive(int(person_id))

# ---------------------------------------------------------
# IMPORTS FOR DRUGS
# ---------------------------------------------------------
from db.drugs_crud import (
    list_drugs,
    get_drug_by_id,
    create_drug,
    update_drug_partial,
    delete_drug_interactive
)


# ---------------------------------------------------------
# DRUGS MENU
# ---------------------------------------------------------
def drugs_menu():
    while True:
        print("\n=== DRUGS MENU ===")
        print("1. List all drugs")
        print("2. View a drug")
        print("3. Create a drug")
        print("4. Update a drug")
        print("5. Delete a drug")
        print("6. Back to main menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            list_drugs()

        elif choice == "2":
            view_drug_interactive()

        elif choice == "3":
            create_drug_interactive()

        elif choice == "4":
            update_drug_interactive()

        elif choice == "5":
            delete_drug_interactive_prompt()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")


# ---------------------------------------------------------
# VIEW DRUG
# ---------------------------------------------------------
def view_drug_interactive():
    drug_id = input("Enter drug ID: ").strip()
    if not drug_id.isdigit():
        print("Invalid ID.")
        return

    drug = get_drug_by_id(int(drug_id))
    if drug is None:
        print("Drug not found.")
        return

    print("\n=== DRUG DETAILS ===")
    for key, value in drug.items():
        print(f"{key}: {value}")


# ---------------------------------------------------------
# CREATE DRUG
# ---------------------------------------------------------
def create_drug_interactive():
    print("\n=== CREATE DRUG ===")

    name = input("Drug name: ").strip()
    stock_conc = input("Stock concentration (e.g., 10 mM): ").strip()
    vendor = input("Vendor (optional): ").strip() or None

    aliquoted = input("Aliquoted? (yes/no): ").strip().lower()
    if aliquoted == "yes":
        aliquoted = True
        aliquot_date = input("Aliquot date (YYYY-MM-DD): ").strip()
        aliquot_volume = input("Aliquot volume (e.g., 50 µL): ").strip()
    else:
        aliquoted = False
        aliquot_date = None
        aliquot_volume = None

    notes = input("Notes (optional): ").strip() or None

    try:
        drug_id = create_drug(
            name=name,
            stock_concentration=stock_conc,
            vendor=vendor,
            aliquoted=aliquoted,
            aliquot_date=aliquot_date,
            aliquot_volume=aliquot_volume,
            notes=notes
        )
        print(f"Drug created with ID {drug_id}.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# UPDATE DRUG
# ---------------------------------------------------------
def update_drug_interactive():
    drug_id = input("Enter drug ID to update: ").strip()
    if not drug_id.isdigit():
        print("Invalid ID.")
        return

    drug_id = int(drug_id)
    drug = get_drug_by_id(drug_id)
    if drug is None:
        print("Drug not found.")
        return

    print("\nLeave fields blank to keep current values.\n")

    name = input(f"Name [{drug['name']}]: ").strip() or drug['name']
    stock_conc = input(f"Stock concentration [{drug['stock_concentration']}]: ").strip() or drug['stock_concentration']
    vendor = input(f"Vendor [{drug['vendor']}]: ").strip() or drug['vendor']

    aliquoted_input = input(f"Aliquoted? (yes/no) [{drug['aliquoted']}]: ").strip().lower()
    if aliquoted_input == "":
        aliquoted = drug["aliquoted"]
        aliquot_date = drug["aliquot_date"]
        aliquot_volume = drug["aliquot_volume"]
    elif aliquoted_input == "yes":
        aliquoted = True
        aliquot_date = input(f"Aliquot date [{drug['aliquot_date']}]: ").strip() or drug['aliquot_date']
        aliquot_volume = input(f"Aliquot volume [{drug['aliquot_volume']}]: ").strip() or drug['aliquot_volume']
    else:
        aliquoted = False
        aliquot_date = None
        aliquot_volume = None

    notes = input(f"Notes [{drug['notes']}]: ").strip() or drug['notes']

    try:
        update_drug_partial(
            drug_id,
            name=name,
            stock_concentration=stock_conc,
            vendor=vendor,
            aliquoted=aliquoted,
            aliquot_date=aliquot_date,
            aliquot_volume=aliquot_volume,
            notes=notes
        )
        print("Drug updated.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# DELETE DRUG
# ---------------------------------------------------------
def delete_drug_interactive_prompt():
    drug_id = input("Enter drug ID to delete: ").strip()
    if not drug_id.isdigit():
        print("Invalid ID.")
        return

    delete_drug_interactive(int(drug_id))
# ---------------------------------------------------------
# IMPORTS FOR ACSF TYPES
# ---------------------------------------------------------
from db.acsf_types_crud import (
    list_acsf_types,
    get_acsf_type_by_id,
    create_acsf_type,
    update_acsf_type_partial,
    delete_acsf_type_interactive
)


# ---------------------------------------------------------
# ACSF TYPES MENU
# ---------------------------------------------------------
def acsf_menu():
    while True:
        print("\n=== ACSF TYPES MENU ===")
        print("1. List all ACSF types")
        print("2. View an ACSF type")
        print("3. Create an ACSF type")
        print("4. Update an ACSF type")
        print("5. Delete an ACSF type")
        print("6. Back to main menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            list_acsf_types()

        elif choice == "2":
            view_acsf_type_interactive()

        elif choice == "3":
            create_acsf_type_interactive()

        elif choice == "4":
            update_acsf_type_interactive()

        elif choice == "5":
            delete_acsf_type_interactive_prompt()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")


# ---------------------------------------------------------
# VIEW ACSF TYPE
# ---------------------------------------------------------
def view_acsf_type_interactive():
    acsf_id = input("Enter ACSF type ID: ").strip()
    if not acsf_id.isdigit():
        print("Invalid ID.")
        return

    acsf = get_acsf_type_by_id(int(acsf_id))
    if acsf is None:
        print("ACSF type not found.")
        return

    print("\n=== ACSF TYPE DETAILS ===")
    for key, value in acsf.items():
        print(f"{key}: {value}")


# ---------------------------------------------------------
# CREATE ACSF TYPE
# ---------------------------------------------------------
def create_acsf_type_interactive():
    print("\n=== CREATE ACSF TYPE ===")

    name = input("ACSF name: ").strip()
    reg_or_mod = input("Type (regular / modified): ").strip()
    notes = input("Notes (optional): ").strip() or None

    try:
        acsf_id = create_acsf_type(
            name=name,
            reg_or_mod=reg_or_mod,
            notes=notes
        )
        print(f"ACSF type created with ID {acsf_id}.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# UPDATE ACSF TYPE
# ---------------------------------------------------------
def update_acsf_type_interactive():
    acsf_id = input("Enter ACSF type ID to update: ").strip()
    if not acsf_id.isdigit():
        print("Invalid ID.")
        return

    acsf_id = int(acsf_id)
    acsf = get_acsf_type_by_id(acsf_id)
    if acsf is None:
        print("ACSF type not found.")
        return

    print("\nLeave fields blank to keep current values.\n")

    name = input(f"Name [{acsf['name']}]: ").strip() or acsf['name']
    reg_or_mod = input(f"Type (regular/modified) [{acsf['reg_or_mod']}]: ").strip() or acsf['reg_or_mod']
    notes = input(f"Notes [{acsf['notes']}]: ").strip() or acsf['notes']

    try:
        update_acsf_type_partial(
            acsf_id,
            name=name,
            reg_or_mod=reg_or_mod,
            notes=notes
        )
        print("ACSF type updated.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# DELETE ACSF TYPE
# ---------------------------------------------------------
def delete_acsf_type_interactive_prompt():
    acsf_id = input("Enter ACSF type ID to delete: ").strip()
    if not acsf_id.isdigit():
        print("Invalid ID.")
        return

    delete_acsf_type_interactive(int(acsf_id))

# ---------------------------------------------------------
# IMPORTS FOR INTERNAL TYPES
# ---------------------------------------------------------
from db.internal_types_crud import (
    list_internal_types,
    get_internal_type_by_id,
    create_internal_type,
    update_internal_type_partial,
    delete_internal_type_interactive
)


# ---------------------------------------------------------
# INTERNAL TYPES MENU
# ---------------------------------------------------------
def internal_menu():
    while True:
        print("\n=== INTERNAL SOLUTION TYPES MENU ===")
        print("1. List all internal types")
        print("2. View an internal type")
        print("3. Create an internal type")
        print("4. Update an internal type")
        print("5. Delete an internal type")
        print("6. Back to main menu")

        choice = input("Select an option: ").strip()

        if choice == "1":
            list_internal_types()

        elif choice == "2":
            view_internal_type_interactive()

        elif choice == "3":
            create_internal_type_interactive()

        elif choice == "4":
            update_internal_type_interactive()

        elif choice == "5":
            delete_internal_type_interactive_prompt()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Try again.")


# ---------------------------------------------------------
# VIEW INTERNAL TYPE
# ---------------------------------------------------------
def view_internal_type_interactive():
    internal_id = input("Enter internal type ID: ").strip()
    if not internal_id.isdigit():
        print("Invalid ID.")
        return

    internal = get_internal_type_by_id(int(internal_id))
    if internal is None:
        print("Internal type not found.")
        return

    print("\n=== INTERNAL TYPE DETAILS ===")
    for key, value in internal.items():
        print(f"{key}: {value}")


# ---------------------------------------------------------
# CREATE INTERNAL TYPE
# ---------------------------------------------------------
def create_internal_type_interactive():
    print("\n=== CREATE INTERNAL TYPE ===")

    name = input("Internal solution name: ").strip()
    notes = input("Notes (optional): ").strip() or None

    try:
        internal_id = create_internal_type(
            name=name,
            notes=notes
        )
        print(f"Internal type created with ID {internal_id}.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# UPDATE INTERNAL TYPE
# ---------------------------------------------------------
def update_internal_type_interactive():
    internal_id = input("Enter internal type ID to update: ").strip()
    if not internal_id.isdigit():
        print("Invalid ID.")
        return

    internal_id = int(internal_id)
    internal = get_internal_type_by_id(internal_id)
    if internal is None:
        print("Internal type not found.")
        return

    print("\nLeave fields blank to keep current values.\n")

    name = input(f"Name [{internal['name']}]: ").strip() or internal['name']
    notes = input(f"Notes [{internal['notes']}]: ").strip() or internal['notes']

    try:
        update_internal_type_partial(
            internal_id,
            name=name,
            notes=notes
        )
        print("Internal type updated.")
    except Exception as e:
        print(f"Error: {e}")


# ---------------------------------------------------------
# DELETE INTERNAL TYPE
# ---------------------------------------------------------
def delete_internal_type_interactive_prompt():
    internal_id = input("Enter internal type ID to delete: ").strip()
    if not internal_id.isdigit():
        print("Invalid ID.")
        return

    delete_internal_type_interactive(int(internal_id))




# ---------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------
if __name__ == "__main__":
    main_menu()



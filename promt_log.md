Used Copilot for the entire project
1. "I want to make an experiment tracker 
small app that uses a SQLite database to store, 
retrieve, update, and delete data. This is for a
 neuurosceince lab in which different experiments 
 have different requirement. This is specifically for 
 electrophysiology experiments. The app should serve 
 as a master planner for all experiment. Each experiment has: mininum number of mice, number of cells per mice, drugs needed for the experiment, type of ASCF , type of internal, the mouse strain, ideal mouse age, person I am doing the experiment for, project the data will be used for. Before writing code, give me a suggested database schema"
 2. "In the experiments, add drugs, and give me full schemas again
 3. "First, give me the full python code just with the schema implemented that I can run and visualize with a free tool like DB Browser for SQLite to open my .db file and see my tables and data visually."
 4. "I want a better name for the python file"
 5. "yes, and I should  schema implemented that I can run and visualize with a free tool like DB Browser for SQLite to open my .db file and see my tables and data visually"
 6. "How would visualize this in DB Browser for SQLite. I have it downloaded on my mac"
 7. "I don’t know about that I opened my project thorugh github desktop"
 8. "Ok, now we will implement CRUD one by one. I want to learn how to create these functions as we implement these"
 9. "Option A — “Teach me everything step-by-step”"
 10. "First, the the delete and update implemented like this: Update: Let the user pick a record (by id or by selecting from a list) and change one or more of its fields.
 Delete: Let the user remove a record by id. ask for confirmation before deleting"
 11. "give me the complete dp_utils.py we wrote"
 12. "CRUD for the mice table"
 13. "can we create different files for each of the CRUDs and retain the original schema?"
14. "I am using VScode, does this mean that I have to first create a folder called db"
15. "Tell me more about __init__.py"
16. "generate the full mice_crud.py next, With partial updates, With delete confirmation"
17. "cells_crud.py should depend on experiment requirement"
18. "Update mice_crud.py so that it also has mouse DOB"
19."Update your schema file to include DOB. Add automatic age calculation from DOB
So you don’t manually enter age_days. Add validation (DOB must be in the past)
Useful for preventing mistakes.
19. "cells_crud.py. This needs project, people, experiment, mice strain, sex, mouse id, mouse dob, mouse age."
20. "I forgot, sometimes mice are injected with virus. This needs to be added to the mouse info if are injected. so we need name of virus, and a date injected, and y/n to show if they were indeed injected. we may need to update the schema and mice_crud.py"
21. "we can continue with our crud implementation"
22. "Still to implement
drugs_crud.py .Simple table — name, stock concentration, vendor, y/n aliqouted, date aliqouted, volume per aliqoute, notes. Update schema, and give me crude file"
23. experiment_drugs_crud.py: experiment drug is for, name of drug, stock concencentration, desired concentration for experiment, volume of stock drug to add to ACSF for desired concentration, notes. Update schema and give me crud file"
24. "acsf_types_crud.py: type name (reg/mod), drugs and [] of each drug. update schema, and give me full acsf_types_crud.py"
25. "paste both acsf_types and acsf_type_drugs?"
26. "internal_types_crud.py"
27. "mouse_strains_crud.py"
28. "people_crud.py"
29. "projects_crud.py" 
30. "give me the updated schema for the previous two crude"
31. "show dependency diagram"
32. "How should I go about building an interface for the user to edit, and display all of this"
33. "Start with a Command‑Line Menu System, step by step"
34. "Flesh out projects_menu() fully"
35. "give all the crude for project at once"
36. "ok I'm confused starts again from the top, I want to build a command line interface"
37. "okay, give me all the cli for project at once and tell me where to paste"
38. "Experiments, and exactly where to paste"
39. "Cells"
40. "People"
41. "now Drugs cli"
42. "ACSF Types"
43. "Internal Types"
44. "now I want to test the interface, and also test that crud is implemented"
45. "how do I run this in vs code"
46. pasted error
47. "Audit all my CRUD modules."
48. Sent Copilot db/projects_crud.py
49. Sent Copilot db/people_crud.py
50. Sent Copilot db/experiments_crud.py
51. Sent Copilot db/mice_crud.py
52. Sent Copilot db/cells_crud.py
53. "tell me which file to paste these"
54. Pasted main.py
55. "Option C — Hybrid
Ask for the important fields, And leave the rest optional."
56. "Option 2 — Ask the user to enter mouse_id_code"
57. "Part 2 — Mice CLI (Hybrid, with user‑entered mouse_id_code)"
58. "— Cells CLI."
59. "I wants to check that the rest of the CLI functions match the original CRUD"
60. "elect an option: 3
Menu not implemented yet."
61. Pasted main menu section main.py.
62. "List all experiments isn't working"
63. "how should I run this? from db.connection import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("PRAGMA table_info(experiments);")
print(cur.fetchall())
conn.close()"
64. Pasted result from previous query
65. Pasted  list_experiments() 
66. Pasted get_all_experiments()
67. "what is this? Python REPL:"
68. "List all projects. View a project isn't working. are we commiting the changes to the database?
69. Pasted full projects_crud.py
70. "fix the cli for project: this is what I have:" Then pasted code for project menu cli.
71. "Enter project ID: TEST
Invalid ID. when I want to view a project"
72. Change id INTEGER PRIMARY KEY → id TEXT PRIMARY KEY

Update all CRUD functions

Update all foreign keys

Update all CLI menus"
73. "Option A — User enters IDs manually"
74. "IDs to be:
A1 — Completely free‑form text"
75. "NO, wipe and start fresh"
76. "before I change all of that, its not even promting me to enter the project id"
77. "nevermind, I want to uodate view project so that I can search by all the other features: def view_project_interactive():
    project_id = input("Enter project ID: ").strip()
    if not project_id.isdigit():
        print("Invalid ID.")
        return

    project = get_project_by_id(int(project_id))
    if project is None:
        print("Project not found.")
        return

    print("\n=== PROJECT DETAILS ===")
    for key, value in project.items():
        print(f"{key}: {value}")"
    

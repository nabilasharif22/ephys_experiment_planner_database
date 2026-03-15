**Project Description**

This project is a modular, Python‑based Laboratory Information Management System (LIMS) designed to support the complex workflows of electrophysiology research. It provides a structured, reliable way to organize every layer of experimental metadata—from high‑level projects and personnel to mice, cells, drugs, ACSF/internal solutions, and experiment configurations. The system is built around SQLite database. Each entity in the system is managed through its own dedicated CRUD module. Command-line interface is used to search the database.



**Project Structure**

ephys_experiment_planner_database/
│
├── main.py                     # CLI entry point
│
├── db/
│   ├── connection.py           # SQLite connection helper
│   ├── initialize_database.py  # Creates tables (TEXT primary keys)
│   ├── projects_crud.py
│   ├── experiments_crud.py
│   ├── mice_crud.py
│   ├── cells_crud.py
│   ├── drugs_crud.py
│   ├── acsf_types_crud.py
│   ├── internal_types_crud.py
│   ├── mouse_strains_crud.py
│   └── people_crud.py
│
└── README.md


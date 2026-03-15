import sqlite3

def create_schema():
    conn = sqlite3.connect("experiments.db")
    cur = conn.cursor()

    # Enable foreign key constraints
    cur.execute("PRAGMA foreign_keys = ON;")

    # 1. experiments
    cur.execute("""
    CREATE TABLE IF NOT EXISTS experiments (
        id INTEGER PRIMARY KEY,
        name TEXT,
        min_mice INTEGER,
        cells_per_mouse INTEGER,
        drugs_summary TEXT,
        acsf_type_id INTEGER,
        internal_type_id INTEGER,
        mouse_strain_id INTEGER,
        ideal_mouse_age_min INTEGER,
        ideal_mouse_age_max INTEGER,
        experiment_for_person_id INTEGER,
        project_id INTEGER,
        notes TEXT,
        FOREIGN KEY (acsf_type_id) REFERENCES acsf_types(id),
        FOREIGN KEY (internal_type_id) REFERENCES internal_types(id),
        FOREIGN KEY (mouse_strain_id) REFERENCES mouse_strains(id),
        FOREIGN KEY (experiment_for_person_id) REFERENCES people(id),
        FOREIGN KEY (project_id) REFERENCES projects(id)
    );
    """)

    # 2. mice
    cur.execute("""
    CREATE TABLE IF NOT EXISTS mice (
        id INTEGER PRIMARY KEY,
        experiment_id INTEGER,
        mouse_id_code TEXT,
        strain_id INTEGER,
        age_days INTEGER,
        sex TEXT,
        notes TEXT,
        FOREIGN KEY (experiment_id) REFERENCES experiments(id),
        FOREIGN KEY (strain_id) REFERENCES mouse_strains(id)
    );
    """)

    # 3. cells
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cells (
        id INTEGER PRIMARY KEY,
        mouse_id INTEGER,
        cell_number INTEGER,
        recording_type TEXT,
        notes TEXT,
        FOREIGN KEY (mouse_id) REFERENCES mice(id)
    );
    """)

    # 4. drugs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS drugs (
        id INTEGER PRIMARY KEY,
        name TEXT,
        stock_concentration TEXT,
        notes TEXT
    );
    """)

    # 5. experiment_drugs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS experiment_drugs (
        id INTEGER PRIMARY KEY,
        experiment_id INTEGER,
        drug_id INTEGER,
        working_concentration TEXT,
        application_method TEXT,
        FOREIGN KEY (experiment_id) REFERENCES experiments(id),
        FOREIGN KEY (drug_id) REFERENCES drugs(id)
    );
    """)

    # 6. acsf_types
    cur.execute("""
    CREATE TABLE IF NOT EXISTS acsf_types (
        id INTEGER PRIMARY KEY,
        name TEXT,
        recipe TEXT
    );
    """)

    # 7. internal_types
    cur.execute("""
    CREATE TABLE IF NOT EXISTS internal_types (
        id INTEGER PRIMARY KEY,
        name TEXT,
        recipe TEXT
    );
    """)

    # 8. mouse_strains
    cur.execute("""
    CREATE TABLE IF NOT EXISTS mouse_strains (
        id INTEGER PRIMARY KEY,
        name TEXT,
        notes TEXT
    );
    """)

    # 9. people
    cur.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT,
        email TEXT
    );
    """)

    # 10. projects
    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT
    );
    """)

    conn.commit()
    conn.close()
    print("Database 'experiments.db' created successfully with full schema.")

if __name__ == "__main__":
    create_schema()

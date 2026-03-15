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
        dob TEXT,
        virus_injected TEXT,            -- "yes" or "no"
        virus_name TEXT,                -- optional
        virus_injection_date TEXT,      -- optional
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

    # drugs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS drugs (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        stock_concentration TEXT,
        vendor TEXT,
        aliquoted TEXT,               -- "yes" or "no"
        aliquot_date TEXT,            -- YYYY-MM-DD
        aliquot_volume TEXT,          -- e.g., "50 µL"
        notes TEXT
    );
    """)

    # 5. experiment_drugs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS experiment_drugs (
        id INTEGER PRIMARY KEY,
        experiment_id INTEGER NOT NULL,
        drug_id INTEGER NOT NULL,
        stock_concentration TEXT,          -- from drugs table, but stored here for snapshot
        desired_concentration TEXT,        -- working concentration for this experiment
        volume_to_add TEXT,                -- volume of stock drug to add to ACSF
        notes TEXT,
        FOREIGN KEY (experiment_id) REFERENCES experiments(id),
        FOREIGN KEY (drug_id) REFERENCES drugs(id)
    );
    """)

    # 6 acsf_types and acsf_type_drugs
# ---------------------------------------------------------
# ACSF TYPES
# ---------------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS acsf_types (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,          -- e.g., "regular", "modified", "high Mg", etc.
        notes TEXT
    );
    """)

# ---------------------------------------------------------
# ACSF TYPE DRUGS (many-to-many)
# ---------------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS acsf_type_drugs (
        id INTEGER PRIMARY KEY,
        acsf_type_id INTEGER NOT NULL,
        drug_id INTEGER NOT NULL,
        concentration TEXT,          -- concentration of this drug in this ACSF
        FOREIGN KEY (acsf_type_id) REFERENCES acsf_types(id),
        FOREIGN KEY (drug_id) REFERENCES drugs(id)
    );
    """)


    # 7. internal_types
    # ---------------------------------------------------------
# INTERNAL SOLUTION TYPES
# ---------------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS internal_types (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,          -- e.g., "K-gluconate", "Cs-methanesulfonate"
        notes TEXT
    );
    """)

# ---------------------------------------------------------
# INTERNAL TYPE DRUGS (many-to-many)
# ---------------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS internal_type_drugs (
        id INTEGER PRIMARY KEY,
        internal_type_id INTEGER NOT NULL,
        drug_id INTEGER NOT NULL,
        concentration TEXT,          -- concentration of this drug/additive in the internal
        FOREIGN KEY (internal_type_id) REFERENCES internal_types(id),
        FOREIGN KEY (drug_id) REFERENCES drugs(id)
    );
    """)


    # 8. mouse_strains
    cur.execute("""
    CREATE TABLE IF NOT EXISTS mouse_strains (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,          -- e.g., "C57BL/6J", "Ai9", "PV-Cre", etc.
        genotype TEXT,               -- optional: "Cre/+", "+/+", "flox/+", etc.
        notes TEXT
    );
    """)

    # 9. people
    cur.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,          -- full name of experimenter
        email TEXT,                  -- optional
        role TEXT,                   -- e.g., "PI", "Postdoc", "Graduate Student"
        notes TEXT
    );
    """)

    # 10. projects
    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,          -- project name
        description TEXT,            -- optional
        pi TEXT,                     -- principal investigator or project owner
        start_date TEXT,             -- YYYY-MM-DD
        notes TEXT
    );
    """)
print("Database 'experiments.db' created successfully with full schema.")

if __name__ == "__main__":
    create_schema()

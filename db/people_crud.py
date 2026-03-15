# db/people_crud.py

from db.connection import get_connection


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
def create_person(name, email=None, role=None, notes=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO people (
            name,
            email,
            role,
            notes
        ) VALUES (?, ?, ?, ?);
    """, (name, email, role, notes))

    conn.commit()
    person_id = cur.lastrowid
    conn.close()
    return person_id


# ---------------------------------------------------------
# READ (single)
# ---------------------------------------------------------
def get_person_by_id(person_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            email,
            role,
            notes
        FROM people
        WHERE id = ?;
    """, (person_id,))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "role": row[3],
        "notes": row[4],
    }


# ---------------------------------------------------------
# READ (all)
# ---------------------------------------------------------
def get_all_people():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            name,
            email,
            role,
            notes
        FROM people;
    """)

    rows = cur.fetchall()
    conn.close()

    people = []
    for row in rows:
        people.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "role": row[3],
            "notes": row[4],
        })

    return people


# ---------------------------------------------------------
# LIST (pretty print)
# ---------------------------------------------------------
def list_people():
    people = get_all_people()
    print("\nPeople:")
    for p in people:
        print(
            f"{p['id']}: {p['name']} "
            f"(email={p['email']}, role={p['role']}, notes={p['notes']})"
        )
    return people


# ---------------------------------------------------------
# UPDATE (partial)
# ---------------------------------------------------------
def update_person_partial(person_id, **fields):
    if not fields:
        return 0

    conn = get_connection()
    cur = conn.cursor()

    set_clause = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values())
    values.append(person_id)

    sql = f"UPDATE people SET {set_clause} WHERE id = ?;"

    cur.execute(sql, values)
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected


# ---------------------------------------------------------
# DELETE (with confirmation)
# ---------------------------------------------------------
def delete_person_interactive(person_id):
    person = get_person_by_id(person_id)
    if person is None:
        print("Person not found.")
        return 0

    print("\nYou are about to delete this person:")
    print(f"ID: {person['id']}")
    print(f"Name: {person['name']}")
    print(f"Email: {person['email']}")
    print(f"Role: {person['role']}")
    print(f"Notes: {person['notes']}")

    confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()
    if confirm != "yes":
        print("Deletion cancelled.")
        return 0

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM people WHERE id = ?;", (person_id,))
    conn.commit()
    affected = cur.rowcount
    conn.close()

    if affected:
        print("Person deleted.")
    else:
        print("Deletion failed.")

    return affected

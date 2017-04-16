from user import Users
from db import get_connection 
from update import ensure_calendar_updated

if __name__ == "main":
    conn = get_connection()
    users = Users(conn)
    for person_id in users.get_users():
        print "Updating", person_id
        ensure_calendar_updated(person_id, conn)
    


def format_mot_header(route):
    mot = route["Mot"]
    mot_type = mot.get("Type", "Unknown")
    duration = route.get("Duration", "?")

    if mot_type == "Footpath":
        return f"Footpath ({duration} min)"
    
    name = mot.get()

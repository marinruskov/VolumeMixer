import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)

settings_file_path = resource_path("Settings.xml")
def save_keybinds(session_name, inc_modifier, inc_char, dec_modifier, dec_char):
    if os.path.exists(settings_file_path) and os.path.getsize(settings_file_path) > 0:
        tree = ET.parse(settings_file_path)
        root = tree.getroot()
    else:
        root = ET.Element("Keybinds")

    session_element = root.find(f"./Session[@name='{session_name}']")
    if session_element is None:
        session_element = ET.SubElement(root, "Session", name=session_name)

    inc_element = session_element.find("Increase")
    if inc_element is None:
        inc_element = ET.SubElement(session_element, "Increase")
    inc_element.set("modifier", inc_modifier)
    inc_element.set("character", inc_char)

    dec_element = session_element.find("Decrease")
    if dec_element is None:
        dec_element = ET.SubElement(session_element, "Decrease")
    dec_element.set("modifier", dec_modifier)
    dec_element.set("character", dec_char)

    # Convert the ElementTree to a string
    xml_str = ET.tostring(root, encoding='utf-8')
    # Parse the string using minidom for pretty printing
    parsed_str = minidom.parseString(xml_str)
    pretty_str = parsed_str.toprettyxml(indent="  ")

    # Remove extra blank lines
    pretty_str = "\n".join([line for line in pretty_str.split("\n") if line.strip()])

    # Write the pretty-printed XML to the file
    with open(settings_file_path, "w") as f:
        f.write(pretty_str)

def load_keybinds(session_name):
    if os.path.exists(settings_file_path) and os.path.getsize(settings_file_path) > 0:
        tree = ET.parse(settings_file_path)
        root = tree.getroot()
        session_element = root.find(f"./Session[@name='{session_name}']")
        if session_element is not None:
            inc_element = session_element.find("Increase")
            dec_element = session_element.find("Decrease")
            if inc_element is not None and dec_element is not None:
                return (inc_element.get("modifier"), inc_element.get("character"),
                        dec_element.get("modifier"), dec_element.get("character"))
    return (None, None, None, None)

def delete_keybinds(session_name):
    if os.path.exists(settings_file_path) and os.path.getsize(settings_file_path) > 0:
        tree = ET.parse(settings_file_path)
        root = tree.getroot()
        session_element = root.find(f"./Session[@name='{session_name}']")
        if session_element is not None:
            root.remove(session_element)
            # Convert the ElementTree to a string
            xml_str = ET.tostring(root, encoding='utf-8')
            # Parse the string using minidom for pretty printing
            parsed_str = minidom.parseString(xml_str)
            pretty_str = parsed_str.toprettyxml(indent="  ")

            # Remove extra blank lines
            pretty_str = "\n".join([line for line in pretty_str.split("\n") if line.strip()])

            # Write the pretty-printed XML to the file
            with open(settings_file_path, "w") as f:
                f.write(pretty_str)

def save_increment_value(value):
    if os.path.exists(settings_file_path) and os.path.getsize(settings_file_path) > 0:
        tree = ET.parse(settings_file_path)
        root = tree.getroot()
    else:
        root = ET.Element("Settings")

    increment = root.find("IncrementValue")
    if increment is None:
        increment = ET.SubElement(root, "IncrementValue")
    increment.text = str(value)

    # Convert the ElementTree to a string
    xml_str = ET.tostring(root, encoding='utf-8')
    parsed_str = minidom.parseString(xml_str)
    pretty_str = parsed_str.toprettyxml(indent="  ")
    pretty_str = "\n".join([line for line in pretty_str.split("\n") if line.strip()])

    with open(settings_file_path, "w") as file:
        file.write(pretty_str)

def load_increment_value():
    if os.path.exists(settings_file_path) and os.path.getsize(settings_file_path) > 0:
        try:
            tree = ET.parse(settings_file_path)
            root = tree.getroot()
            increment = root.find("IncrementValue")
            return float(increment.text) if increment is not None else 5.0
        except ET.ParseError:
            return 5.0
    return 5.0

def save_startup_enabled(enabled):
    if os.path.exists(settings_file_path) and os.path.getsize(settings_file_path) > 0:
        tree = ET.parse(settings_file_path)
        root = tree.getroot()
    else:
        root = ET.Element("Settings")

    startup = root.find("StartupEnabled")
    if startup is None:
        startup = ET.SubElement(root, "StartupEnabled")
    startup.text = "true" if enabled else "false"

    xml_str = ET.tostring(root, encoding='utf-8')
    parsed_str = minidom.parseString(xml_str)
    pretty_str = parsed_str.toprettyxml(indent="  ")
    pretty_str = "\n".join([line for line in pretty_str.split("\n") if line.strip()])

    with open(settings_file_path, "w") as file:
        file.write(pretty_str)

def load_startup_enabled():
    if os.path.exists(settings_file_path) and os.path.getsize(settings_file_path) > 0:
        try:
            tree = ET.parse(settings_file_path)
            root = tree.getroot()
            startup = root.find("StartupEnabled")
            return startup.text == "true" if startup is not None else False
        except ET.ParseError:
            return False
    return False
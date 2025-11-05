def generate_crud(model_name, fields):
    """
    Generate a simple in-memory CRUD class for a given model.
    
    Args:
    model_name (str): Name of the model (e.g., 'User').
    fields (list): List of field names (e.g., ['id', 'name', 'email']).
    
    Returns:
    str: The generated Python code as a string.
    """
    # Start with the class definition
    code = f"class {model_name}CRUD:\n"
    code += "    def __init__(self):\n"
    code += "        self.data = []\n"
    code += "        self.next_id = 1\n\n"
    
    # Generate constructor for the model instance
    init_params = ', '.join(fields[1:]) if len(fields) > 1 else ''  # Skip id for params
    init_body = ' = '.join([f + f'"{f.upper()}_DEFAULT"' for f in fields[1:]]) if len(fields) > 1 else ''
    if init_body:
        init_body = f'self.{fields[0]} = self.next_id\nself.next_id += 1\n' + 'self.' + ' = '.join([f + init_body.split(' = ')[1] for f in fields[1:]])
    else:
        init_body = f'self.{fields[0]} = self.next_id\nself.next_id += 1'
    
    code += f"    def create(self, {init_params}):\n"
    code += f"        instance = {model_name}(self.next_id, {', '.join(fields[1:])})\n"
    code += "        self.data.append(instance)\n"
    code += "        return instance\n\n"
    
    # Read all
    code += "    def read_all(self):\n"
    code += "        return self.data[:]\n\n"
    
    # Read by id
    code += "    def read(self, id):\n"
    code += "        for item in self.data:\n"
    code += f"            if item.{fields[0]} == id:\n"
    code += "                return item\n"
    code += "        return None\n\n"
    
    # Update
    update_params = ', '.join(fields)
    code += f"    def update(self, id, {', '.join(fields[1:])}):\n"
    code += f"        instance = self.read(id)\n"
    if len(fields) > 1:
        code += '        '.join([f"instance.{f} = {f}\n" for f in fields[1:]])
    code += "        return instance\n\n"
    
    # Delete
    code += "    def delete(self, id):\n"
    code += "        for i, item in enumerate(self.data):\n"
    code += f"            if item.{fields[0]} == id:\n"
    code += "                del self.data[i]\n"
    code += "                return True\n"
    code += "        return False\n\n"
    
    # Generate a simple model class
    code = f"class {model_name}:\n"
    code += f"    def __init__(self, {', '.join(fields)}):\n"
    for f in fields:
        code += f"        self.{f} = {f}\n"
    code += "\n" + code  # Append the CRUD class after the model
    
    return code

# Example usage
if __name__ == "__main__":
    print(generate_crud('User', ['id', 'name', 'email']))
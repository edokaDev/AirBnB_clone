#!/usr/bin/python3
"""A cmd-line interpreter to handle creation and deletion of objects."""
import cmd
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.state import State
import models


class HBNBCommand(cmd.Cmd):
    """All methods and attributes that will be used in the command line."""

    prompt = '(hbnb) '
    class_list = ["BaseModel", "User", "Place", "State",
                  "City", "Amenity", "Review"]

    def do_quit(self, line):
        """Exit the command line session."""
        return True

    def do_EOF(self, line):
        """Exit the command line session."""
        return True

    def emptyline(self):
        """Do nothing if empty line is parsed."""
        if self.lastcmd:
            self.lastcmd = ""
            self.onecmd(self.lastcmd)

    def do_create(self, line):
        """Create.

        Create an new instance of BaseModel,
        saves it to a json file and prints id.
        """
        if not line:
            print("** class name missing **")
            return

        if line not in HBNBCommand.class_list:
            print("** class doesn't exist **")
            return
        if line in globals() and isinstance(globals()[line], type):
            new_object = globals()[line]()
            print(new_object.id)
            new_object.save()
        else:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Show.

        Print the string representation of an instance
        based on the class name and id.
        """
        if not line:
            print("** class name missing **")
            return

        args = line.split()

        if args[0] not in HBNBCommand.class_list:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        key = '.'.join((args[0], args[1]))

        with open('storage_file.json', 'r', encoding='utf-8') as f:
            objs_dict = json.load(f)

        if key not in objs_dict.keys():
            print("** no instance found ** ")
        else:
            obj_dict = objs_dict[key]
            obj = globals()[args[0]](**obj_dict)
            print(obj)

    def do_destroy(self, line):
        """Delete.

        Delete an instance based on the class name
        and id (saves the changes into the JSON file)
        """
        if not line:
            print("** class name missing **")
            return

        args = line.split()

        if args[0] not in HBNBCommand.class_list:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        key = '.'.join((args[0], args[1]))

        with open('storage_file.json', 'r', encoding='utf-8') as f:
            objs_dict = json.load(f)

        if key not in objs_dict.keys():
            print("** no instance found ** ")
        else:
            del objs_dict[key]
            objs_json = json.dumps(objs_dict)
            with open('storage_file.json', 'w', encoding='utf-8') as f:
                f.write(objs_json)
            models.storage.reload()

    def do_all(self, line):
        """All.

        Print a list of string representations of class instances
        based or not based on the name of class
        Usage: all
               all ClassName
        """
        args = line.split()
        argc = len(args)
        string_list = []

        if argc == 1:
            if args[0] not in HBNBCommand.class_list:
                print("** class doesn't exist **")
                return

        with open("storage_file.json", 'r', encoding='utf-8') as f:
            objs_dict = json.load(f)

        for key in objs_dict.keys():
            if argc == 1:
                if args[0] in key:
                    obj_dict = objs_dict[key]
                    obj_spawn = globals()[args[0]](**obj_dict)
                    string = obj_spawn.__str__()
                    string_list.append(string)
            elif argc == 0:
                obj_dict = objs_dict[key]
                obj_spawn = globals()[obj_dict['__class__']](**obj_dict)
                string = obj_spawn.__str__()
                string_list.append(string)

        if len(string_list) == 0:
            print("** class doesn't exist **")
        else:
            print(string_list)

    def do_update(self, line):
        """Update.

        Update an existing class instance by adding or
        modifying an attribute.
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = line.split()
        argc = len(args)

        if argc < 1:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.class_list:
            print("** class doesn't exist **")
            return

        if argc < 2:
            print("** instance id missing **")
            return

        with open('storage_file.json', 'r', encoding='utf-8') as f:
            objs_dict = json.load(f)

        key = '.'.join((args[0], args[1]))

        keys_list = objs_dict.keys()

        if key not in keys_list:
            print("** no instance found **")
            return

        if argc < 3:
            print("** attribute name missing **")
            return

        if argc < 4:
            print("** value missing **")
            return

        obj_dict = objs_dict[key]
        string = args[3].strip('\'\"')
        obj_spawn = globals()[args[0]](**obj_dict)
        args[2] = args[2].strip('"').strip("'")
        if args[2] in obj_dict.keys():
            prev_value = getattr(obj_spawn, args[2])
            string = type(prev_value)(string)
            setattr(obj_spawn, args[2], string)
        else:
            setattr(obj_spawn, args[2], string)

        with open('storage_file.json', 'r+', encoding='utf-8') as f:
            old_copy = json.load(f)
            f.seek(0)
            class_name = args[0] + '.' + args[1]
            old_copy[class_name] = obj_spawn.to_dict()
            new_copy = json.dumps(old_copy)
            f.write(new_copy)
        models.storage.reload()
        obj_spawn.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()

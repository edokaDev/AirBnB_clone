#!/usr/bin/python3
"""A cmd-line interpreter to handle creation and deletion of objects."""
import cmd
import json
import re
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
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

    def do_all(self, args):
        """all.

        Print all string representation of all instances
        based or not on the class name.
        Ex: $ all BaseModel or $ all.

        - The printed result is a list of strings.
        - If the class name doesn't exist,
        print ** class doesn't exist ** (ex: $ all MyModel)
        """
        args_list = args.split()
        class_name = None
        # If the class name is missing
        if len(args_list) == 1:
            class_name = args_list[0]
            if class_name not in globals():
                print("** class doesn't exist **")
                return

        json_models = FileStorage()
        json_models.reload()

        if class_name:
            objs = self.filter_obj_cls(json_models.all(), class_name)
        else:
            objs = json_models.all()

        all_list = []
        inst = None
        for ob in objs:
            ob_class_name = ob.split('.')[0]
            if class_name:
                if ob_class_name == class_name:
                    inst = globals()[class_name](**(objs[ob]))
            else:
                inst = globals()[ob_class_name](**(objs[ob]))
            all_list.append(inst.__str__())

        print(all_list)

    def do_destroy(self, line):
        """Delete.

        Delete an instance based on the class name
        and id (saves the changes into the JSON file)
        """
        if not line:
            print("** class name missing **")
            return

        args_list = line.split()

        class_name = args_list[0]
        if class_name not in globals():
            print("** class doesn't exist")
            return
        if len(args_list) < 2:
            print("** instance id missing **")
            return
        id = args_list[1]
        json_models = FileStorage()
        json_models.reload()
        obj_dict = json_models.all()
        try:
            obj_dict.pop(f"{class_name}.{id}")
            json_models.save()
        except KeyError:
            print("** no instance found **")
        return

    def filter_obj_cls(self, all_obj, class_name):
        """Class Object Filter.

        Filter the stored objects by a particular class.

        Args:
            - all_obj: dict - dictionary containing all objects.
            - class_name: string - Class name to filter
        Return:
            - New Dictionary with filtered objects.
        """
        regex = re.compile(rf"^({class_name}).")
        filtered_dict = {key: value for key, value in all_obj.items()
                         if re.search(regex, key)}
        return filtered_dict

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
        try:
            with open('storage_file.json', 'r', encoding='utf-8') as f:
                objs_dict = json.load(f)
        except Exception:
            return

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

        try:
            with open('storage_file.json', 'r+', encoding='utf-8') as f:
                old_copy = json.load(f)
                f.seek(0)
                class_name = args[0] + '.' + args[1]
                old_copy[class_name] = obj_spawn.to_dict()
                new_copy = json.dumps(old_copy)
                f.write(new_copy)
            models.storage.reload()
            obj_spawn.save()
        except Exception:
            return


if __name__ == "__main__":
    HBNBCommand().cmdloop()

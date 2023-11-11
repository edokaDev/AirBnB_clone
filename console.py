"""A cmd-line interpreter to handle creation and deletion of objects."""
import cmd
import json
from models.base_model import BaseModel
import models


class HBNBCommand(cmd.Cmd):
    """All methods and attributes that will be used in the command line."""

    def do_quit(self, line):
        """Exits the command line session."""
        return True

    def do_EOF(self, line):
        """Exits the command line session."""
        return True

    def emptyline(self):
        """Does nothing if empty line is parsed."""
        if self.lastcmd:
            self.lastcmd = ""
            self.onecmd(self.lastcmd)

    def do_create(self, line):
        """Creates an new instance of BaseModel,
        saves it to a json file and prints id.
        """
        class_list = ["BaseModel"]
        if not line:
            print("** class name missing **")
            return

        if line not in class_list:
            print("** class doesn't exist **")
            return
        if line in globals() and isinstance(globals()[line], type):
            new_object = globals()[line]()
            print(new_object.id)
            new_object.save()
        else:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Prints the string representation of an instance
        based on the class name and id.
        """
        if not line:
            print("** class name missing **")
            return

        args = line.split()

        if args[0] not in ["BaseModel"]:
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
            obj = models.base_model.BaseModel(**obj_dict)
            print(obj)

    def do_destroy(self, line):
        """Deletes an instance based on the class name
        and id (saves the changes into the JSON file)
        """
        if not line:
            print("** class name missing **")
            return

        args = line.split()

        if args[0] not in ["BaseModel"]:
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
        """Prints a list of string representations of class instances
        based or not based on the name of class
        Usage: all
               all ClassName
        """
        class_list = ["BaseModel"]
        args = line.split()
        argc = len(args)
        string_list = []

        if argc == 1:
            if args[0] not in class_list:
                print("** class doesn't exist **")
                return

        with open("storage_file.json", 'r', encoding='utf-8') as f:
            objs_dict = json.load(f)

        for key in objs_dict.keys():
            if argc == 1:
                if args[0] in key:
                    obj_dict = objs_dict[key]
                    obj_spawn = models.base_model.BaseModel(**obj_dict)
                    string = obj_spawn.__dict__
                    string_list.append(string)
            elif argc == 0:
                obj_dict = objs_dict[key]
                obj_spawn = models.base_model.BaseModel(**obj_dict)
                string = obj_spawn.__str__()
                string_list.append(string)

        if len(string_list) == 0:
            print("** class doesn't exist **")
        else:
            print(string_list)

    def do_update(self, line):
        """Updates an existing class instance by adding or
        modifying an attribute.
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        class_list = ["BaseModel"]
        args = line.split()
        argc = len(args)

        if argc < 1:
            print("** class name missing **")
            return
        if args[0] not in class_list:
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
        obj_spawn = models.base_model.BaseModel(**obj_dict)
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

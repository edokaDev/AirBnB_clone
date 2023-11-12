#!/usr/bin/python3
"""A cmd-line interpreter to handle creation and deletion of objects."""
import cmd
from datetime import datetime
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

    def do_show(self, line):
        """show.

        Print the string representation of an instance
        based on the class name and id.
        """
        if not line:
            print("** class name missing **")
            return
        args_list = line.split()
        # If the class name is missing
        if len(args_list) == 0:
            print("** class name missing **")
            return
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

        instance_found = False

        for item in obj_dict:
            obj = item.split(".")
            if class_name == obj[0] and id == obj[1]:
                # instance found
                new = globals()[class_name](**(obj_dict[item]))
                print(new.__str__())
                instance_found = True
                break
        if not instance_found:
            print("** no instance found **")
        return

    def do_destroy(self, line):
        """Delete.

        Delete an instance based on the class name
        and id (saves the changes into the JSON file)
        """
        if not line:
            print("** class name missing **")
            return

        args_list = line.split()
        # If the class name is missing
        if len(args_list) == 0:
            print("** class name missing **")
            return
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
                    inst = globals()[class_name](**(objs[ob].to_dict()))
            else:
                inst = globals()[ob_class_name](**(objs[ob].to_dict()))
            all_list.append(inst.__str__())

        print(all_list)

    def do_update(self, args):
        """update.

        Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com".

        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args_list = args.split()
        # if len(args_list) != 4:
        if len(args_list) >= 1:
            # class name present
            class_name = args_list[0]
            if class_name not in globals():
                print("** class doesn't exist **")
                return
            if len(args_list) >= 2:
                # class name and instance id present
                instance_id = args_list[1]
                # check if id exist

                json_models = FileStorage()
                json_models.reload()
                obj_dict = self.filter_obj_cls(json_models.all(), class_name)

                instance_found = False

                for item in obj_dict:
                    obj = item.split(".")
                    if class_name == obj[0] and instance_id == obj[1]:
                        # instance found
                        instance_found = True
                        break
                if not instance_found:
                    print("** no instance found **")
                    return

                if len(args_list) >= 3:
                    # attribute present
                    attr_name = args_list[2]

                else:
                    # attribute not present
                    print("** attribute name missing **")
                    return

                if len(args_list) >= 4:
                    # attribute value present

                    # stripping of quotes
                    attr_value = args_list[3].strip('"').strip("'")
                    if args_list[3][0] == '"':
                        # if the attribute value is multiple words
                        if len(args_list) == 5:
                            attr_value_1 = args_list[4].strip('"').strip("'")
                            attr_value = f"{attr_value} {attr_value_1}"
                    instance = obj_dict[f"{class_name}.{instance_id}"]
                    if attr_name in instance:
                        # casting the attr type if attr already exists
                        attr_value = type(instance[attr_name])(attr_value)
                    instance.__setitem__(attr_name, attr_value)

                    instance["updated_at"] = str(datetime.now().isoformat())
                    json_models.save()
                    return

                else:
                    # attribute value not present
                    print("** value missing **")
                    return

            else:
                # id not present
                print("** instance id missing **")
                return

        else:
            # If the class name is missing
            print("** class name missing **")
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


if __name__ == "__main__":
    HBNBCommand().cmdloop()

#!/usr/bin/python3
"""
Console 0.0.1
"""


import cmd
import sys
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class
    """
    prompt = "(hbnb) "
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print("")
        return True

    def emptyline(self):
        """Do nothing on an empty input line"""
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file),
        and prints the id.
        Ex: $ create BaseModel
        """
        if not arg:
            print("** class name missing **")
        elif arg not in self.classes:
            print("** class doesn't exist **")
        else:
            new_instance = self.classes[arg]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance based on the
        class name and id.
        Ex: $ show BaseModel 1234-1234-1234.
        """
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            objects = storage.all()
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file).
        Ex: $ destroy BaseModel 1234-1234-1234.
        """
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            objects = storage.all()
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Prints all string representation of all instances based or not
        on the class name.
        Ex: $ all BaseModel or $ all.
        """
        args = arg.split()
        objects = storage.all()

        if not arg:
            print([str(obj) for obj in objects.values()])
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            print([str(obj) for key, obj in
                   objects.items() if key.startswith(args[0])])

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com".
        """
        args = arg.split()
        objects = storage.all()

        if not arg:
            print("** class name missing **")
        elif args[0] not in self.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key not in objects:
                print("** no instance found **")
            else:
                obj = objects[key]
                attr_name = args[2]
                attr_value = args[3]
                setattr(obj, attr_name, attr_value)
                obj.save

    def default(self, line):
        ''' To handle <class name>.<command>() syntax '''
        args = line.split(".")
        class_name = args[0]
        cmd_name = args[1]
        if cmd_name == "all()":
            self.do_all(class_name)
        elif cmd_name.startswith("show"):
            ID = cmd_name[5:-1]
            arg = f"{class_name} {ID}"
            self.do_show(arg)
        elif cmd_name.startswith("destroy"):
            ID = cmd_name[9:-2]
            arg = f"{class_name} {ID}"
            self.do_destroy(arg)


if __name__ == '__main__':
    HBNBCommand().cmdloop()

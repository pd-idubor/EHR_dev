#!/usr/bin/python3
"""
    Describes the HBNB class
"""
import cmd
from models import storage
import shlex
from models.base_model import BaseModel
from models.user import User
from models.demo import Demo
#from models.history import History
from models.complaint import Complaint
from models.diagnosis import Diagnosis
from models.labs import Labs
from models.medics import Medics
from models.practitioner import Practitioner
from models.procedure import Procedure


classes = {"BaseModel": BaseModel, "User": User, "Demo": Demo,
            "Complaint": Complaint,
            "Diagnosis": Diagnosis, "Labs": Labs,
            "Medics": Medics, "Procedure": Procedure,
            "Practitioner": Practitioner
            }

class EHRCommand(cmd.Cmd):
    """
        Defines the the entry point of the command interpreter
    """
    prompt = "(EHR app)> "

    def do_quit(self, args):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, args):
        """EOF signal to exit the program
        """
        return True

    def do_create(self, args):
        """Creates a new instance of BaseModel and prints the id
        """
        new = args.split(" ")

        if not new:
            print("** class name missing **")
            return

        elif new[0] not in classes:
            print("** class doesn't exist **")
            return
        new_instance = classes[new[0]]()

        for i in range(1, len(new)):
            first = new[i].split("=")
            try:
                if first[1][0] == "\"":
                    first[1] = first[1].replace("\"", "")
                    first[1] = first[1].replace("_", " ")

                elif "." in first[1]:
                    first[1] = float(first[1])

                else:
                    first[1] = int(first[1])
                setattr(new_instance, first[0], first[1])
            except (Exception):
                continue
        new_instance.save()
        print(new_instance.id)

    def do_show(self, args):
        """Prints the string representation of an instance
        """
        arg_l = shlex.split(args)

        if (len(arg_l) == 0):
            print("** class name missing **")
            return

        try:
            eval(arg_l[0])
        except NameError:
            print("** class doesn't exist **")
            return

        if (len(arg_l) == 1):
            print("** instance id missing **")
            return

        r_obj = storage.all()
        key = arg_l[0] + "." + arg_l[1]
        try:
            val = r_obj[key]
            print(val)
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id
        """
        arg_l = shlex.split(args)

        if (len(arg_l) == 0):
            print("** class name missing **")
            return

        try:
            eval(arg_l[0])
        except NameError:
            print("** class doesn't exist **")
            return

        if (len(arg_l) == 1):
            print("** instance id missing **")
            return

        r_obj = storage.all()
        key = arg_l[0] + "." + arg_l[1]

        try:
            del r_obj[key]

        except KeyError:
            print("** no instance found **")
        storage.save()

    def do_all(self, args):
        """Prints all string representation of all instances
        """
        arg = shlex.split(args)

        if (len(args) > 0):
            try:
                eval(args)
            except NameError:
                print("** class doesn't exist **")
                return
        objs = storage.all()
        obj_list = []

        for objs in storage.all().values():
            if (len(arg) > 0):
                if (arg[0] == objs.__class__.__name__):
                    obj_list.append(objs.__str__())
            elif (len(arg) == 0):
                obj_list.append(objs.__str__())
        print(obj_list)

    def do_update(self, args):
        """Updates an instance based on the class name and id
        """
        arg_l = shlex.split(args)

        if (len(arg_l) == 0):
            print("** class name missing **")
            return

        try:
            eval(arg_l[0])
        except NameError:
            print("** class doesn't exist **")
            return

        if (len(arg_l) == 1):
            print("** instance id missing **")
            return

        r_obj = storage.all()
        key = arg_l[0] + "." + arg_l[1]
        try:
            obj_val = r_obj[key]
        except KeyError:
            print("** no instance found **")
            return

        if (len(arg_l) == 2):
            print("** attribute name missing **")
            return

        if (len(arg_l) == 3):
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return
        try:
            attr_t = type(getattr(obj_val, arg_l[2]))
            arg_l[3] = attr_t(arg_l[3])
        except AttributeError:
            pass
        setattr(obj_val, arg_l[2], arg_l[3])
        storage.save()

    def do_count(self, args):
        """
            Rretrieve the number of instances of a class
        """
        objs_l = []
        objs = storage.all()

        try:
            if len(args) != 0:
                eval(args)
        except NameError:
            print("** class doesn't exist **")
            return

        for key, val in objs.items():
            if len(args) != 0:
                if type(val) is eval(args):
                    objs_l.append(val)
            else:
                objs_l.append(val)
        print(len(objs_l))

    def default(self, args):
        """
            Catches funcions of dot notation, default for invalid input
        """
        func_args = {
                "all": self.do_all,
                "count": self.do_count,
                "show": self.do_show,
                "destroy": self.do_destroy,
                "update": self.do_update
                }
        args = (args.replace("(", ".").replace(")", ".")
                .replace('"', "").replace(",", "").split("."))

        try:
            cmd_arg = args[0] + " " + args[2]
            func = func_args[args[1]]
            func(cmd_arg)
        except (IndexError, KeyError):
            print("*** Unknown syntax:", args[0])

    def emptyline(self):
        """Executes nothing upon receiving an empty line
        """
        pass


if __name__ == '__main__':
    EHRCommand().cmdloop()

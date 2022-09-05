#!/usr/bin/python

"""A module for command line interface tool"""
import cmd
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


class HBNBCommand(cmd.Cmd):

    """
    A command line interface tool
    for the HBNB project
    """

    prompt = '(hbnb) '
    __classes = {

        'Amenity',
        'BaseModel',
        'City',
        'Place',
        'Review',
        'State',
        'User',

    }

    def precmd(self, arg):

        if "." in arg and "(" in arg and ")" in arg:
            if "{" not in arg and "}" not in arg:
                holder = arg.split(".")
                holder1 = holder[1].split("(")
                holder2 = holder1[1].split(")")
                if "\"" in arg:
                    holder3 = holder2[0].split("\"")
                    try:
                        args = [holder1[0],
                                holder[0],
                                holder3[1],
                                holder3[3],
                                holder3[5]
                                ]
                        arg = " ".join(args)
                    except IndexError:
                        arg = holder1[0] + " " + holder[0] + " " + holder3[1]

                else:
                    arg = holder1[0] + " " + holder[0]
        return arg

    def do_count(self, arg):
        """ Counts any class attribute"""
        if arg in self.__classes:
            with open("storage.json", 'r') as file:
                new = json.load(file)
                holder = []
                count = 0
                for data in new:
                    if arg[0] in data:
                        holder.append(str(new[data]))
                        count += 1
            file.close()
            print(count)

    def do_quit(self, arg):
        """Quits the console and returns nothing"""
        exit()

    def do_EOF(self, arg):
        """sends EOF signal to the console"""
        print("")
        return True

    def emptyline(self):
        """Skips empty lines of command"""
        pass

    def do_create(self, arg):
        """
        creates a new instance of BaseModel
        usage: create BaseModel
        """
        value = parse(arg)
        if not value:
            print("**class name missing **")
        # if value[0] == 'BaseModel':
        elif value[0] in self.__classes:
            print(eval(value[0])().id)
            storage.save()

        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """
        Prints the string representation
        of an instance based on the class
        """
        value = parse(arg)

        if not value:
            print("** class name is missing **")

        elif value[0] not in self.__classes:
            print("** class doesn't exist **")

        elif value[0] in self.__classes:
            with open("storage.json", "r") as file:
                holder = json.load(file)
                file.close()
            try:
                key = value[0] + "." + value[1]
            except IndexError:
                print("** instance id is missing **")
                return
            try:
                print(holder[key])
                # print(storage.all()[key])
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based
        on the class name passed
        as an argument with the id
        """
        value = parse(arg)
        all_obj = storage.all()

        if not value:
            print("** class name is missing **")

        elif value[0] == 'all':
            with open("file.json", "r") as file:
                holder = json.load(file)
            file.close()
            holder.clear()
            with open("file.json", "w") as file:
                json.dump(holder, file, indent=2)
            file.close()
            with open("storage.json", "w") as file:
                json.dump(holder, file, indent=2)
            file.close()
            storage.destroy()

        elif value[0] not in self.__classes:
            print("** class doesn't exist **")

        elif value[0] in self.__classes:
            with open("file.json", "r") as file:
                holder = json.load(file)
            file.close()
            try:
                key = value[0] + "." + value[1]
            except IndexError:
                print("** instance id is missing **")
                return
            try:
                holder.pop(key)
                objects = storage
                objects.destroy(key)
                objects.save()
            except KeyError:
                print("** no instance found **")
                return
            with open("file.json", "w") as file:
                json.dump(holder, file, indent=2)
            file.close()
#           FOR STORAGE REPRESENTATION
            with open("storage.json", "r") as file:
                holder = json.load(file)
            file.close()
            try:
                key = value[0] + "." + value[1]
            except IndexError:
                print("** instance id is missing **")
                return

            with open("storage.json", "w") as file:
                json.dump(holder, file, indent=2)
            file.close()

    def do_all(self, arg):
        """"
        prints all string representation
        of all
        """
        value = parse(arg)

        if not value:
            hold = storage.all()
            holder = []
            for key in hold.keys():
                holder.append(str(hold[key]))
            # with open("storage.json", 'r') as file:
            #     new = json.load(file)
            #     holder = []
            #     for data in new:
            #             holder.append(str(new[data]))
            print(holder)
            del holder
            return

        elif value[0] in self.__classes:
            with open("storage.json", 'r') as file:
                new = json.load(file)
                holder = []
                for data in new:
                    if value[0] in data:
                        holder.append(str(new[data]))
            file.close()
            print(holder)

        elif value[0] not in self.__classes:
            print("** class doesn't exist **")
            return

    def do_update(self, arg):
        """
        updates a given instance
        based on the class namean id
        Eg:
        <update> <class name> <id> <attr name>
        """
        value = parse(arg)

        if not value:
            print("** class is missing **")
            return

        elif value[0] not in self.__classes:
            print("** class doesn't exist**")
            return

        elif len(value) < 2:
            print("** instance id missing **")
            return

        # elif len(value) < 4:
        #     print("** value missing **")

        else:
            try:
                with open("file.json", 'r+') as file:
                    holder = json.load(file)
                file.close()
                key = value[0] + "." + value[1]
                if key not in holder.keys():
                    print("** no instance found **")
                    return
                try:
                    attr_name = value[2]
                except IndexError:
                    print("** attribute name missing **")
                    return
                try:
                    new_value = value[3]
                except IndexError:
                    print("** value missing **")
                    return
                setattr(storage.all()[key], attr_name, new_value)
                storage.all()[key].save()
            except IndexError:
                print("** no instance found **")

        pass


def parse(arg):
    return arg.split()


if __name__ == '__main__':
    HBNBCommand().cmdloop()

import os, sys

def get_disk():
    res = ''
    confirm = 'n'
    while (confirm != 'y'):
        print(os.popen("lsblk").read())
        res = input("enter disk name: ")
        confirm = input("U shure? [y/n] ")
    return res;

def edit_users():
    root_psswd = ''
    cnf = ''
    while (root_psswd == '' or cnf != 'y'):
        root_psswd = input("Choose password for root: ")
        cnf = input("U shure? [y/n] ")

    cmd = ""
    users = {"root" : {"password" : root_psswd}}
    while (cmd != "done"):
        cmd = input("\nEditing users\nFor all commands type \"help\"\nEnter the command: ")

        if (cmd == "help"):
            print("Commands: list, add_user, rm_user, add_group, rm_group, done")

        if (cmd =="list"):
            print(users, sep="\n")

        if (cmd == "add_user"):
            name = input("name? ")
            if (name in users):
                print("user already exists")
                continue

            psswd = input("passwoed? ")
            if (len(psswd) == 0):
                print("incorrect password")
                continue

            cnf = input("U shure? [y/n] ")
            if (cnf != 'y'):
                continue
            users[name] = {'password' : psswd}

        if (cmd == "rm_user"):
            name = input("name to remove? ")
            if (name == "root"):
                print("impossible to remove root user")
                continue
            cnf = input("U shure? [y/n]")
            if (cnf != 'y'):
                continue
            if (name in users):
                users.pop(name)

        if (cmd == "add_group"):
            name = input("name? ")
            if (name == "root"):
                print("Impossible to add root in groups")
                continue

            groups = input("groups? ").split()
            if (name not in users):
                print("wrong username")
                continue
            if ("groups" not in users[name]):
                users[name]["groups"] = []

            cnf = input("U shure? [y/n] ")
            if (cnf != "y"):
                continue

            for i in groups:
                if (i not in users[name]["groups"]):
                    users[name]["groups"].append(i)

        if (cmd == "rm_group"):
            name = input("name? ")
            groups = input("groups to remove? ").split()

            cnf = input("U shure? [y/n] ")
            if (name not in users):
                continue
            if ('groups' not in users[name]):
                continue

            for i in groups:
                if (i in users[name]["groups"]):
                    users[name]["groups"].remove(i)
            if (len(users[name]["groups"]) == 0):
                users[name].pop("groups")
    return users

disk = get_disk()
users = edit_users()
f = open("users", "w")
f.writelines(str(len(users)))
f.writelines('\n')
for i in users:
    f.writelines(i)
    f.writelines('\n')
    f.writelines(users[i]["password"])
    f.writelines('\n')
    if ("groups" in users[i]):
        f.writelines(str(len(users[i]["groups"])))
        f.writelines('\n')
        for j in users[i]["groups"]:
            f.writelines(j)
            f.writelines('\n')
    else:
        f.writelines('0')
        f.writelines('\n')
f.close()

os.system(f"mkfs.ext4 /dev/{disk}2")
os.system(f"mkfs.fat -F 32 /dev/{disk}1")

os.system(f"mount /dev/{disk}2 /mnt")
os.system(f"mount --mkdir /dev/{disk}1 /mnt/boot")

os.system(f"pacstrap -K /mnt base linux linux-firmware vim python3 networkmanager")

os.system("genfstab -U /mnt >> /mnt/etc/fstab")

os.system("mkdir /mnt/die")
os.system("cp help.py /mnt/die/run.py")
os.system("cp users /mnt/die/")

os.system("cp --dereference /etc/resolv.conf /mnt/etc/")
os.system("mount --types proc /proc /mnt/proc ")
os.system("mount --rbind /sys /mnt/sys")
os.system("mount --make-rslave /mnt/sys ")
os.system("mount --rbind /dev /mnt/dev ")
os.system("mount --make-rslave /mnt/dev ")
os.system("mount --bind /run /mnt/run ")
os.system("mount --make-slave /mnt/run ")
os.system("chroot /mnt /bin/bash -c \"python3 /die/run.py\"")
os.system("rm -rf /mnt/die")
os.system("rm users")
#os.system("reboot")

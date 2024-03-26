import os, sys

def add_users():
    f = open("die/users", "r")
    lst = [i[:-1] for i in f.readlines()]
    n = int(lst[0])
    print(f"echo \"root:{lst[2]}\" | chpasswd")

    cnt = 4
    for i in range(n - 1):
        name = lst[cnt]
        psswd = lst[cnt + 1]
        groups = ""
        x = int(lst[cnt + 2])
        cnt += 3
        print(f"useradd -m {name}")
        for j in range(x):
            group = lst[cnt]
            print(f"usermod -aG {group} {name}")
            cnt += 1
        print(f"echo \"{name}:{psswd}\" | chpasswd")

add_users()

os.system("mkinitcpio -P")
os.system("pacman -S efibootmgr grub sudo --noconfirm")
os.system("grub-install --target=x86_64-efi --efi-directory=/boot")
os.system("grub-mkconfig -o /boot/grub/grub.cfg")
os.system("systemctl enable NetworkManager")
os.system("echo \"%wheel ALL=(ALL:ALL) ALL\" >> /etc/sudoers")

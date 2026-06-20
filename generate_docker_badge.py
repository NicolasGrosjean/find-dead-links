from genbadge import Badge

version = input("Enter the version: ")
b = Badge(left_txt="docker", right_txt=version, color="brightgreen")
b.write_to("badges/docker.svg", use_shields=False)

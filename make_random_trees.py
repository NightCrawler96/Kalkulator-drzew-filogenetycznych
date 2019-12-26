from subprocess import call

for i in range(5):
    call(["python", "biola.py", f"./tmp/{i}.newick", "-r", "5"])

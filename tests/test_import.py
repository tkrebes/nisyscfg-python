import os

parent_dir, _ = os.path.split(os.path.dirname(__file__))
# Set the current working directory to the parent directory of test_import.py.
os.chdir(parent_dir)

# Walk all module directories and create import tests for all non-private python
# modules.
for root, dirs, files in os.walk("nisyscfg"):
    base_name = ".".join(root.split(os.path.sep))
    if "__init__.py" in files:
        exec("def test_{}(): import {}".format(base_name.replace(".", "_"), base_name))
    for f in files:
        if f.endswith(".py") and not f.startswith("_"):
            mod_name = base_name + "." + f[:-3]
            exec("def test_{}(): import {}".format(mod_name.replace(".", "_"), mod_name))

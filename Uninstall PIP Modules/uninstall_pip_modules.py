import subprocess

RESTRICTED_PACKAGES = ["pip", "setuptools", "wheel"]

def get_installed_packages():
    result = subprocess.run(["pip3", "list"], capture_output=True)
    packages_w_versions = result.stdout.decode('utf-8').split("\n")

    packages = []
    for i in range(2, len(packages_w_versions)-1):
        p = packages_w_versions[i]
        package = p.split(" ")[0].strip()
        if package not in RESTRICTED_PACKAGES:
            packages.append(package)

    return packages

def uninstall_package(package_name):
    print("Attempting to uninstall package: " + package_name)
    subprocess.run(["pip3", "uninstall", "-y", package_name])

if __name__ == "__main__":
    packages = get_installed_packages()
    while len(packages) > 0:
        for p in packages:
            uninstall_package(p)
        packages = get_installed_packages()

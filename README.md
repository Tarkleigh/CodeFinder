# CodeFinder

In larger code bases with multiple Git repositories, it can sometimes be difficult to tell where code is used.
This can be especially vexing when trying to remove cyclic dependencies between Git repositories
where a detailed list of code usages is vital. While modern IDEs are good at finding usages of individual files or
classes
they usually don't offer the feature to create a complete list of dependencies. Editors like VIM often offer even less.

This is where this tool comes in. It will find all usages of Java code from Git repository A (the source repository)
in Git repository B (the target repository) and create an easy to consume output of the findings for later inspection

## How to use:

First, check out the two Git repositories you want to inspect. Once this is done, run CodeFinder.py and pass it the path
to
the two repositories. This can be done by either:

- Using the --source_root and --target_root parameters on the command line or in a script
- Simply running the script without parameters. A file chooser dialogue will appear and allow you to choose first the
  source and then the
  target root folder

These options can also be mixed, if you prefer. Once the two root directories are set, the script will run and first
create
a list of Java classes from the source repository and then try to find them in the target repository. The script will
print
output to the shell while it is running, giving you feedback what was already found. Once the target repository has been
fully
searched, a .csv file with the results will be created in the folder the script was run in. The file will be
automatically
opened by whatever program you are using for this file ending

## Which folder to use:

The script will accept any folder as a starting point and will search the subdirectories for .Java files. It will do the
same for the target repository root once the list of dependencies has been created. To avoid unnecessary directory
searches
you should choose the lowest directory to start as possible.

To make the output easily understandable, the script will create a label for both the source and target repository that
depends on the passed folders. If your project uses the common Gradle or Maven directory structure, the script will find
the
"src" folder and use the name of the folder above it for the label. Otherwise, it will use the name of the corresponding
root folder
for the label

## What does the output look like?

The output will be a csv file called "dependency_usages.csv" with the columns "Source Module,Used Class,Target
Module,Consuming Class" 

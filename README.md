# CodeFinder

In larger code bases with multiple Git repositories, it can sometimes be difficult to tell which part of a repository is
used where. This can be especially vexing when trying to break cyclic dependencies since developers need to know which
code to make the dependency graph acyclic again. While modern IDEs are good at finding usages of individual files or
classes they usually don't offer the option to create a complete usage list of all coding in repository. Text editors
like Vim or NeoVim offer even less.

This is where this script comes in. It will find all usages of Java code from Git repository A (the source repository)
in Git repository B (the target repository) and create an easy to consume output of the findings for later inspection.
Naturally, this can also be used without Git as the input are just paths to directories.

## How to use:

First, check out the two Git repositories you want to inspect. Once this is done, run **CodeFinder.py** and pass the
fully-qualified path to the source and target folders (for example your repositories). This can be done by either:

- Using the --source_root and --target_root parameters on the command line or when running the script in an IDE
- Simply running the script without parameters. A file chooser dialogue will appear and allow you to pick first the
  source and then the target root folder
- If you pass just one of the parameters, the script will prompt you for the missing path

Once the paths to two root directories are set, the script will run and create a list of Java classes from the source
repository which it will then try to find in the target repository. The script will print output to the console while it
is running, giving you feedback which folder it is currently scanning. Once the target repository has been fully
searched, a csv file with the results will be created in the folder the script was executed. The file will then be
automatically opened by whatever program you are using for this file ending (provided you have set a default for csv
files)

## What does the output look like?

The output will be a csv file called "dependency_usages.csv" with the columns "Source Module,Used Class,Target
Module,Consuming Class".

For example, here are the usages of the hypothetical Tesseract Engine in the also fictional project Magnetar:

![](https://github.com/Tarkleigh/CodeFinder/blob/main/examples/Example.png)

This screenshot is from Apple's Numbers tool, please use the raw csv file in the "examples" folder to see the output in
your tool of choice.

## What counts as a usage?

At the moment, the script considers importing a class a usage. It does not automatically exclude for unused imports, so
if your coding regularly imports code it does not need, this will result in possibly misleading output (you will get
false positives in the findings). This is currently not considered a bug, since unused imports are generally frowned
upon.

The script also does not consider static imports and fully qualified imports. These could be considered in principle but
would require scanning the entire source code for usages rather than stopping after the import section which is how the
script currently works. Given that source files can get very large (potentially thousands of lines) and these kind of
imports aren't very common, this limitation is currently seemed acceptable. If it isn't for you, please feel free to
reach out.

## Which folder to use:

The script will accept any folder as a starting point and will search the subdirectories for Java files (i.e. files that
end in .java or whatever file ending your operating system uses). It will do the same for the target repository root
once the list of dependencies has been created. To avoid unnecessary directory searches you should choose the lowest
possible directory as a starting point. For example, if you only care about usages from part of your source repository,
setting this sub-folder as source root can help keeping the results relevant and reducing the runtime of the script.

To make the output easily understandable, the script will create a label for both the source and target repository that
depends on the passed folders. If your project uses the common Maven / Gradle directory structure, the script will find
the "src" folder and use the name of the folder above it for the label. Otherwise, it will use the name of the passed
root folder as the label

## Compatibility Notes:

This script only works with Java files, and it assumes the touched files are encoded in UTF-8. Files in any other
encoding will be ignored and a warning will be printed to help you find the wrongly encoded files. While the Maven /
Gradle directory structure is used when determining the label, the script does not require this directory setup, and you
can use it for all kind of Java coding as long as you pass in two valid directories.

The script is portable and should run on all common operating systems (it was tested on Windows, macOS and Ubuntu).
Since Java is multi-platform, this script should be as well, so if it does not work for your operating system, please
feel free to open an issue.
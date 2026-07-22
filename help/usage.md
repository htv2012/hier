# How to Use This Template

## Create a New Project Using This Template

Follow this [procedure](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)

# Rename the Project

Once you cloned this template, the first step is to rename the
project to reflect your purpose and to avoid name collision.

1. Search for the word *xyz in all the files, except for file `uv.lock` and directory `help`.
3. Replace *xyz* with the name of your project
4. Rename `src/xyz` to a new name, take care to use
   underscore instead of dashes. For example, if your project name is
   *foo-bar*, then the directory should be *foo_bar*

Instead of performing the above steps, you can also issue the following command:

    make rename

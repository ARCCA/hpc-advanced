---
title: "Installing packages"
teaching: 15
exercises: 30
questions:
- "How do I install a package for framwork/language X?"
- "Can I use the operating system package manager?"
objectives:
- "Install packages for a wide range of languages such as Python, R, Anaconda, Perl"
- "Use containers to install complete software packages with dependencies in a single image with Singularity."
keypoints:
- "Users can control their own software when needed for development."
---

Installing packages for common frameworks/languages is very useful for a user on HPC to perform.  Fortunately we allow downloads
from the Internet so this is quite easy to achieve (some HPC systems can be isolated from the Internet that makes things
harder).  There will be many ways to install packages for programs, for example Perl can be just the operating system
version of Perl or part of a bigger packages such as ActiveState Perl.  ActiveState has its own package system rather
than using the default package system in Perl.  However we aim to provide the user in this section to be able to
understand how packages work and install for common languages.

Once installed on the login node, the SLURM job scripts can be written to take advantage of the new package or software.
You do not need to install the package again!

> ## Check versions
>
> Versions of software modules can be checked with `module av`, for example for Python
>
> ~~~
> $ module av python
> ~~~
> {: .language-bash}
>
> Specifying the version of the software also makes sure changes to default version will not impact your jobs.  For
> example default python loaded with `module load python` could install packages into one location but if the default
> version changed it will not automatically reinstall those packages.
{: .callout}

# Python

[Python](https://www.python.org) is becoming the de-facto language across many disciplines.  It is easy to read, write and run.  Python 3 should
be preferred over the now retired Python 2.  On Hawk a user can load Python from a module

~~~
$ module load python/3.7.0
~~~
{: .language-bash}

> ## Python versions
>
> Calling Python can be performed using just `python` or with the version number such as `python3` or even 
> more exact `python3.7`.  To be sure you are calling Python 3 we recommend running with `python3` rather than the unversioned `python`.  What is the difference on Hawk?
> > ## Solution
> >
> > ~~~
> > $ python --version
> > ~~~
> > {: .language-bash}
> >
> > will print
> >
> > ~~~
> > Python 2.7.5
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}

Python 3.7.0 is now loaded into your environment, this can be checked with

~~~
$ python3 --version
~~~
{: .language-bash}

~~~
$ Python 3.7.0
~~~
{: .output}

## Installing a package

To install a package we recommend using the `pip` functionality.  This provides many packages of Python and handles
dependencies between the packages.  For a user on Hawk, this can be run as

~~~
$ pip3 install --user <package>
~~~
{: .language-bash}

> ## Pip versions
>
> Pip (just like Python) also is versioned with `pip` just being some OS default.  Whilst `pip3` will call the Python 3
> version of Pip.  This is important to match overwise it will install packages in the wrong location.  What versions
> are available on Hawk?
> > ## Solution
> > 
> > There is no default OS `pip` but `pip` and `pip` are supplied by the module.
> > 
> > ~~~
> > $ pip --version
> > $ pip3 --version
> > ~~~
> > {: .language-bash}
> > 
> > Both print
> > 
> > ~~~
> > pip 20.0.2 from /apps/languages/python/3.7.0/el7/AVX512/intel-2018/lib/python3.7/site-packages/pip (python 3.7)
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}

Where `<package>` is the name of the package.  The packages can be found using the Python Package Index or
[PyPI](https://pypi.org).

The main concept for the user is to use `--user` that places the package in `$HOME` in this case in `$HOME/.local/lib/python3.7/site-packages`.  This is automatically in the searchpath for Python when importing the module.

### Example

To install a rather unhelpful `hello-world` package, run

~~~
$ pip3 install --user pip-hello-world
~~~
{: .language-bash}

This will install the package in your `$HOME` directory.

This package can be tested with the following Python script

~~~
from helloworld import hello
c = hello.Hello()
c.say_hello()
~~~
{: .language-python}

The script will produce

~~~
'Hello, World!'
~~~
{: .output}

> ## Virtual environments
>
> Python supports a concept called virtual environments.  These are self-contained Python environments that allows you
> to install packages without impacting other environments you may have.  For example:
>
> ~~~
> $ python3.7 -m venv pyenv-test
> $ source pyenv-test/bin/activate
> $ pip3 install pip-hello-world
> $ python3.7
> $ deactivate
> ~~~
> {: .language-bash}
>
> Everything is contained with the directory `pyenv-test`.  There was also no need to specify `--user`.  For beginners
> this can be quite confusing but is very useful to master.  Once finished you can `deactivate` the environment`.
{: .callout}

## R

[R](https://cran.r-project.org/) is a language for statisticians. It is very popular language to perform statistics (its primary role).  Package
management for R is inbuilt rather than using a separate program to perform it.  
On Hawk, R can be loaded via the module system with

~~~
$ module load R/3.5.1
~~~
{: .language-bash}

### Example

Running R, the following command will install the `jsonlite` package

~~~
install.packages(“jsonlite”)
# (If prompted, answer Yes to install locally)
# Select a download mirror in UK if possible.
~~~
{: .language-r}

Where `jsonlite` is the package name you want to install.  Information can be found at
[CRAN](https://cran.r-project.org/)

In this case the package will be installed at `$HOME/R/x86_64-pc-linux-gnu-library/3.5/`

## Anaconda

[Anaconda](https://www.anaconda.org) is a fully featured software management tool that provides many packages for many different languages.
Anaconda allow dependencies between software packages to be installed.

Since Anaconda keeps updating we can load the module on Hawk with

~~~
$ module load anaconda
~~~
{: .language-bash}

This should load a default version of Anaconda.  Specific versions can be loaded as well.

### Example

A package can then be installed with

~~~
$ conda search biopython
$ conda create --name snowflakes biopython
~~~
{: .language-bash}

This first checks there is a `biopython` package and then creates an environment `snowflakes` to store the package in.

The files are stored in `$HOME/.conda`

This package can then be activated using

~~~
$ conda info --envs
$ . /apps/languages/anaconda3/etc/profile.d/conda.sh
$ conda activate snowflakes
$ python
$ source deactivate
~~~
{: .language-bash}

This first lists all environments you have installed.  Then activates the environment you would like and then you can
run `python`.  Finally you can deactivate the environment.

Newer versions of Anaconda may change the procedure.

> ## Anaconda directory
>
> Every package you download is stored in `$HOME/.conda` and also lots of other files are created for every package.
> Overtime this directory can have many files and will reach the quota limit for files.  We recommend using `conda clean
> -a` to tidyup the directory and reduce the number of files.
{: .callout}

## Perl

[Perl](https://www.perl.org) has been around for a long-time but becoming uncommon to see being used on HPC.  On Hawk we
recommend using the operating system Perl command so no module is required.

~~~
$ perl --version
~~~
{: .language-bash}

To manage packages we can use the `cpanm` utility.  This can be installed in your home directory with

~~~
$ mkdir -p ~/bin && cd ~/bin
$ curl -L https://cpanmin.us/ -o cpanm
$ chmod +x cpanm
~~~
{: .language-bash}

Then setup `cpanm` with

~~~
$ cpanm --local-lib=~/perl5 local::lib
$ eval $(perl -I ~/perl5/lib/perl5/ -Mlocal::lib)
$ perl -I ~/perl5/lib/perl5/ -Mlocal::lib
# Add output from perl command above to $HOME/.myenv
~~~
{: .language-bash}

This will install Perl packages in `$HOME/perl5`.

### Example

Install the `Test::More` package.

~~~
$ cpanm Test::More
~~~
{: .language-bash}

Then run the following Perl script

~~~
use Test::More;
print $Test::More::VERSION ."\n";
~~~
{: .source}

Which should produce something like

~~~
1.302175
~~~
{: .output}

## Singularity

[Singularity](https://sylabs.io/) is a container solution for HPC where alternatives such as Docker are not suitable.
Singularity can *pretend* to be another operating system but inherits all the local privilege you have on the host
system.  On Hawk we do not want anyone to be able to run software as another user - especially root.  Also containers
are immutable so you save files inside containers - $HOME and /scratch are mounted within the image.

Singulairity is available as a module with:

~~~
$ module load singularity
~~~
{: .language-bash}

The latest version should be preferred due to containing the latest versions of the code that may include security and
performance fixes.

Singularity can then be used, initially users will want to download existing containers but eventually you can build you
own - maybe via the [Singularity Hub](https://www.singularity-hub.org)

> ## MPI and GPUs
>
> Singularity supports using MPI and GPUs.  MPI can be tricky especially with OpenMPI but GPUs are supported using the
> `--nv` command line option that loads the relevent GPU libraries into the container from the host operating system.
{: .callout}

### Example

To download a container from Singularity Hub then you can run:

~~~
$ singularity pull shub://vsoch/hello-world
~~~
{: .language-bash}

This will pull down an image file `hello-world_latest.sif`.  This can be run with:

~~~
$ singularity run hello-world_latest.sif
~~~
{: .language-bash}

This produces the following output:

~~~
RaawwWWWWWRRRR!! Avocado!
~~~
{: .output}

[Docker Hub](https://hub.docker.com) can also be used for Docker containers such as

~~~
$ singularity pull docker://ubuntu
~~~
{: .language-bash}

You can then run a Ubuntu application on Redhat, e.g.

~~~
$ singularity exec ubuntu_latest.sif cat /etc/os-release
~~~
{: .language-bash}

A useful site for GPUs is [NGC](https://ngc.nvidia.com/catalog/all) that hosts containers for software optimised for
GPUs.  Instructions are on the website.

> ## Containers
> 
> Containers allows a user to build once and run anywhere (if same processor type).  A recipe file can be created to
> store the exact steps used to create the image.  This can make sure any code is reproducible by others.  It is useful
> for packages that assume a user has root access to their machine and install OS level packages for dependencies.
{: .callout}

# Others?

There may be other software package managers that you want to investigte. Please get in touch with us if you need help.
For example, the [Spack](https://spack.io/) is a software manager to make it easy to install packages.  Finally there is
also the traditional `autoconf` and `make` approach. For example you can build software with:

~~~
$ ./configure --prefix=$HOME/my_package
$ make
$ make install
~~~
{: .language-bash}

This will install `my_package` in your `$HOME` directory.

Experimenting with software packages is encouraged to find new and novel ways to perform your research.


{% include links.md %}


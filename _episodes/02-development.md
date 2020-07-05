---
title: "Development tools for building code"
teaching: 30
exercises: 15
questions:
- "What more can I do with the command-line?"
- "How can I revert changes to code?"
- "How can I build things in a certain order?"
- "What options are they when I compiler code?"
objectives:
- "Move around the command-line with ease."
- "Understand options available to revision control."
- "Use simple makefiles to build code."
- "Understand some basic compiler options."
keypoints:
- "Navigating the command-line quickly can save time and reduce mistakes."
- "Revision control is not just good practice but good science."
- "Repeating multiple steps can be quick."
- "Compilers are not smart, requires smart users to tell them what to do."
---

# Command-line and tools at your fingertips.

A Linux course is a good start to learn the required skills needed to access HPC systems hosted across a network via
ssh.  The command-line is a very powerful device, once mastered, desktops can seem inefficient when performing some
tasks.

> ## Editing a long command.
> You may have just written a very long command-line - maybe with a few pipes (`|`) or pasted in a long line of text (a
> search term).  You discover you spelt part of the command incorrect, how do you get to that part of the line?
{: .challenge}

The default shell on many Linux systems is Bash. Bash provides the commands and features for the user to interact with
the system.  Bash provides a number of options, these can be seen with `set -o`

One particular useful feature to know about if the editing mode of Bash.  These are descrived as `emacs` or `vi` mode.
These are the 2 most famous editors on Linux - a regular Linux user usually finds themselves either using `emacs` or
`vi` eventually.  These editors have different ways to navigate within text. Foe example in `emacs`, `CTRL-a` will
position the cursor at the beginning of the line, `CTRL-e` to the end.  In `vi` , `^` will position the cursor at
beginning of the line, `$` to the end.

> ## Finding currently used options
> Find the current set of options used by your Bash shell and find the editing mode used.
>
> > ## Solution
> >
> > Printing the current settings can be achieved simply with:
> >
> > ~~~
> > $ set -o
> > ~~~
> > {: .language-bash}
> >
> > ~~~
> > <...>
> > emacs           on
> > <...>
> > vi              off
> > <...>
> > ~~~
> > {: .output}
> {: .solution}
{: .challenge}

The options can be changed by giving the preffered way of navigating

~~~
$ set -o vi
~~~
{: .language-bash}

> ## What other options?
> 
> There are many options that can be set, such as changing behaviour what a command fails in a pipe.  See `man bash` for
> explanation of options.
{: .callout}

## Terminal managers

One aspect of using a remote shell via SSH is that if you logout you kill any processes that were running.  Utilities
such as `nohup` can be used to stop processes being stopped such as long-running download of a data file. Alternatively
a terminal manager that remains open on the remote side until you decide to close it can be used instead.

There are 2 main terminal managers in [Screen](https://www.gnu.org/software/screen/) and
[Tmux](https://github.com/tmux/tmux). 

*Screen* is a GNU project that has been around for a long time.  You can create new
sessions or attach to existing sessions remotely. For example on your desktop or laptop the following alias to ssh to
the remote machine can be used:

~~~
$ alias sshhawk1='ssh -t hawk1 screen -RR'
~~~
{: .language-bash}

Where `hawk1` is a ssh host defined in `~/.ssh/config`
~~~
Host hawk1
Hostname hawklogin01.cf.ac.uk
User c.username
ForwardX11 yes
ForwardX11Trusted yes
~~~
{: .output}

The alias will allow just `sshhawk1` to be typed and it will either connect to any detached screen session or create a
new session.  On the remote server (note the ssh config fixes the login node to hawklogin01) `screen -ls` can list the
sessions running.

*Tmux* is available as a module on Hawk with `module load tmux`.  See documentation or `man tmux`.

# Revision control

One of the hardest things to get into a habit with is revision control.  There is a long history of revision control
software.  Personally started wth RCS, used Subversion in a previous job but not the uniquitous revision control
software is [Git](https://git-scm.com).  Git tends to be installed on many Linux systems and is available on Windows via
[Git for Windows](https://gitforwindows.org/) and on Mac via "Xcode Command Line Tools".

Git can be used locally or distributively but the main thing to grasp that with Git there is no "central" version of the
code.  Git repositories can be copied and maintained independently of each other.  The only thing that places some
control to Git is to work to an agreed workflow.  [Github](https://www.github.com) is a popular site to host Git repositories.  Cardiff University
hosts its own [Gitlab](https://git.cardiff.ac.uk) repository.  These sites allow for repositories to be forked (or
copied to another user) and then by agreement within the project the changes can be fed back to the original repository.
When changes are performed usually branches (or a specific copy of the code for the one change) which can then be merged
back to either a fork or the original repository.

A list of common man pages for Git commands are:

~~~
$ man git-init
$ man git-clone
$ man git-branch
$ man git-push
$ man git-pull
$ man git-log
~~~
{: .language-bash}

> ## Clone a repository
>
> Clone this documentation site from Github at https://github.com/ARCCA/hpc-advanced.git
> 
> > ## Solution
> > 
> > ~~~
> > $ git clone https://github.com/ARCCA/hpc-advanced.git
> > ~~~
> > {: .language-bash}
> {: .solution}
{: .challenge}

Many of the operations in Git can be performed directly on the website of the Git repository.  This can be useful for
simple changes.

> ## Further Git information
> 
> Look out for courses and read online tutorials (Github has a good starter guide).  Find excuses to use it and
> practice and get collaborating with colleagues by pushing job scripts online.
{: .callout}

# Dependency in tasks

There are many tools available to solve dependencies.  A traditional (and tried and tested) method is the `Makefile`
method. 

Makefiles are simple text files that describe a dependency between files or operations.  These are usually used to
describe dependencies for building code but can be used for many tasks such as copying files from the Internet before
running your job on the login node.

> ## What dependencies do you have in your work?
>
> Think about the dependencies you may have in your work.  Could things be performed in parallel or serial?
{: .challenge}

A `Makefile` is a file containing variables and dependency information (usually on files). For example a simple "Hello
world" example might be:

~~~
CC=gcc

hello: hello.o
	$(CC) $^ -o $@

hello.o: hello.c
	$(CC) $^ -c -o $@
~~~
{: .language-make}

This makefile will build the `hello` executable by depending on `hello.o` that has a rule to be created using `hello.c`.

See [Make](https://www.gnu.org/software/make/manual/make.html) for further information.

# Compiling code

Compiling code on HPC can be tricky due to the performance of the code can be positively or negatively impacted with
compiler options.  For example recent Intel processors have a new instruction set AVX512.  If the code is not designed
to benefit from this it can actually be negatively impacted.

For completely new code it could be worth using default compiler options of `-O2` to begin with.  Both Intel and GNU
Compilers have this option.

To load the default version of the Intel Compiler use:
~~~
$ module load compiler/intel
~~~
{: .language-bash}

To load the default version of the GNU compiler use:
~~~
$ module load compiler/gnu
~~~
{: .language-bash}

> ## Find out the available options
> 
> How could the available options to compilers be found?
>
> > ## Solution
> > 
> > Using the `man` pages is a good start.
> >
> > ~~~
> > $ man icc
> > $ man gcc
> > ~~~
> > {: .language-bash}
> {: .solution}
{: .challenge}

Intel compilers have a few features worth highlighting:
 * the aggressive default optimisation that can change results of calculations. This is
controlled with `-fp-model` option.  `-fp-model precise` can help with numerical stability or to reproduce answers.
 * the dependency on the underlying GNU compiler for C++ compatability means for later versions of the C++ standard a
   GNU compiler that supports that standard is also loaded. e.g.
~~~
$ module load compiler/gnu/8
$ module load compiler/intel
~~~

There is also the PGI compiler, loaded with `module load compiler/pgi`.  For all available compiler versions see `module av
compiler`.

{% include links.md %}


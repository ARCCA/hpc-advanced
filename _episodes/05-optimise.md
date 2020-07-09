---
title: "Optimisation"
teaching: 45
exercises: 15
questions:
- "Why is more job running so slowly?"
- "What is a GPU and how do I use one?"
- "Where should I read and write my data?"
- "What libraries should I use for X?"
objectives:
- "Profile and understand different between walltime and cputime."
- "Understand what a GPU is and how it can be used."
- "Understand all the different filesystems on the system."
- "Look for existing libraries that provide the function you need."
keypoints:
- "Optimising jobs benefits you *AND* the whole community using the system."
- "Do not reinvent the wheel if you need common functionality in your code."
---

When looking to speed up code there are 2 parts of the code that need to be understood:
* The parallel section - code that benefits from multiple processors.
* The serial section - code that is performed by one processor.

[Amdahl's Law](https://en.wikipedia.org/wiki/Amdahl%27s_law) can be used to describe the performance.  The serial
sections of code will always restrict the possibility of perfect scaling.  This is covered further in OpenMP and MPI
courses.

Whilst analysing code and improving the performance is good practice, it really only makes a difference for developers.
For users it is important to be able to know the options that can speed up their jobs.  GPUs can provide a simple method
for users to benefit from if the software supports them.  GPUs can greatly speed up common tasks such as linear algebra
operations.

Another aspect of performance is the I/O.  This usually related to the filesystem performance but also be network
performance can impact applications using MPI.

# GPUs

Hawk, as of July 2020, contains 2 types of Nvidia GPUs.
 
* [Nvidia V100](https://www.nvidia.com/en-us/data-center/v100/)
  * Ideal for machine learning with Tensor Core technology
  * Dual cards on `gpu_v100` partition.
* [Nvidia Tesla P100](https://www.nvidia.com/en-gb/data-center/tesla-p100/)
  * General purpose GPU with still good performance.
  * Dual cards on `gpu` partition

SLURM requires the job to request both the correct partition and how many GPUs to use.  For example

~~~
$ srun -n 1 -p gpu --gres=gpu:1 --pty bash --login
~~~
{: .language-bash}

This will ask for 1 CPU and 1 GPU card to use.  This sets `CUDA_VISIBLE_DEVICES` to tell software to only use the GPU
cards given to it.

To benefit from GPUs the code requires explicit instructions where it will copy and process the data on the GPU.  Not
all work benefits from GPUs but where it is possible it usually results in great gains in performance.

## Example

Matlab can use GPUs.  Matlab is available with `module load matlab`.  For example run Matlab and run `gpuDevice()` to list the GPU device.

> ## Matlab example
>
> Run Matlab and find out what GPUs are available on both `gpu` and `gpu_v100` partition.
>
> > ## Solution
> >
> > Request a SLURM interactive system with
> > 
> > ~~~
> > $ srun --account=scw1148 -n 1 -p gpu --gres=gpu:1 --pty bash --login
> > ~~~
> > {: .language-bash}
> > 
> > Run Matlab with `matlab -nodisplay` and type `gpuDevice()`
> {: .solution}
{: .challenge}

[Pytorch](https://pytorch.org) is a popular machine learning framework. This is available with module `module load
pytorch` but can also be installed by the user (see [previous session]({{ site.baseurl }}/03-packages).  Pytorch will need some
data files.  These can be downloaded on the login node either by running the example script with `--epochs=0` or within Python such as downloading the MNIST dataset with

~~~
import torchvision
torchvision.datasets.MNIST(root="data", download=True)
~~~
{: .language-python}

There are a number of example tutorial scripts included in the repository at
[Github](https://github.com/pytorch/pytorch) but may be version dependent.

> ## Pytorch example
> 
> Download `mnist.py` from
>
> ~~~
> $ wget --recursive --no-parent {{ site.url }}{{ site.baseurl }}/files/opt1/mnist.py
> ~~~
> {: .language-bash}
>
> Then `module load pytorch` and download the data before running on SLURM
> 
> ~~~
> $ python mnist.py --epochs=0
> ~~~
> {: .language-bash}
>
> Time each run with `--no-cuda` for non-GPU code and with no options to use default GPU.
>
> > ## Solution
> > 
> > Make sure in the same directory downloaded data and request interactive session
> > ~~~
> > $ srun --account=scw1148 -n 1 -p gpu --gres=gpu:1 --pty bash --login
> > ~~~
> > {: .language-bash}
> >
> > Then run with `time`
> >
> > ~~~
> > $ time python mnist.py --no-cuda
> > $ time python mnist.py
> > ~~~
> > {: .language-bash}
> {: .solution}
{: .challenge}

## Further GPU advice

GPUs can be used for many tools from Molecular simulation to Photogrammetry software.  Just check the documentation for
the application for GPUs.

There is also the option of Singularity (see [previous session]({{ site.baseurl }}/03-packages) along with [Nvidia
NGC](https://ngc.nvidia.com/) to lookup and download software that benefits from GPUs.

# Filesystems

On Hawk, there are 3 main filesystems

 * `/scratch` - [Lustre](http://lustre.org/) parallel filesystem.
 * `/home` - [NFS](https://en.wikipedia.org/wiki/Network_File_System)
 * `/tmp` - Local filesystem on each node.  Small compared to others.

Jobs should be run on Lustre unless for specific reasons.  Hawk benefits from new Lustre features such as [Progressive File Layouts](http://wiki.lustre.org/Progressive_File_Layouts) to simplify some of the previous issues with performance. 

> ## Other filesystems on HPC
> 
> There are many types of filesystems that might be encountered for particular use cases. GPFS is similar to Lustre
> while HDFS is for data analytics.
{: .callout}

## Lustre

What is `/scratch`? The filesystem consists of a number of servers.  Each server provides places to store data (OSTs)
and the metadata of the data (MDTs).  These can be listed running:

~~~
$ lfs osts
$ lfs mdts
~~~
{: .language-bash}

Hawk now has 40 OSTs serving 1.2 PB of storage.  There is 1 MDT serving the metadata of the data.  With only 1 metadata
target serving information about files, accessing many small files on Lustre delivers very poor performance.  For a
simple demonstration run

~~~
$ time /bin/ls /scratch
~~~
{: .language-bash}

Can produce

~~~
real	0m0.011s
~~~
{: .output}

and

~~~
$ time ls /scratch
~~~
{: .language-bash}

Can produce

~~~
real	0m0.030s
~~~
{: .output}

The difference between the commands is `ls` tends to be an alias to colorise the output and it will lookup the metadata
of the files which is slow on Lustre.  E.g.

~~~
$ alias
~~~
{: .language-bash}

Will show

~~~
alias ls='ls --color=auto'
~~~
{: .language-bash}

> ## Metadata on other systems
> 
> Repeat on other filesystems on Hawk such as `/tmp` and `/home`.
>
{: .challenge}

With 40 OSTs it should be possible to write out data in parallel upto 40 OSTs in parallel if the code supports it.  

For power users, the way a file is divided across the OSTs can be seen with

~~~
$ lfs getstripe /scratch/c.username/my_file
~~~
{: .language-bash}

## NFS

NFS is a server/client design where all data is served from one server across all clients (compared to Lustre with many servers and storage devices).  Another aspect to remember is caching, `/home` is NFS based and performing an operation such as `ls` will be slow the
first time and faster the next time.  Performance is not consistent.

We *DO NOT* recommend running jobs on `/home`.

## /tmp

`/tmp` is the local filesystem on each node.  It is small (only in the GBs) and shared with other users.  However for
some operations such as small file I/O it can be useful to use, however this tends to be quite rare.

## General advice

 * *ALWAYS* use `/scratch/` for large files input and output.
 * For smaller files possible to use `/home` or `/tmp` but only a few jobs at a time.
 * Write files in large blocks of data.  Do not write and flush output since it is a slow way of writing data.
 * For Intel Fortran Compiler use `export FORT_BUFFERED=y` when running the code.

# Profiling code

Profiling the application is critical in highlighting what parts of the code need to be targetted for optimisation.

For Intel Fortran Compiler (similar to C and C++) use the following:

~~~
$ ifort -g -pg main.f90
~~~
{: .language-bash}

Then run the executable `./a.out` and this will produce `gmon.out` and run

~~~
$ gprof ./a.out gmon.out
~~~
{: .language-bash}

With Python, the following can be used

~~~
$ python -m cProfile [-o output] [-s sort] main.py
~~~
{: .language-bash}

> ## Optimisation
> 
> Obtain the examples at
>
> ~~~
> $ wget --recursive --no-parent {{ site.url }}{{ site.baseurl }}/files/opt1/Makefile
> $ wget --recursive --no-parent {{ site.url }}{{ site.baseurl }}/files/opt1/main.f90
> $ wget --recursive --no-parent {{ site.url }}{{ site.baseurl }}/files/opt1/main.py
> ~~~
> {: .language-bash}
>
> Run them with the relevant optimisation tool.
>
> > ## Solution
> > 
> > Load the Intel Compiler with `module load compiler/intel` and then `make` and then `gprof ./main gmon.out`.  Output
> > will show the timings.
> > 
> > For Python load the version of Python `module load python` and then `python3 -m cProfile main.py` and check output
> > for timings for each function.
> > 
> > Arrays are stored in a certain way and if accessed in sequence then performance is fast, if accessed by jumping
> > around the array then performance bad - CPU cache is not being used efficiently.
> {: .solution}
{: .challenge}

## ARM Forge

ARM Forge, just like with debugging, has an optimiser as well.  It is recommended to use the local GUI.  This is available as a download from [ARM
website](https://developer.arm.com/tools-and-software/server-and-hpc/downloads/arm-forge) and look at the links in
*Remote Client Downloads*

The optimiser, MAP, allows you to run the program either directly or via a job scheduler.  There is also an option to
load a file that contains the sample data from a previous run of the optimiser on Hawk.

Please get in contact if interested.

# Summary

It is worth spending some time looking at software and seeing what options there are such as GPUs.  Use `/scratch`
unless for some demonstratable performance reason.  Please get in contact if you feel your jobs are not working.

{% include links.md %}


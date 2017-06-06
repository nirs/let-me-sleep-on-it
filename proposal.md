# Let me sleep on it - improving concurrency in unexpected ways

## Abstract

Contrary to the common belief, Python has real threads and even with the
famous GIL, they can be used in useful ways. Vdsm is a heavily
multi-threaded Python program, constantly juggling tens of threads
waiting for blocking system calls. In this talk we will explore a real
world thread synchronization problem taken from Vdsm's LVM cache module.
We will demonstrate the problem using simple tests and show the
unexpected solution.

## Bio

Nir has worked for Red Hat on oVirt storage since 2013, taming the Vdsm
beast. Has been tinkering with Python and contributing to many free software
projects since 2003. See https://github.com/nirs for recent work.

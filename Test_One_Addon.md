
##Test1 Helper
##Assignment2-Tet1 Addon
###Ahla Cho


####Multi\*
Define the following and give examples of each.

1. Multi-tasking
   - Definition: Multi-tasking is the ability of an operating system to execute more than one task simultaneously on a single processor      machine. However, in reality two tasks on a single processor machines cannot be executed at the same time. 
     Actually CPU switches very quickly from one task to the next task that appears as if all the tasks are executing at the same time. 
   - Examples: Listening to music and searching internet browsing at the same time

2. Multi-programming
   - Definition: Multi-programming is the ability of an operating system to execute more than one program on a single processor machine.      More than one program can reside into the main memeory at one same time.
   - Examples: A computer running excel and chrome browser simultaneously is an example of multiprogramming.

3. Multi-processing
   - Definition: Multi-processing is the abiltiy of an operating system to execute more than one process simultaneously on a multi-          processor machine. Computer uses more than one CPU at a time.
   - Examples: When create a file then computer takes Time and date default

4. Multi-threaded
   - Definition: Multi-threading is the ability of an operating system to execute the different parts of a program called threads at the      same time. A thread is a smallest part of process that can run concurrently with the other threads of the same process.
   - Examples: Basically seen when more number of clients access the server.


####Review Questions From Chapters 3

1. What is an instruction trace?
   - A sequence of instructions tha execute for a process

2. What common events lead to the creation of a process?
   - New batch job
   - Interactive log-on
   - Created by OS to provide a service
   - Spawned by existing proceess

3. What does it mean to preempt a process?
   - To interrupt a process without requiring its cooperation, and with intent to resume it later.

4. What is swapping and what is its purpose?
   - Swapping was an older form of memory management. 
   - Move part or all of a process from main memory to disk.
 

5. Why does Figure 3.9b have two blocked states?
   - There are two independent concepts:
     (a)Whther a process is waiting on an event (blocked or not)
     (b)Whether a process has been swapped out of main memory(suspended or not)
     To accommodate this 2X2 combination, we need two Ready states and two Blocked states.

6. List four characteristics of a suspended process.
   - The process is not immediately available for execution.
   - The process may or may not be waiting for a event.
   - The process was placed in a suspended state by an agent: either itself, a parent process, or the operating system, for the purpose      of preventing its execution.
   - The process may not be removed from this state until the agent explicitly orders the removal.

7. List three general categories of information in a process control block.
   - Process identification
   - Processor state information
   - Process control information

8. Why are two modes (user and kernel) needed?
   - To protect the OS and key operating system tables, such as process control blocks, from interface by user programs.

9. What is the difference between an interrupt and a trap?
   - Interrupt is external and independent from current running process.
   - Trap is error or exception condition generated within the currently running process.

10. Give three examples of an interrupt.
    - Clock interrupt
    - I/O interrrup
    - Memory fault

11. What is the difference between a mode switch and a process switch?
    - A mode switch may occur without changing the state of the process that is currently in the Running state. 
      Whereas a process switch involves a state change - much more expensive.

# dynamic_thread_pinning
This script allows users to pin specific threads to user-defined CPU cores while ensuring that floating threads are assigned dynamically to balance CPU load. 

## Prerequisites

sudo apt install python3
pip3 install psutil

## Usage
Mention name of threads to get pinned.
Enter cores to pin to those threads
Enter cores for floating threads, meaning all other threads will float between the cores user specifies. 

python3 thread_pinning.py

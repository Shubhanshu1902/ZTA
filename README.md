Instructions to run the code.
1. Run: mk fifo pipe/{pipeName}
2. while true; do eval "$(cat pipe/{pipeName})" > pipe/ output.txt; done
3. 

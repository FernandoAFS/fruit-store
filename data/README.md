
# Data sub-directory

Empty on prupose.

To combine all data in one single json file use

`find data -type f | awk -F \/ '{print $NF " " $0}' | sort -n | cut -d ' ' -f 2 | xargs jq -s '.' > data_list.json`


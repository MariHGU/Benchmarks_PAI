# Add Conda's binary directory to the PATH
export PATH="/Users/geoff/anaconda2/bin:$PATH"

# Initialize conda without auto-activating base environment
__conda_setup="$('/Users/geoff/anaconda2/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    # Add the necessary shell setup for conda activate to work without auto-activating base
    eval "$__conda_setup"
    # Disable auto-activation of base environment
    conda config --set auto_activate_base false
else
    if [ -f "/Users/geoff/anaconda2/etc/profile.d/conda.sh" ]; then
        . "/Users/geoff/anaconda2/etc/profile.d/conda.sh"
    fi
fi
unset __conda_setup
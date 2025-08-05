# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/Users/geoff/anaconda2/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    # Don't eval $__conda_setup (this prevents automatic activation)
    if [ -f "/Users/geoff/anaconda2/etc/profile.d/conda.sh" ]; then
        . "/Users/geoff/anaconda2/etc/profile.d/conda.sh"
    else
        export PATH="/Users/geoff/anaconda2/bin:$PATH"
    fi
else
    # Don't eval $__conda_setup (this prevents automatic activation)
    if [ -f "/Users/geoff/anaconda2/etc/profile.d/conda.sh" ]; then
        . "/Users/geoff/anaconda2/etc/profile.d/conda.sh"
    else
        export PATH="/Users/geoff/anaconda2/bin:$PATH"
    fi
fi

# Unset irrelevant variables
unset __conda_setup
export CONDA_AUTO_ACTIVATE_BASE=false  # Add this line to prevent base activation
# <<< conda initialize <<<
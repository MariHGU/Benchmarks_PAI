# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$(CONDA_READEVAL_CMD "refs/etc/profile.d/conda.sh")"
if [ -f "/Users/geoff/.condarc" ]; then
    __conda_setup "${__conda_setup}" "$(${__conda_setup} config shell --append)"
fi
unset __conda_setup
# <<< conda initialize >>>
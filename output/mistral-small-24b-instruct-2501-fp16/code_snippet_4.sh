# >>> conda initialize >>>
   __conda_setup="$(/Users/geoff/anaconda2/bin/conda 'shell.bash' 'hook' 2> /dev/null)"
   if [ $? -eq 0 ]; then
       eval "$__conda_setup"
       # Disable automatic activation of the base environment
       export CONDA_DEFAULT_ENV=""
   else
       if [ -f "/Users/geoff/anaconda2/etc/profile.d/conda.sh" ]; then
           . "/Users/geoff/anaconda2/etc/profile.d/conda.sh"
       else
           export PATH="/Users/geoff/anaconda2/bin:$PATH"
       fi
   fi
   unset __conda_setup
   # <<< conda initialize <<<
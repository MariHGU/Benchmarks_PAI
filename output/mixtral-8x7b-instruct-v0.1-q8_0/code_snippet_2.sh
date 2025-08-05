# Add Anaconda2 install location to PATH (without activating base env)
export PATH="/Users/geoff/anaconda2/bin:$PATH"

# Check if conda exists, and add conda activate to bashrc if not found
if ! command -v conda &> /dev/null; then
    echo 'conda not found, adding conda activate to .bashrc'
    echo 'source activate /Users/geoff/anaconda2/etc/profile.d/conda.sh' >> ~/.bashrc
fi
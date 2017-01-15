VIRTUALENV_DIR=/opt/vipbot

# If activation script of the virtual environment exists,
# let's hope that it's all good
if [[ -e "$VIRTUALENV_DIR/bin/activate" ]]; then
    exit 0
fi

# Check that virtualenv is present
which virtualenv &> /dev/null
if [[ "$?" -ne 0 ]]; then
  echo "$0: CRITICAL: dependency 'virtualenv' is not installed."
  exit 3
fi

# Create the virtual environment
virtualenv $VIRTUALENV_DIR -p python3
if [[ $? -ne 0 ]]; then
    echo "${0}: CRITICAL: could not create virtual environment under ${VIRTUALENV_DIR}"
    exit 2
fi

# Acivate the environment
source $VIRTUALENV_DIR/bin/activate
if [[ $? -ne 0 ]]; then
    echo "${0}: CRITICAL: could not activate virtual environment: ${VIRTUALENV_DIR}/bin/activate"
    exit 3
fi

# Install Python package
python setup.py install
if [[ $? -ne 0 ]]; then
    echo "${0}: CRITICAL: could not install 'vipbot' package under Python virtual environment"
    exit 4
fi

exit 0

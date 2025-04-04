#!/bin/bash
# This script will prepare Status-Page to run after the code has been upgraded to
# its most recent release.

# This script will invoke Python with the value of the PYTHON environment
# variable (if set), or fall back to "python3". Note that Status-Page requires
# Python 3.10 or later.

cd "$(dirname "$0")"
VIRTUALENV="$(pwd -P)/venv"
PYTHON="${PYTHON:-python3}"

# Validate the minimum required Python version
COMMAND="${PYTHON} -c 'import sys; exit(1 if sys.version_info < (3, 10) else 0)'"
PYTHON_VERSION=$(eval "${PYTHON} -V")
eval $COMMAND || {
  echo "-------------------------------------------------------------------------"
  echo "ERROR: Unsupported Python version: ${PYTHON_VERSION}. Status-Page requires"
  echo "Python 3.10 or later. To specify an alternate Python executable, set"
  echo "the PYTHON environment variable. For example:"
  echo ""
  echo "  sudo PYTHON=/usr/bin/python3.10 ./upgrade.sh"
  echo ""
  echo "To show your current Python version: ${PYTHON} -V"
  echo "-------------------------------------------------------------------------"
  exit 1
}
echo "Using ${PYTHON_VERSION}"

# Remove the existing virtual environment (if any)
if [ -d "$VIRTUALENV" ]; then
  COMMAND="rm -rf ${VIRTUALENV}"
  echo "Removing old virtual environment..."
  eval $COMMAND
else
  WARN_MISSING_VENV=1
fi

# Create a new virtual environment
COMMAND="${PYTHON} -m venv ${VIRTUALENV}"
echo "Creating a new virtual environment at ${VIRTUALENV}..."
eval $COMMAND || {
  echo "--------------------------------------------------------------------"
  echo "ERROR: Failed to create the virtual environment. Check that you have"
  echo "the required system packages installed and the following path is"
  echo "writable: ${VIRTUALENV}"
  echo "--------------------------------------------------------------------"
  exit 1
}

# Activate the virtual environment
source "${VIRTUALENV}/bin/activate"

# Upgrade pip
COMMAND="pip install --upgrade pip"
echo "Updating pip ($COMMAND)..."
eval $COMMAND || exit 1
pip -V

# Install necessary system packages
COMMAND="pip install wheel"
echo "Installing Python system packages ($COMMAND)..."
eval $COMMAND || exit 1

# Install required Python packages
COMMAND="pip install -r requirements.txt"
echo "Installing core dependencies ($COMMAND)..."
eval $COMMAND || exit 1

# Install optional packages (if any)
if [ -s "local_requirements.txt" ]; then
  COMMAND="pip install -r local_requirements.txt"
  echo "Installing local dependencies ($COMMAND)..."
  eval $COMMAND || exit 1
elif [ -f "local_requirements.txt" ]; then
  echo "Skipping local dependencies (local_requirements.txt is empty)"
else
  echo "Skipping local dependencies (local_requirements.txt not found)"
fi

# Apply any database migrations
COMMAND="python3 statuspage/manage.py migrate"
echo "Applying database migrations ($COMMAND)..."
eval $COMMAND || exit 1

# Build the local documentation
COMMAND="mkdocs build"
echo "Building documentation ($COMMAND)..."
eval $COMMAND || exit 1

# Collect static files
COMMAND="python3 statuspage/manage.py collectstatic --no-input"
echo "Collecting static files ($COMMAND)..."
eval $COMMAND || exit 1

# Delete any stale content types
COMMAND="python3 statuspage/manage.py remove_stale_contenttypes --no-input"
echo "Removing stale content types ($COMMAND)..."
eval $COMMAND || exit 1

# Delete any expired user sessions
COMMAND="python3 statuspage/manage.py clearsessions"
echo "Removing expired user sessions ($COMMAND)..."
eval $COMMAND || exit 1

# Clear the cache
COMMAND="python3 statuspage/manage.py clearcache"
echo "Clearing the cache ($COMMAND)..."
eval $COMMAND || exit 1

if [ -v WARN_MISSING_VENV ]; then
  echo "--------------------------------------------------------------------"
  echo "WARNING: No existing virtual environment was detected. A new one has"
  echo "been created. Update your systemd service files to reflect the new"
  echo "Python and gunicorn executables. (If this is a new installation,"
  echo "this warning can be ignored.)"
  echo ""
  echo "status-page.service ExecStart:"
  echo "  ${VIRTUALENV}/bin/gunicorn"
  echo ""
  echo "status-page-scheduler.service ExecStart:"
  echo "  ${VIRTUALENV}/bin/python"
  echo ""
  echo "status-page-rq.service ExecStart:"
  echo "  ${VIRTUALENV}/bin/python"
  echo ""
  echo "After modifying these files, reload the systemctl daemon:"
  echo "  > systemctl daemon-reload"
  echo "--------------------------------------------------------------------"
fi

echo "Upgrade complete! Don't forget to restart the Status-Page services:"
echo "  > sudo systemctl restart status-page status-page-scheduler status-page-rq"

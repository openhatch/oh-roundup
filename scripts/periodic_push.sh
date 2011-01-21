#!/bin/bash
cd $HOME/trackers/bugs/

# Make sure that "db" is not part of the repository
if git ls-files | grep -q ^db; then
   echo "Eek, the db is in the repository."
   exit 1
fi

# Okay, it should be safe. Push.
git push --quiet origin HEAD:master | grep -v 'Syncing Gitorious'

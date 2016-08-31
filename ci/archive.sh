#!/bin/bash -ex

pushd `dirname $0`/.. > /dev/null
root=$(pwd -P)
popd > /dev/null

#----------------------------------------------------------------------

# gather some data about the repo
source $root/ci/vars.sh

sh $root/install.sh

# Path to py file
src=$root

# stage the artifact for a mvn deploy
mv $src $root/$APP.$EXT

